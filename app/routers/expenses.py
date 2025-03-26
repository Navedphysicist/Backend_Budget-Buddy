from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.models import Expense
from app.schemas.schemas import Expense as ExpenseSchema, ExpenseCreate, ExpenseUpdate
from typing import List, Optional
from datetime import datetime
import pandas as pd
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

@router.get("/expense", response_model=List[ExpenseSchema])
async def get_expenses(
    category: Optional[str] = None,
    recurring: Optional[bool] = None,
    month: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, gt=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(Expense)
    if category:
        query = query.filter(Expense.category.has(name=category))
    if recurring is not None:
        query = query.filter(Expense.recurring == recurring)
    if month:
        try:
            query = query.filter(func.strftime('%Y-%m', Expense.date) == month)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid month format. Use YYYY-MM")
    if search:
        query = query.filter(Expense.note.ilike(f"%{search}%"))
    
    # Pagination
    limit = 10
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    expenses = result.scalars().all()
    return expenses

@router.post("/expense", response_model=ExpenseSchema, status_code=201)
async def create_expense(expense: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

@router.delete("/expense/{expense_id}")
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expense).filter(Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    await db.delete(expense)
    await db.commit()
    return {"message": "Expense deleted"}

@router.patch("/expense/{expense_id}", response_model=ExpenseSchema)
async def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Expense).filter(Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    for field, value in expense_update.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    
    await db.commit()
    await db.refresh(expense)
    return expense

@router.get("/getCSV")
async def get_expenses_csv(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expense))
    expenses = result.scalars().all()
    
    # Convert to DataFrame
    expense_data = []
    for expense in expenses:
        expense_data.append({
            'id': expense.id,
            'amount': expense.amount,
            'date': expense.date,
            'note': expense.note,
            'recurring': expense.recurring,
            'category': expense.category.name if expense.category else None,
            'payment_mode': expense.payment_mode.name if expense.payment_mode else None
        })
    
    df = pd.DataFrame(expense_data)
    
    # Create CSV
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=expenses_{datetime.now().strftime('%Y%m%d')}.csv"}
    )
    
    return response
