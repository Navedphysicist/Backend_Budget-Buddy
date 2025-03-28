from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.testimonial import DbTestimonial
from app.schemas.schemas import Testimonial as TestimonialSchema
from typing import List

router = APIRouter()

@router.get("/testimonials", response_model=List[TestimonialSchema])
def get_testimonials(db: Session = Depends(get_db)):
    testimonials = db.query(DbTestimonial).all()
    return testimonials
