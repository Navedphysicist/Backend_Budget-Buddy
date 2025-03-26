from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import testimonials, categories, expenses, incomes
from app.db.database import engine
from app.models import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup - initialize database
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # Cleanup - close any connections if needed
    await engine.dispose()


app = FastAPI(
    title="BudgetBuddy API",
    description="API for managing testimonials, categories, expenses, incomes, and budget summaries",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(testimonials.router, tags=["Testimonials"])
app.include_router(categories.router, tags=["Categories"])
app.include_router(expenses.router, tags=["Expenses"])
app.include_router(incomes.router, tags=["Incomes"])


@app.get("/")
async def root():
    return {"message": "Welcome to BudgetBuddy API"}
