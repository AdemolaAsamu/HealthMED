"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas


# ============= Food CRUD =============
def get_food(db: Session, food_id: int):
    return db.query(models.Food).filter(models.Food.id == food_id).first()


def get_food_by_source_id(db: Session, source: str, source_food_id: str):
    return db.query(models.Food).filter(
        and_(
            models.Food.source == source,
            models.Food.source_food_id == source_food_id
        )
    ).first()


def search_foods(db: Session, query: str, limit: int = 50):
    return db.query(models.Food).filter(
        models.Food.name.ilike(f"%{query}%")
    ).limit(limit).all()


def create_food(db: Session, food: schemas.FoodCreate):
    db_food = models.Food(
        source=food.source,
        source_food_id=food.source_food_id,
        name=food.name,
        brand=food.brand,
        serving_size_g=food.serving_size_g,
        calories=food.calories,
        carbs_g=food.carbs_g,
        sugars_g=food.sugars_g,
        fiber_g=food.fiber_g,
        protein_g=food.protein_g,
        fat_g=food.fat_g,
        glycemic_category=food.glycemic_category,
        raw_json=food.raw_json
    )
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


def update_food_nutrition(db: Session, db_food: models.Food, food: schemas.FoodCreate):
    db_food.name = food.name or db_food.name
    db_food.brand = food.brand or db_food.brand
    db_food.serving_size_g = food.serving_size_g or db_food.serving_size_g
    db_food.raw_json = food.raw_json or db_food.raw_json

    for field in (
        "calories",
        "carbs_g",
        "sugars_g",
        "fiber_g",
        "protein_g",
        "fat_g",
        "glycemic_category",
    ):
        value = getattr(food, field)
        if value is not None:
            setattr(db_food, field, value)

    db.commit()
    db.refresh(db_food)
    return db_food


# ============= Meal CRUD =============
def create_meal(db: Session, meal: schemas.MealCreate):
    food_by_id = {}
    for item in meal.items:
        food = get_food(db, item.food_id)
        if not food:
            raise ValueError(f"Food not found: {item.food_id}")
        food_by_id[item.food_id] = food

    db_meal = models.Meal(
        user_session_id=meal.user_session_id,
        name=meal.name
    )
    db.add(db_meal)
    db.flush()  # Get the meal ID

    # Add meal items
    for item in meal.items:
        db_item = models.MealItem(
            meal_id=db_meal.id,
            food_id=item.food_id,
            quantity=item.quantity,
            serving_multiplier=item.serving_multiplier
        )
        # Calculate nutrition based on food and multipliers
        food = food_by_id[item.food_id]
        multiplier = item.quantity * item.serving_multiplier
        db_item.carbs_g = food.carbs_g * multiplier if food.carbs_g is not None else None
        db_item.sugars_g = food.sugars_g * multiplier if food.sugars_g is not None else None
        db_item.calories = food.calories * multiplier if food.calories is not None else None
        db.add(db_item)

    db.commit()
    db.refresh(db_meal)
    return db_meal


def get_meal(db: Session, meal_id: int):
    return db.query(models.Meal).filter(models.Meal.id == meal_id).first()


def get_user_meals(db: Session, user_session_id: str, limit: int = 50):
    return db.query(models.Meal).filter(
        models.Meal.user_session_id == user_session_id
    ).order_by(models.Meal.created_at.desc()).limit(limit).all()


def delete_meal(db: Session, meal_id: int):
    meal = get_meal(db, meal_id)
    if meal:
        db.delete(meal)
        db.commit()
    return meal


# ============= Meal Item CRUD =============
def add_meal_item(db: Session, meal_id: int, item: schemas.MealItemCreate):
    food = get_food(db, item.food_id)
    if not food:
        return None

    db_item = models.MealItem(
        meal_id=meal_id,
        food_id=item.food_id,
        quantity=item.quantity,
        serving_multiplier=item.serving_multiplier
    )

    # Calculate nutrition
    multiplier = item.quantity * item.serving_multiplier
    db_item.carbs_g = food.carbs_g * multiplier if food.carbs_g is not None else None
    db_item.sugars_g = food.sugars_g * multiplier if food.sugars_g is not None else None
    db_item.calories = food.calories * multiplier if food.calories is not None else None

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def remove_meal_item(db: Session, meal_id: int, meal_item_id: int):
    item = db.query(models.MealItem).filter(
        models.MealItem.id == meal_item_id,
        models.MealItem.meal_id == meal_id
    ).first()
    if item:
        db.delete(item)
        db.commit()
    return item


# ============= Simulation CRUD =============
def create_simulation(db: Session, simulation: models.Simulation):
    db.add(simulation)
    db.commit()
    db.refresh(simulation)
    return simulation


def get_simulation(db: Session, simulation_id: int):
    return db.query(models.Simulation).filter(
        models.Simulation.id == simulation_id
    ).first()


def get_meal_simulations(db: Session, meal_id: int):
    return db.query(models.Simulation).filter(
        models.Simulation.meal_id == meal_id
    ).order_by(models.Simulation.created_at.desc()).all()


# ============= Education CRUD =============
def get_all_education_cards(db: Session):
    return db.query(models.EducationCard)\
        .order_by(models.EducationCard.sort_order)\
        .all()


def get_education_cards_by_category(db: Session, category: str):
    return db.query(models.EducationCard)\
        .filter(models.EducationCard.category == category)\
        .order_by(models.EducationCard.sort_order)\
        .all()


def create_education_card(db: Session, card: schemas.EducationCardCreate):
    db_card = models.EducationCard(
        title=card.title,
        body=card.body,
        animation_type=card.animation_type,
        category=card.category,
        sort_order=card.sort_order
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_education_card(db: Session, card_id: int, card: schemas.EducationCardCreate):
    db_card = db.query(models.EducationCard).filter(
        models.EducationCard.id == card_id
    ).first()
    if db_card:
        db_card.title = card.title
        db_card.body = card.body
        db_card.animation_type = card.animation_type
        db_card.category = card.category
        db_card.sort_order = card.sort_order
        db.commit()
        db.refresh(db_card)
    return db_card


def delete_education_card(db: Session, card_id: int):
    card = db.query(models.EducationCard).filter(
        models.EducationCard.id == card_id
    ).first()
    if card:
        db.delete(card)
        db.commit()
    return card

