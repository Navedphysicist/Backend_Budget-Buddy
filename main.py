from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import testimonials, categories, expenses, incomes
from app.db.database import engine
from app.db.database import Base


Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="BudgetBuddy API",
    description="API for managing testimonials, categories, expenses, incomes, and budget summaries",
    version="1.0.0"
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
def root():
    return {"message": "Welcome to BudgetBuddy API"}
