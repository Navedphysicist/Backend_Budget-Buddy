from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.models import Category, Expense
from app.schemas.schemas import Category as CategorySchema, CategoryWithExpense
from typing import List

router = APIRouter()

@router.get("/categories", response_model=List[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories

@router.get("/category_expense", response_model=List[CategoryWithExpense])
async def get_category_expenses(db: AsyncSession = Depends(get_db)):
    query = select(
        Category,
        func.coalesce(func.sum(Expense.amount), 0).label('expense')
    ).outerjoin(Expense).group_by(Category.id)
    
    result = await db.execute(query)
    categories = []
    for row in result:
        category_dict = row[0].__dict__
        category_dict['expense'] = float(row[1])
        categories.append(category_dict)
    return categories

@router.get("/category_budget", response_model=List[CategorySchema])
async def get_category_budgets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories
