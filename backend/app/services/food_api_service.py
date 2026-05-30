"""
Food API service - Integration with external food databases
Integrates with USDA FoodData Central and Open Food Facts APIs
"""
import os
import httpx
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app import crud, schemas


class FoodAPIService:
    """Service for fetching and caching food data from external APIs"""

    USDA_API_KEY = os.getenv("USDA_API_KEY", "DEMO_KEY")
    USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"
    OPENFOODFACTS_BASE_URL = "https://world.openfoodfacts.org/api/v0"

    @staticmethod
    async def search_usda_foods(query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search USDA FoodData Central for foods
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                params = {
                    "query": query,
                    "api_key": FoodAPIService.USDA_API_KEY,
                    "pageSize": limit
                }
                response = await client.get(
                    f"{FoodAPIService.USDA_BASE_URL}/foods/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                return data.get("foods", [])
        except Exception as e:
            print(f"Error searching USDA: {e}")
            return []

    @staticmethod
    async def search_openfoodfacts(query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search Open Food Facts for foods
        Useful for packaged foods and barcodes
        """
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                params = {
                    "search_terms": query,
                    "json": 1,
                    "page_size": limit
                }
                response = await client.get(
                    f"{FoodAPIService.OPENFOODFACTS_BASE_URL}/search",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                return data.get("products", [])
        except Exception as e:
            print(f"Error searching Open Food Facts: {e}")
            return []

    @staticmethod
    def extract_nutrition_from_usda(food_data: Dict[str, Any]) -> Optional[schemas.FoodCreate]:
        """
        Extract nutrition data from USDA response
        """
        try:
            fdc_id = str(food_data.get("fdcId"))
            description = food_data.get("description", "")

            # Find nutrition data
            nutrients_dict = {}
            nutrients = food_data.get("foodNutrients", [])

            for nutrient in nutrients:
                nutrient_name = nutrient.get("nutrientName", "").lower()
                value = nutrient.get("value", 0)

                if "energy" in nutrient_name and ("kcal" in nutrient_name or nutrient.get("unitName", "").lower() == "kcal"):
                    nutrients_dict["calories"] = value
                elif "carbohydrate" in nutrient_name and "total" in nutrient_name and "sugar" not in nutrient_name:
                    nutrients_dict["carbs_g"] = value
                elif "sugars" in nutrient_name and "total" in nutrient_name:
                    nutrients_dict["sugars_g"] = value
                elif "fiber" in nutrient_name and "total" in nutrient_name:
                    nutrients_dict["fiber_g"] = value
                elif "protein" in nutrient_name:
                    nutrients_dict["protein_g"] = value
                elif "fat" in nutrient_name and "total" in nutrient_name:
                    nutrients_dict["fat_g"] = value

            serving_size = food_data.get("servingSize", 100) or 100
            serving_unit = food_data.get("servingSizeUnit", "g")

            if serving_unit.lower() != "g":
                # Try to convert other units to grams
                serving_size = 100  # Default fallback

            return schemas.FoodCreate(
                source="usda",
                source_food_id=fdc_id,
                name=description,
                brand=None,
                serving_size_g=serving_size,
                calories=nutrients_dict.get("calories"),
                carbs_g=nutrients_dict.get("carbs_g"),
                sugars_g=nutrients_dict.get("sugars_g"),
                fiber_g=nutrients_dict.get("fiber_g"),
                protein_g=nutrients_dict.get("protein_g"),
                fat_g=nutrients_dict.get("fat_g"),
                glycemic_category=None,
                raw_json=food_data
            )
        except Exception as e:
            print(f"Error extracting USDA nutrition: {e}")
            return None

    @staticmethod
    def extract_nutrition_from_openfoodfacts(food_data: Dict[str, Any]) -> Optional[schemas.FoodCreate]:
        """
        Extract nutrition data from Open Food Facts response
        """
        try:
            ean = str(food_data.get("ean_tags", ["unknown"])[0]) if food_data.get("ean_tags") else str(food_data.get("code", "unknown"))
            name = food_data.get("product_name", "")
            brand = food_data.get("brands", "")

            # Nutrition data per 100g or per serving
            nutrition = food_data.get("nutrition_data_per_100g", {})
            if not nutrition:
                nutrition = food_data.get("nutriments", {})

            serving_size = food_data.get("serving_quantity", 100) or 100
            serving_unit = food_data.get("serving_quantity_unit", "g")

            if serving_unit.lower() != "g":
                serving_size = 100  # Default fallback

            return schemas.FoodCreate(
                source="openfoodfacts",
                source_food_id=ean,
                name=name,
                brand=brand,
                serving_size_g=serving_size,
                calories=nutrition.get("energy-kcal") or nutrition.get("energy_kcal"),
                carbs_g=nutrition.get("carbohydrates") or nutrition.get("carbohydrates_100g"),
                sugars_g=nutrition.get("sugars") or nutrition.get("sugars_100g"),
                fiber_g=nutrition.get("fiber") or nutrition.get("fiber_100g"),
                protein_g=nutrition.get("proteins") or nutrition.get("proteins_100g"),
                fat_g=nutrition.get("fat") or nutrition.get("fat_100g"),
                glycemic_category=None,
                raw_json=food_data
            )
        except Exception as e:
            print(f"Error extracting Open Food Facts nutrition: {e}")
            return None

    @staticmethod
    async def search_foods(
        db: Session,
        query: str,
        limit: int = 20,
        use_cache: bool = True
    ) -> List[schemas.FoodResponse]:
        """
        Search for foods from multiple sources
        1. Check local cache first
        2. Query USDA
        3. Query Open Food Facts
        4. Cache new results
        """

        results = []

        # 1. Check local cache
        cached_foods = crud.search_foods(db, query, limit=limit)
        results.extend([schemas.FoodResponse.model_validate(f) for f in cached_foods])

        if len(results) >= limit:
            return results[:limit]

        # 2. Search USDA
        usda_foods = await FoodAPIService.search_usda_foods(query, limit=limit)
        for food_data in usda_foods[:limit - len(results)]:
            parsed_food = FoodAPIService.extract_nutrition_from_usda(food_data)
            if parsed_food:
                # Check if already in cache
                existing = crud.get_food_by_source_id(db, parsed_food.source, parsed_food.source_food_id)
                if not existing:
                    existing = crud.create_food(db, parsed_food)
                results.append(schemas.FoodResponse.model_validate(existing))

        if len(results) >= limit:
            return results[:limit]

        # 3. Search Open Food Facts
        openfoodfacts_foods = await FoodAPIService.search_openfoodfacts(query, limit=limit)
        for food_data in openfoodfacts_foods[:limit - len(results)]:
            parsed_food = FoodAPIService.extract_nutrition_from_openfoodfacts(food_data)
            if parsed_food:
                existing = crud.get_food_by_source_id(db, parsed_food.source, parsed_food.source_food_id)
                if not existing:
                    existing = crud.create_food(db, parsed_food)
                results.append(schemas.FoodResponse.model_validate(existing))

        return results[:limit]

