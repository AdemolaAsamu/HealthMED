"""
Database initialization and seed data
Creates tables and populates with common foods
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models import Food, EducationCard
from app.schemas import FoodCreate, EducationCardCreate
import app.crud as crud


def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")


def seed_foods():
    """Seed database with common foods"""
    db = SessionLocal()

    # Common foods with estimated nutrition data
    foods_to_add = [
        FoodCreate(
            source="manual",
            source_food_id="apple_medium",
            name="Apple, medium",
            brand=None,
            serving_size_g=182,
            calories=95,
            carbs_g=25,
            sugars_g=19,
            fiber_g=4.4,
            protein_g=0.5,
            fat_g=0.3,
            glycemic_category="medium"
        ),
        FoodCreate(
            source="manual",
            source_food_id="banana_medium",
            name="Banana, medium",
            brand=None,
            serving_size_g=118,
            calories=105,
            carbs_g=27,
            sugars_g=14,
            fiber_g=3.1,
            protein_g=1.3,
            fat_g=0.3,
            glycemic_category="medium"
        ),
        FoodCreate(
            source="manual",
            source_food_id="orange_juice",
            name="Orange juice, 100% unsweetened, 1 cup",
            brand=None,
            serving_size_g=240,
            calories=112,
            carbs_g=26,
            sugars_g=21,
            fiber_g=0.5,
            protein_g=2.0,
            fat_g=0.5,
            glycemic_category="high"
        ),
        FoodCreate(
            source="manual",
            source_food_id="whole_wheat_bread",
            name="Whole wheat bread, 1 slice",
            brand=None,
            serving_size_g=28,
            calories=80,
            carbs_g=14,
            sugars_g=2,
            fiber_g=2.4,
            protein_g=4,
            fat_g=1,
            glycemic_category="medium"
        ),
        FoodCreate(
            source="manual",
            source_food_id="white_bread",
            name="White bread, 1 slice",
            brand=None,
            serving_size_g=28,
            calories=79,
            carbs_g=15,
            sugars_g=2,
            fiber_g=0.9,
            protein_g=2.7,
            fat_g=1,
            glycemic_category="high"
        ),
        FoodCreate(
            source="manual",
            source_food_id="oatmeal",
            name="Oatmeal, cooked, 1 cup",
            brand=None,
            serving_size_g=240,
            calories=150,
            carbs_g=27,
            sugars_g=1,
            fiber_g=4,
            protein_g=5,
            fat_g=3,
            glycemic_category="medium"
        ),
        FoodCreate(
            source="manual",
            source_food_id="brown_rice",
            name="Brown rice, cooked, 1 cup",
            brand=None,
            serving_size_g=195,
            calories=215,
            carbs_g=45,
            sugars_g=1,
            fiber_g=3.5,
            protein_g=5,
            fat_g=2,
            glycemic_category="medium"
        ),
        FoodCreate(
            source="manual",
            source_food_id="white_rice",
            name="White rice, cooked, 1 cup",
            brand=None,
            serving_size_g=195,
            calories=206,
            carbs_g=45,
            sugars_g=0,
            fiber_g=0.6,
            protein_g=4.3,
            fat_g=0.2,
            glycemic_category="high"
        ),
        FoodCreate(
            source="manual",
            source_food_id="broccoli",
            name="Broccoli, chopped, cooked, 1 cup",
            brand=None,
            serving_size_g=156,
            calories=55,
            carbs_g=11,
            sugars_g=2.2,
            fiber_g=2.4,
            protein_g=3.7,
            fat_g=0.6,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="chicken_breast",
            name="Chicken breast, grilled, 3 oz",
            brand=None,
            serving_size_g=85,
            calories=128,
            carbs_g=0,
            sugars_g=0,
            fiber_g=0,
            protein_g=26,
            fat_g=2.7,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="egg",
            name="Egg, large, boiled",
            brand=None,
            serving_size_g=50,
            calories=78,
            carbs_g=0.6,
            sugars_g=0.6,
            fiber_g=0,
            protein_g=6.3,
            fat_g=5.3,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="yogurt_plain",
            name="Yogurt, plain, full-fat, 1 cup",
            brand=None,
            serving_size_g=227,
            calories=180,
            carbs_g=7,
            sugars_g=6,
            fiber_g=0,
            protein_g=10,
            fat_g=10,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="yogurt_sweetened",
            name="Yogurt, sweetened flavored, 1 cup",
            brand=None,
            serving_size_g=227,
            calories=230,
            carbs_g=43,
            sugars_g=33,
            fiber_g=0,
            protein_g=10,
            fat_g=2,
            glycemic_category="high"
        ),
        FoodCreate(
            source="manual",
            source_food_id="milk_whole",
            name="Milk, whole, 1 cup",
            brand=None,
            serving_size_g=244,
            calories=150,
            carbs_g=12,
            sugars_g=12,
            fiber_g=0,
            protein_g=8,
            fat_g=8,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="coke",
            name="Coca-Cola, 12 oz can",
            brand="The Coca-Cola Company",
            serving_size_g=355,
            calories=140,
            carbs_g=39,
            sugars_g=39,
            fiber_g=0,
            protein_g=0,
            fat_g=0,
            glycemic_category="high"
        ),
        FoodCreate(
            source="manual",
            source_food_id="lentil_soup",
            name="Lentil soup, 1 cup",
            brand=None,
            serving_size_g=250,
            calories=140,
            carbs_g=20,
            sugars_g=1,
            fiber_g=8,
            protein_g=9,
            fat_g=1,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="sweet_potato",
            name="Sweet potato, baked, medium",
            brand=None,
            serving_size_g=100,
            calories=103,
            carbs_g=24,
            sugars_g=5,
            fiber_g=3.9,
            protein_g=2.1,
            fat_g=0.1,
            glycemic_category="medium"
        ),
        FoodCreate(
            source="manual",
            source_food_id="mixed_nuts",
            name="Mixed nuts, 1 oz",
            brand=None,
            serving_size_g=28,
            calories=161,
            carbs_g=6,
            sugars_g=1,
            fiber_g=3.5,
            protein_g=5.7,
            fat_g=14,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="avocado",
            name="Avocado, half",
            brand=None,
            serving_size_g=68,
            calories=121,
            carbs_g=6,
            sugars_g=0.3,
            fiber_g=5,
            protein_g=1.5,
            fat_g=11,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="salmon",
            name="Salmon, grilled, 3 oz",
            brand=None,
            serving_size_g=85,
            calories=206,
            carbs_g=0,
            sugars_g=0,
            fiber_g=0,
            protein_g=22,
            fat_g=12,
            glycemic_category="low"
        ),
        FoodCreate(
            source="manual",
            source_food_id="pasta_white",
            name="Pasta, white, cooked, 1 cup",
            brand=None,
            serving_size_g=160,
            calories=220,
            carbs_g=43,
            sugars_g=0.8,
            fiber_g=2.7,
            protein_g=8,
            fat_g=1.1,
            glycemic_category="high"
        ),
        FoodCreate(
            source="manual",
            source_food_id="pasta_whole_wheat",
            name="Pasta, whole wheat, cooked, 1 cup",
            brand=None,
            serving_size_g=160,
            calories=174,
            carbs_g=37,
            sugars_g=0.6,
            fiber_g=6.3,
            protein_g=7.5,
            fat_g=0.8,
            glycemic_category="medium"
        ),
    ]

    for food_data in foods_to_add:
        existing = crud.get_food_by_source_id(db, food_data.source, food_data.source_food_id)
        if not existing:
            crud.create_food(db, food_data)
            print(f"✓ Added food: {food_data.name}")
        else:
            print(f"✓ Food already exists: {food_data.name}")

    db.close()


def seed_education_cards():
    """Seed database with educational content"""
    db = SessionLocal()

    education_cards = [
        EducationCardCreate(
            title="Why 1 Teaspoon Matters",
            body="Your blood contains only about 4-5 grams of glucose, roughly 1 teaspoon of sugar at any given moment. "
                 "Yet a typical meal might contain 30-100+ grams of carbohydrates. Your body works hard to keep blood glucose "
                 "in this narrow range through insulin secretion and glucose storage. Understanding this contrast helps explain "
                 "why meal composition matters so much.",
            animation_type="bloodstream",
            category="basic",
            sort_order=1
        ),
        EducationCardCreate(
            title="Carbohydrates → Glucose",
            body="When you eat carbohydrates, your digestive system breaks them down into glucose molecules. "
                 "This glucose enters your bloodstream. Your body then signals the pancreas to release insulin, "
                 "which acts like a 'key' that lets glucose leave the blood and enter cells for energy, storage, or conversion to fat.",
            animation_type="glucose_spike",
            category="basic",
            sort_order=2
        ),
        EducationCardCreate(
            title="Fiber Slows Absorption",
            body="Fiber is indigestible carbohydrate that slows the breakdown and absorption of other carbohydrates. "
                 "When you eat high-fiber foods, glucose enters your bloodstream more gradually, leading to a gentler rise in blood sugar "
                 "and a lower insulin demand. Example: whole orange vs orange juice.",
            animation_type="glucose_curve",
            category="basic",
            sort_order=3
        ),
        EducationCardCreate(
            title="Protein and Fat Slow Rising",
            body="Protein and fat delay gastric emptying, meaning food stays in your stomach longer before entering the small intestine. "
                 "This slows glucose absorption, resulting in a lower and later peak in blood glucose. A meal with protein and fat "
                 "causes a gentler glucose curve than the same carbs eaten alone.",
            animation_type="glucose_spike",
            category="basic",
            sort_order=4
        ),
        EducationCardCreate(
            title="Glucose Storage Pathways",
            body="Once glucose enters cells, it can follow three main pathways: (1) Immediate energy - muscles and brain use it right away. "
                 "(2) Glycogen storage - muscles and liver store excess glucose as glycogen for short-term energy. "
                 "(3) Fat storage - when glycogen tanks are full and excess remains, insulin signals cells to convert glucose to triglycerides and store as fat.",
            animation_type="glucose_distribution",
            category="basic",
            sort_order=5
        ),
        EducationCardCreate(
            title="Walking After Meals Helps",
            body="Movement immediately after eating is one of the most powerful tools to reduce blood glucose spikes. "
                 "Active muscles pull glucose from the blood without needing much insulin. A 10-15 minute walk after a meal can reduce peak glucose by 20-30% "
                 "and improve overall glucose handling. Even light activity beats sitting.",
            animation_type="post_meal_activity",
            category="basic",
            sort_order=6
        ),
        EducationCardCreate(
            title="Insulin Resistance Explained",
            body="Over time, if cells are constantly exposed to high insulin levels (from repeated high-carb/low-fiber meals and inactivity), "
                 "they can become less responsive to insulin - a condition called insulin resistance. When this happens, the pancreas has to produce even more insulin. "
                 "Prediabetes and Type 2 diabetes develop when this system breaks down.",
            animation_type="insulin_resistance",
            category="advanced",
            sort_order=7
        ),
        EducationCardCreate(
            title="Sleep Affects Glucose Control",
            body="Poor sleep increases insulin resistance and makes blood glucose spikes larger. When you're sleep-deprived, "
                 "your body becomes less sensitive to insulin and more likely to store excess energy as fat. Prioritizing 7-9 hours of quality sleep "
                 "significantly improves glucose management and metabolic health.",
            animation_type="lifestyle",
            category="advanced",
            sort_order=8
        ),
        EducationCardCreate(
            title="Repeated Excess Can Lead to Fatty Liver",
            body="When glucose spikes are frequent and high (especially from refined carbs with low fiber), and the meal energy exceeds your expenditure, "
                 "the excess glucose can be converted to fat stored in liver cells. Over time, this contributes to fatty liver disease. "
                 "Regular physical activity and whole-food, high-fiber carbs reduce this risk significantly.",
            animation_type="health_risks",
            category="advanced",
            sort_order=9
        ),
        EducationCardCreate(
            title="Metabolic Health is About Patterns",
            body="One meal doesn't cause disease. Metabolic health is about patterns. If most of your meals spike blood glucose high, "
                 "are low in fiber, sedentary followed, and combined with poor sleep, the cumulative effect increases risk for weight gain, "
                 "metabolic dysfunction, and chronic disease. Conversely, consistent good habits compound in your favor.",
            animation_type="longterm",
            category="advanced",
            sort_order=10
        ),
        EducationCardCreate(
            title="Comparison: Coke vs Apple",
            body="A 12 oz Coke has 39g of sugar and virtually no fiber. An apple has 19g of sugars but 4.4g of fiber. "
                 "The Coke spikes blood glucose rapidly and gives an insulin jolt. The apple's glucose enters gradually due to fiber. "
                 "Both contain similar calories, but the metabolic outcomes are very different.",
            animation_type="comparison",
            category="comparison",
            sort_order=11
        ),
        EducationCardCreate(
            title="Comparison: White vs Whole Wheat Bread",
            body="White bread has minimal fiber and refined carbs → rapid glucose spike. Whole wheat bread has fiber that slows absorption. "
                 "Over time, consistently choosing whole grain significantly reduces glucose stress on your system.",
            animation_type="comparison",
            category="comparison",
            sort_order=12
        ),
        EducationCardCreate(
            title="Comparison: Rice + Protein vs Rice Alone",
            body="White rice alone → fast glucose spike. White rice + grilled chicken → much gentler rise because protein slows digestion. "
                 "Adding vegetables and protein to every meal is a simple habit that improves glucose handling across the day.",
            animation_type="comparison",
            category="comparison",
            sort_order=13
        ),
    ]

    for card_data in education_cards:
        # Check if card already exists
        existing = db.query(EducationCard).filter(
            EducationCard.title == card_data.title
        ).first()

        if not existing:
            crud.create_education_card(db, card_data)
            print(f"✓ Added education card: {card_data.title}")
        else:
            print(f"✓ Card already exists: {card_data.title}")

    db.close()


def main():
    """Run all initialization steps"""
    print("\n🚀 Starting database initialization...\n")
    init_db()
    seed_foods()
    seed_education_cards()
    print("\n✅ Database initialization complete!\n")


if __name__ == "__main__":
    main()

