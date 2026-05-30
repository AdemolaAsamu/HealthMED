"""
Food search and management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.services.food_api_service import FoodAPIService

router = APIRouter(prefix="/api/foods", tags=["foods"])


@router.get("/search", response_model=schemas.FoodSearchResult)
async def search_foods(
    query: str = Query(..., min_length=1, max_length=200),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search for foods from local cache and external APIs.
    Results are automatically cached in the database.
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    foods = await FoodAPIService.search_foods(db, query, limit=limit)

    return schemas.FoodSearchResult(
        foods=foods,
        total_results=len(foods),
        query=query
    )


@router.get("/{food_id}", response_model=schemas.FoodResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    """Get a specific food by ID"""
    food = crud.get_food(db, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return schemas.FoodResponse.model_validate(food)


@router.post("/manual", response_model=schemas.FoodResponse)
def create_food_manual(
    food: schemas.FoodCreate,
    db: Session = Depends(get_db)
):
    """
    Manually add a food to the database.
    Useful when API data is missing or incomplete.
    """
    # Check if already exists
    existing = crud.get_food_by_source_id(db, food.source, food.source_food_id)
    if existing:
        return schemas.FoodResponse.model_validate(existing)

    created_food = crud.create_food(db, food)
    return schemas.FoodResponse.model_validate(created_food)

