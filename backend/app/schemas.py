"""
Pydantic schemas for request/response validation
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


# ============= Food Schemas =============
class FoodBase(BaseModel):
    name: str
    brand: Optional[str] = None
    serving_size_g: float
    calories: Optional[float] = None
    carbs_g: Optional[float] = None
    sugars_g: Optional[float] = None
    fiber_g: Optional[float] = None
    protein_g: Optional[float] = None
    fat_g: Optional[float] = None
    glycemic_category: Optional[str] = None


class FoodCreate(FoodBase):
    source: str
    source_food_id: str
    raw_json: Optional[Dict[str, Any]] = None


class FoodResponse(FoodBase):
    id: int
    source: str
    source_food_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= Meal Schemas =============
class MealItemCreate(BaseModel):
    food_id: int
    quantity: float = 1.0
    serving_multiplier: float = 1.0


class MealItemResponse(BaseModel):
    id: int
    food_id: int
    quantity: float
    serving_multiplier: float
    carbs_g: Optional[float]
    sugars_g: Optional[float]
    calories: Optional[float]
    food: Optional[FoodResponse] = None

    class Config:
        from_attributes = True


class MealCreate(BaseModel):
    user_session_id: str
    name: Optional[str] = None
    items: List[MealItemCreate]


class MealResponse(BaseModel):
    id: int
    user_session_id: str
    name: Optional[str] = None
    created_at: datetime
    meal_items: List[MealItemResponse] = []

    class Config:
        from_attributes = True


class MealSummary(BaseModel):
    total_calories: float
    total_carbs_g: float
    total_sugars_g: float
    total_fiber_g: float
    total_protein_g: float
    total_fat_g: float
    net_carbs_g: float
    estimated_glycemic_load: float


# ============= Lifestyle Schemas =============
class LifestyleProfile(BaseModel):
    is_sedentary: bool = True
    post_meal_walk_minutes: int = 0
    regular_exercise: bool = False
    exercise_intensity: Optional[str] = None  # 'low', 'moderate', 'high'
    poor_sleep: bool = False
    high_stress: bool = False
    high_muscle_mass: bool = False
    insulin_resistant: bool = False
    prediabetic: bool = False
    high_fiber_meal: bool = False
    protein_first: bool = False


# ============= Simulation Schemas =============
class SimulationRequest(BaseModel):
    meal_id: int
    lifestyle_profile: LifestyleProfile


class GlucoseTimepointResponse(BaseModel):
    minutes: int
    glucose_mg_dl: float
    glucose_grams: float
    glucose_percentage_remaining: float


class SimulationResponse(BaseModel):
    id: int
    meal_id: int
    estimated_peak_mg_dl: float
    glucose_grams_baseline: float
    glucose_grams_peak: float
    insulin_load_score: float
    storage_risk_score: float
    glucose_curve: List[GlucoseTimepointResponse]
    explanation: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# ============= Education Schemas =============
class EducationCardCreate(BaseModel):
    title: str
    body: str
    animation_type: Optional[str] = None
    category: Optional[str] = None
    sort_order: int = 0


class EducationCardResponse(BaseModel):
    id: int
    title: str
    body: str
    animation_type: Optional[str] = None
    category: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True


# ============= Food Search Response =============
class FoodSearchResult(BaseModel):
    foods: List[FoodResponse]
    total_results: int
    query: str


# ============= Comparison =============
class FoodComparisonItem(BaseModel):
    food: FoodResponse
    meal_simulation: Optional[SimulationResponse] = None


class ComparisonResponse(BaseModel):
    items: List[FoodComparisonItem]

