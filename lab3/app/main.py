from fastapi import FastAPI
from .database import engine, Base
from .routes import users, currencies, subscriptions

app = FastAPI(title="Currency Tracker", version="1.0.0")

app.include_router(users.router)
app.include_router(currencies.router)
app.include_router(subscriptions.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Currency Tracker API. Go to /docs for documentation"}
