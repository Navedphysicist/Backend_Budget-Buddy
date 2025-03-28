from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.category import Category
from app.schemas.payment_mode import PaymentMode

class ExpenseBase(BaseModel):
    amount: float
    date: date
    note: Optional[str] = None
    recurring: bool = False
    category_id: int
    payment_mode_id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    note: Optional[str] = None
    date: Optional[date] = None
    recurring: Optional[bool] = None
    category_id: Optional[int] = None
    payment_mode_id: Optional[int] = None

class Expense(ExpenseBase):
    id: int
    category: Category
    payment_mode: PaymentMode
    
    class Config:
        from_attributes = True
