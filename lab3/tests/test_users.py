import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_db, engine, Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(TEST_DATABASE_URL)
TestAsyncSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_duplicate_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/users/", json={"username": "testuser", "email": "test@example.com"})
        response = await ac.post("/users/", json={"username": "testuser", "email": "other@example.com"})
    assert response.status_code == 409
