from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models, schemas, cbr
from ..database import get_db

router = APIRouter(prefix="/currencies", tags=["currencies"])

@router.get("/", response_model=list[schemas.CurrencyOut])
async def list_currencies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Currency))
    return result.scalars().all()

@router.post("/update", status_code=200)
async def update_currencies(db: AsyncSession = Depends(get_db)):
    try:
        currencies_data = await cbr.fetch_currencies()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"CBR service unavailable: {e}")
    
    updated = 0
    for data in currencies_data:
        result = await db.execute(
            select(models.Currency).where(models.Currency.code == data['code'])
        )
        currency = result.scalar_one_or_none()
        if currency:
            if currency.name != data['name']:
                currency.name = data['name']
                updated += 1
        else:
            db.add(models.Currency(code=data['code'], name=data['name']))
            updated += 1
    await db.commit()
    return {"message": f"Currencies updated. {updated} changes."}

@router.get("/{currency_code}/rate")
async def get_currency_rate(currency_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Currency).where(models.Currency.code == currency_code.upper())
    )
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found in database")
    
    try:
        rate = await cbr.get_rate(currency_code.upper())
    except ValueError:
        raise HTTPException(status_code=404, detail="Currency not found in CBR response")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"CBR service error: {e}")
    
    return {
        "code": currency.code,
        "name": currency.name,
        "rate": rate,
        "date": "today"
    }
