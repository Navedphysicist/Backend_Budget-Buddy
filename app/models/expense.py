from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class DbExpense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String, nullable=True)
    recurring = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    payment_mode_id = Column(Integer, ForeignKey("payment_modes.id"))
    
    category = relationship("DbCategory", back_populates="expenses")
    payment_mode = relationship("DbPaymentMode", back_populates="expenses")
