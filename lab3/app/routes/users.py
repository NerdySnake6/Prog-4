from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(
            (models.User.username == user_data.username) | (models.User.email == user_data.email)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User with this username or email already exists")
    
    user = models.User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/", response_model=list[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    return result.scalars().all()

@router.get("/{user_id}", response_model=schemas.UserWithSubscriptions)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.subscriptions).selectinload(models.Subscription.currency))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscriptions = [sub.currency for sub in user.subscriptions]
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "subscriptions": subscriptions
    }

@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(user_id: int, user_data: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.username and user_data.username != user.username:
        chk = await db.execute(select(models.User).where(models.User.username == user_data.username))
        if chk.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Username already taken")
    if user_data.email and user_data.email != user.email:
        chk = await db.execute(select(models.User).where(models.User.email == user_data.email))
        if chk.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Email already taken")
    
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
