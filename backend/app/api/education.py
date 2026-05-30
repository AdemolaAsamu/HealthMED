"""
Educational content API endpoints
"""
import os
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/education", tags=["education"])


def verify_admin_key(x_admin_key: Optional[str] = Header(default=None)):
    """Require X-Admin-Key for content mutations when ADMIN_API_KEY is configured."""
    expected_key = os.getenv("ADMIN_API_KEY")
    if expected_key and x_admin_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid admin key")


@router.get("/cards", response_model=list[schemas.EducationCardResponse])
def get_education_cards(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all educational cards, optionally filtered by category.
    Categories: 'basic', 'advanced', 'comparison'
    """
    if category:
        cards = crud.get_education_cards_by_category(db, category)
    else:
        cards = crud.get_all_education_cards(db)

    return [schemas.EducationCardResponse.model_validate(c) for c in cards]


@router.get("/cards/{card_id}", response_model=schemas.EducationCardResponse)
def get_education_card(card_id: int, db: Session = Depends(get_db)):
    """Get a specific education card by ID"""
    card = db.query(crud.models.EducationCard).filter(
        crud.models.EducationCard.id == card_id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    return schemas.EducationCardResponse.model_validate(card)


@router.post("/cards", response_model=schemas.EducationCardResponse)
def create_education_card(
    card: schemas.EducationCardCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_key)
):
    """Create a new education card (Admin)"""
    created_card = crud.create_education_card(db, card)
    return schemas.EducationCardResponse.model_validate(created_card)


@router.put("/cards/{card_id}", response_model=schemas.EducationCardResponse)
def update_education_card(
    card_id: int,
    card: schemas.EducationCardCreate,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_key)
):
    """Update an education card (Admin)"""
    updated_card = crud.update_education_card(db, card_id, card)
    if not updated_card:
        raise HTTPException(status_code=404, detail="Card not found")

    return schemas.EducationCardResponse.model_validate(updated_card)


@router.delete("/cards/{card_id}")
def delete_education_card(
    card_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_key)
):
    """Delete an education card (Admin)"""
    card = crud.delete_education_card(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    return {"status": "success", "message": "Card deleted"}

