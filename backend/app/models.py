"""
SQLAlchemy database models for Inside My Meal
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Food(Base):
    """Stores food items from external APIs"""
    __tablename__ = "foods"
    __table_args__ = (
        UniqueConstraint("source", "source_food_id", name="uq_food_source_source_food_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False)  # 'usda' or 'openfoodfacts'
    source_food_id = Column(String(500), nullable=False)
    name = Column(String(500), nullable=False, index=True)
    brand = Column(String(255), nullable=True)
    serving_size_g = Column(Float, nullable=False)
    calories = Column(Float, nullable=True)
    carbs_g = Column(Float, nullable=True)
    sugars_g = Column(Float, nullable=True)
    fiber_g = Column(Float, nullable=True)
    protein_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    glycemic_category = Column(String(50), nullable=True)  # 'low', 'medium', 'high'
    raw_json = Column(JSON, nullable=True)  # Store full API response
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    meal_items = relationship("MealItem", back_populates="food", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Food {self.name}>"


class Meal(Base):
    """Stores user meal sessions"""
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_session_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    meal_items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan")
    simulations = relationship("Simulation", back_populates="meal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Meal {self.name}>"


class MealItem(Base):
    """Individual foods that make up a meal"""
    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)  # Multiplier
    serving_multiplier = Column(Float, nullable=False, default=1.0)
    carbs_g = Column(Float, nullable=True)
    sugars_g = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)

    # Relationships
    meal = relationship("Meal", back_populates="meal_items")
    food = relationship("Food", back_populates="meal_items")

    def __repr__(self):
        return f"<MealItem quantity={self.quantity}>"


class Simulation(Base):
    """Glucose simulation results based on meal and lifestyle"""
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    lifestyle_profile = Column(JSON, nullable=False)  # Store lifestyle settings
    estimated_peak_mg_dl = Column(Float, nullable=False)
    glucose_grams_baseline = Column(Float, nullable=False)
    glucose_grams_peak = Column(Float, nullable=False)
    insulin_load_score = Column(Float, nullable=False)
    storage_risk_score = Column(Float, nullable=False)
    explanation_json = Column(JSON, nullable=True)  # Educational explanation
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    meal = relationship("Meal", back_populates="simulations")

    def __repr__(self):
        return f"<Simulation peak={self.estimated_peak_mg_dl}>"


class EducationCard(Base):
    """Educational content blocks"""
    __tablename__ = "education_cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    animation_type = Column(String(100), nullable=True)  # 'glucose_spike', 'insulin_action', etc.
    category = Column(String(100), nullable=True)  # 'basic', 'advanced', 'comparison'
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EducationCard {self.title}>"

