from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# Testimonial schemas
class TestimonialBase(BaseModel):
    name: str
    role: str
    quote: str
    rating: int
    image: Optional[str] = None

class TestimonialCreate(TestimonialBase):
    pass

class Testimonial(TestimonialBase):
    id: int
    
    class Config:
        from_attributes = True

# Category schemas
class CategoryBase(BaseModel):
    name: str
    icon: str
    budget: float
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# PaymentMode schemas
class PaymentModeBase(BaseModel):
    name: str
    icon: str
    color: Optional[str] = None

class PaymentModeCreate(PaymentModeBase):
    pass

class PaymentMode(PaymentModeBase):
    id: int
    
    class Config:
        from_attributes = True

# Expense schemas
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

# Income schemas
class IncomeBase(BaseModel):
    amount: float
    date: date
    source: str
    is_recurring: bool = False

class IncomeCreate(IncomeBase):
    pass

class IncomeUpdate(BaseModel):
    amount: Optional[float] = None
    source: Optional[str] = None
    date: Optional[date] = None
    is_recurring: Optional[bool] = None

class Income(IncomeBase):
    id: int
    
    class Config:
        from_attributes = True

# Category with expense total
class CategoryWithExpense(Category):
    expense: float
