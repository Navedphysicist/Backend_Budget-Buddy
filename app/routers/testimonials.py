from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.models import Testimonial
from app.schemas.schemas import Testimonial as TestimonialSchema
from typing import List

router = APIRouter()

@router.get("/testimonials", response_model=List[TestimonialSchema])
async def get_testimonials(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Testimonial))
    testimonials = result.scalars().all()
    return testimonials
