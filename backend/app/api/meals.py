"""
Meal analysis API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.services.glucose_simulator import GlucoseSimulator

router = APIRouter(prefix="/api/meals", tags=["meals"])


@router.post("/", response_model=schemas.MealResponse)
def create_meal(
    meal: schemas.MealCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new meal with multiple food items.
    Returns the meal with calculated nutrition totals.
    """
    if not meal.items:
        raise HTTPException(status_code=400, detail="Meal must contain at least one food item")

    try:
        created_meal = crud.create_meal(db, meal)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return schemas.MealResponse.model_validate(created_meal)


@router.get("/{meal_id}", response_model=schemas.MealResponse)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    """Get a specific meal by ID"""
    meal = crud.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return schemas.MealResponse.model_validate(meal)


@router.get("/user/{user_session_id}", response_model=list[schemas.MealResponse])
def get_user_meals(
    user_session_id: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all meals for a user session"""
    meals = crud.get_user_meals(db, user_session_id, limit=limit)
    return [schemas.MealResponse.model_validate(m) for m in meals]


@router.post("/{meal_id}/items", response_model=schemas.MealItemResponse)
def add_meal_item(
    meal_id: int,
    item: schemas.MealItemCreate,
    db: Session = Depends(get_db)
):
    """Add food item to an existing meal"""
    meal = crud.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    food = crud.get_food(db, item.food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    meal_item = crud.add_meal_item(db, meal_id, item)
    return schemas.MealItemResponse.model_validate(meal_item)


@router.delete("/{meal_id}/items/{item_id}")
def remove_meal_item(
    meal_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove food item from meal"""
    meal = crud.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    item = crud.remove_meal_item(db, meal_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Meal item not found")

    return {"status": "success", "message": "Item removed from meal"}


@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    """Delete a meal"""
    meal = crud.delete_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"status": "success", "message": "Meal deleted"}


@router.get("/{meal_id}/summary", response_model=schemas.MealSummary)
def get_meal_summary(meal_id: int, db: Session = Depends(get_db)):
    """Get nutrition summary for a meal"""
    meal = crud.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    meal_items_data = []
    for item in meal.meal_items:
        multiplier = item.quantity * item.serving_multiplier
        meal_items_data.append({
            "calories": item.calories or 0,
            "carbs_g": item.carbs_g or 0,
            "sugars_g": item.sugars_g or 0,
            "fiber_g": ((item.food.fiber_g or 0) * multiplier) if item.food else 0,
            "protein_g": ((item.food.protein_g or 0) * multiplier) if item.food else 0,
            "fat_g": ((item.food.fat_g or 0) * multiplier) if item.food else 0,
        })

    return GlucoseSimulator.calculate_meal_summary(meal_items_data)

