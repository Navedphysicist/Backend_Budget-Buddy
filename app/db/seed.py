from sqlalchemy.orm import Session
from app.models.models import Testimonial, Category, PaymentMode


def seed_data(db: Session):
    # Seed testimonials
    testimonials = [
        Testimonial(
            name="Richard James",
            role="Small Business Owner",
            quote="BudgetBuddy has transformed how I manage my business finances. The intuitive interface and powerful tracking tools have saved me countless hours.",
            rating=5,
            image="https://mighty.tools/mockmind-api/content/human/1.jpg"
        ),
        Testimonial(
            name="Sarah White",
            role="Freelance Consultant",
            quote="As a professional, I need reliable financial tools. BudgetBuddy delivers with its comprehensive reporting and budget management features.",
            rating=5,
            image="https://mighty.tools/mockmind-api/content/human/2.jpg"
        ),
        Testimonial(
            name="Emma Brown",
            role="Entrepreneur",
            quote="The receipt scanner feature has been a game-changer for tracking my expenses. I highly recommend BudgetBuddy to anyone looking to improve their financial management.",
            rating=4,
            image="https://mighty.tools/mockmind-api/content/human/3.jpg"
        )
    ]
    
    # Seed categories
    categories = [
        Category(name="Food expenses", icon="Utensils", budget=5000, color="amber"),
        Category(name="Shopping", icon="ShoppingCart", budget=8000, color="blue"),
        Category(name="Entertainment", icon="Gamepad", budget=3000, color="purple"),
        Category(name="Medical", icon="Stethoscope", budget=2000, color="red"),
        Category(name="Bills and Utilities", icon="FileText", budget=4000, color="gray"),
        Category(name="Education", icon="GraduationCap", budget=7000, color="green")
    ]
    
    # Seed payment modes
    payment_modes = [
        PaymentMode(name="Credit Card", icon="CreditCard", color="blue"),
        PaymentMode(name="Debit Card", icon="CreditCard", color="green"),
        PaymentMode(name="Cash", icon="Money", color="gray"),
        PaymentMode(name="UPI", icon="Mobile", color="purple")
    ]
    
    # Add all to session
    for testimonial in testimonials:
        db.add(testimonial)
    
    for category in categories:
        db.add(category)
    
    for payment_mode in payment_modes:
        db.add(payment_mode)
    
    # Commit the session
    db.commit()
