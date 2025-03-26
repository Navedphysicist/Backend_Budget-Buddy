from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class Testimonial(Base):
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    quote = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    image = Column(String, nullable=True)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    color = Column(String, nullable=True)
    expenses = relationship("Expense", back_populates="category")

class PaymentMode(Base):
    __tablename__ = "payment_modes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    color = Column(String, nullable=True)
    expenses = relationship("Expense", back_populates="payment_mode")

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    recurring = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    payment_mode_id = Column(Integer, ForeignKey("payment_modes.id"))
    
    category = relationship("Category", back_populates="expenses")
    payment_mode = relationship("PaymentMode", back_populates="expenses")

class Income(Base):
    __tablename__ = "incomes"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    source = Column(String, nullable=False)
    is_recurring = Column(Boolean, default=False)
