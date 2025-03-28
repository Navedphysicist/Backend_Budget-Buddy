from pydantic import BaseModel
from typing import Optional

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

class CategoryWithExpense(Category):
    expense: float
