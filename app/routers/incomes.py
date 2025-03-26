from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.models import Income
from app.schemas.schemas import Income as IncomeSchema, IncomeCreate, IncomeUpdate
from typing import List, Optional


router = APIRouter()

@router.get("/income", response_model=List[IncomeSchema])
async def get_incomes(
    recurring: Optional[bool] = None,
    source: Optional[str] = None,
    month: Optional[str] = None,
    top: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Income)
    
    if recurring is not None:
        query = query.filter(Income.is_recurring == recurring)
    if source:
        query = query.filter(Income.source == source)
    if month:
        try:
            query = query.filter(func.strftime('%Y-%m', Income.date) == month)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid month format. Use YYYY-MM")
    if top:
        query = query.limit(top)
    
    result = await db.execute(query)
    incomes = result.scalars().all()
    return incomes

@router.post("/income", response_model=IncomeSchema, status_code=201)
async def create_income(income: IncomeCreate, db: AsyncSession = Depends(get_db)):
    db_income = Income(**income.model_dump())
    db.add(db_income)
    await db.commit()
    await db.refresh(db_income)
    return db_income

@router.delete("/income/{income_id}")
async def delete_income(income_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Income).filter(Income.id == income_id))
    income = result.scalar_one_or_none()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    await db.delete(income)
    await db.commit()
    return {"message": "Income deleted"}

@router.patch("/income/{income_id}", response_model=IncomeSchema)
async def update_income(
    income_id: int,
    income_update: IncomeUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Income).filter(Income.id == income_id))
    income = result.scalar_one_or_none()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    
    for field, value in income_update.model_dump(exclude_unset=True).items():
        setattr(income, field, value)
    
    await db.commit()
    await db.refresh(income)
    return income
