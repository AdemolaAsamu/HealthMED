"""
Inside My Meal FastAPI Application
Educational platform for understanding glucose and metabolic health
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, SessionLocal, engine
from app.api import foods, meals, simulations, education, admin
from app import models
from app.migrations.init_db import seed_education_cards, seed_foods
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inside My Meal API",
    description="Educational API for understanding blood glucose and metabolic health",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(foods.router)
app.include_router(meals.router)
app.include_router(simulations.router)
app.include_router(education.router)
app.include_router(admin.router)


@app.on_event("startup")
def seed_default_content_if_empty():
    """
    Render starts the app with uvicorn, not backend/run.py.
    Seed default foods and education cards when a fresh production DB is empty.
    """
    db = SessionLocal()
    try:
        has_foods = db.query(models.Food.id).first() is not None
        has_education = db.query(models.EducationCard.id).first() is not None
    finally:
        db.close()

    if not has_foods:
        seed_foods()
    if not has_education:
        seed_education_cards()


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Welcome to Inside My Meal API",
        "description": "Educational platform for understanding glucose and metabolic health",
        "docs": "/docs",
        "version": "1.0.0",
        "disclaimer": "This is an educational tool, not medical advice. Always consult healthcare providers.",
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/api/disclaimers", tags=["disclaimers"])
def get_disclaimers():
    """Return medical/legal disclaimers"""
    return {
        "primary_disclaimer": (
            "Inside My Meal is an EDUCATIONAL TOOL ONLY. It is NOT medical advice, "
            "does NOT diagnose conditions, and does NOT replace professional healthcare consultation."
        ),
        "glucose_response": (
            "Individual glucose responses vary significantly based on genetics, fitness level, "
            "stress levels, sleep, medications, and other factors. This simulation uses simplified "
            "educational estimates and is not personalized."
        ),
        "cgm_recommendation": (
            "If you have diabetes or prediabetes, use a Continuous Glucose Monitor (CGM) "
            "for personal glucose data rather than relying on estimates."
        ),
        "medical_conditions": [
            "If you have diabetes or prediabetes: Consult your healthcare provider or endocrinologist",
            "If you are pregnant or nursing: Consult your OB-GYN",
            "If you have an eating disorder: Seek professional psychological support",
            "If you are on medications affecting glucose: Consult your pharmacist or doctor"
        ],
        "limitations": [
            "This tool cannot account for individual metabolic variations",
            "It does not consider medications or supplements",
            "It does not assess personal medical history",
            "It does not replace professional glucose monitoring",
            "Results are educational estimates only"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

