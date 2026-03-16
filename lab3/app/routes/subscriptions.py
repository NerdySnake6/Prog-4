from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def subscribe(sub_data: schemas.SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(models.User, sub_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(models.Currency).where(models.Currency.code == sub_data.currency_code.upper())
    )
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    existing = await db.execute(
        select(models.Subscription).where(
            and_(
                models.Subscription.user_id == sub_data.user_id,
                models.Subscription.currency_id == currency.id
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Already subscribed")
    
    sub = models.Subscription(user_id=user.id, currency_id=currency.id)
    db.add(sub)
    await db.commit()
    return {"message": "Subscribed"}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe(sub_data: schemas.SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(models.User, sub_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(models.Currency).where(models.Currency.code == sub_data.currency_code.upper())
    )
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    sub = await db.execute(
        select(models.Subscription).where(
            and_(
                models.Subscription.user_id == sub_data.user_id,
                models.Subscription.currency_id == currency.id
            )
        )
    )
    sub = sub.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    await db.delete(sub)
    await db.commit()
