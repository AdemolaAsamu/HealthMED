# API Documentation

## Base URL

```
http://localhost:8000
```

## Interactive API Explorer

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Health & General Endpoints

### Health Check
```
GET /health
```

Returns server health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Get Disclaimers
```
GET /api/disclaimers
```

Returns all legal and medical disclaimers.

**Response:**
```json
{
  "primary_disclaimer": "...",
  "glucose_response": "...",
  "cgm_recommendation": "...",
  "medical_conditions": ["..."],
  "limitations": ["..."]
}
```

## Food API

### Search Foods
```
GET /api/foods/search?query=apple&limit=20
```

Search for foods from local cache and external APIs (USDA, Open Food Facts).

**Query Parameters:**
- `query` (required, string, 1-200 chars): Food name
- `limit` (optional, integer, 1-100): Max results (default: 20)

**Response:**
```json
{
  "foods": [
    {
      "id": 1,
      "source": "usda",
      "source_food_id": "123456",
      "name": "Apple, medium",
      "brand": null,
      "serving_size_g": 182,
      "calories": 95,
      "carbs_g": 25,
      "sugars_g": 19,
      "fiber_g": 4.4,
      "protein_g": 0.5,
      "fat_g": 0.3,
      "glycemic_category": "medium",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total_results": 1,
  "query": "apple"
}
```

### Get Food by ID
```
GET /api/foods/{food_id}
```

Get detailed information about a specific food.

**Response:** Same as individual food object from search

### Manually Add Food
```
POST /api/foods/manual
```

Manually add a food to the database (useful when API data is incomplete).

**Request Body:**
```json
{
  "source": "manual",
  "source_food_id": "manual_apple_2024",
  "name": "Apple, medium",
  "brand": null,
  "serving_size_g": 182,
  "calories": 95,
  "carbs_g": 25,
  "sugars_g": 19,
  "fiber_g": 4.4,
  "protein_g": 0.5,
  "fat_g": 0.3,
  "glycemic_category": "medium"
}
```

## Meal API

### Create Meal
```
POST /api/meals/
```

Create a new meal with multiple food items.

**Request Body:**
```json
{
  "user_session_id": "user_123",
  "name": "Breakfast",
  "items": [
    {
      "food_id": 1,
      "quantity": 1,
      "serving_multiplier": 1.0
    },
    {
      "food_id": 2,
      "quantity": 1,
      "serving_multiplier": 1.5
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_session_id": "user_123",
  "name": "Breakfast",
  "created_at": "2024-01-01T00:00:00",
  "meal_items": [...]
}
```

### Get Meal
```
GET /api/meals/{meal_id}
```

Get a specific meal with all items.

**Response:** Full meal object with meal_items array

### Get User Meals
```
GET /api/meals/user/{user_session_id}?limit=50
```

Get all meals for a user session.

**Query Parameters:**
- `limit` (optional, 1-100): Max meals to return

**Response:**
```json
[
  {
    "id": 1,
    "user_session_id": "user_123",
    "name": "Breakfast",
    "created_at": "2024-01-01T00:00:00",
    "meal_items": [...]
  }
]
```

### Add Item to Meal
```
POST /api/meals/{meal_id}/items
```

Add a food item to an existing meal.

**Request Body:**
```json
{
  "food_id": 3,
  "quantity": 1,
  "serving_multiplier": 1.0
}
```

### Remove Item from Meal
```
DELETE /api/meals/{meal_id}/items/{item_id}
```

Remove a food item from a meal.

### Delete Meal
```
DELETE /api/meals/{meal_id}
```

Delete an entire meal.

### Get Meal Summary
```
GET /api/meals/{meal_id}/summary
```

Get nutrition totals for a meal.

**Response:**
```json
{
  "total_calories": 450,
  "total_carbs_g": 60,
  "total_sugars_g": 25,
  "total_fiber_g": 8,
  "total_protein_g": 20,
  "total_fat_g": 15,
  "net_carbs_g": 52,
  "estimated_glycemic_load": 26
}
```

## Simulation API

### Create Simulation
```
POST /api/simulations/
```

Run glucose simulation for a meal with lifestyle modifiers.

**Request Body:**
```json
{
  "meal_id": 1,
  "lifestyle_profile": {
    "is_sedentary": true,
    "post_meal_walk_minutes": 0,
    "regular_exercise": false,
    "exercise_intensity": null,
    "poor_sleep": false,
    "high_stress": false,
    "high_muscle_mass": false,
    "insulin_resistant": false,
    "prediabetic": false,
    "high_fiber_meal": false,
    "protein_first": false
  }
}
```

**Response:**
```json
{
  "id": 1,
  "meal_id": 1,
  "estimated_peak_mg_dl": 145.5,
  "glucose_grams_baseline": 4.5,
  "glucose_grams_peak": 7.25,
  "insulin_load_score": 45.2,
  "storage_risk_score": 35.8,
  "glucose_curve": [
    {
      "minutes": 0,
      "glucose_mg_dl": 90,
      "glucose_grams": 4.5,
      "glucose_percentage_remaining": 100
    },
    {
      "minutes": 30,
      "glucose_mg_dl": 145.5,
      "glucose_grams": 7.25,
      "glucose_percentage_remaining": 161.1
    }
  ],
  "explanation": {
    "summary": "...",
    "factors": ["..."],
    "recommendations": ["..."],
    "risks": ["..."],
    "disclaimer": "..."
  },
  "created_at": "2024-01-01T00:00:00"
}
```

### Get Simulation
```
GET /api/simulations/{simulation_id}
```

Get a specific simulation result.

### Get Meal Simulations
```
GET /api/simulations/meal/{meal_id}
```

Get all simulations for a meal.

**Response:** Array of simulation objects

### Compare Meals
```
POST /api/simulations/compare
```

Compare glucose responses of multiple meals.

**Request Body:**
```json
{
  "meal_ids": [1, 2, 3],
  "lifestyle": {
    "is_sedentary": true,
    "post_meal_walk_minutes": 0,
    "regular_exercise": false,
    "poor_sleep": false,
    "high_stress": false,
    "high_muscle_mass": false,
    "insulin_resistant": false,
    "prediabetic": false,
    "high_fiber_meal": false,
    "protein_first": false
  }
}
```

**Response:**
```json
{
  "comparisons": [
    {
      "meal_id": 1,
      "meal_name": "Meal 1",
      "peak_mg_dl": 145.5,
      "insulin_load_score": 45.2,
      "storage_risk_score": 35.8,
      "meal_summary": {...}
    }
  ],
  "lifestyle_profile": {...},
  "best_option": {...}
}
```

## Education API

### Get All Education Cards
```
GET /api/education/cards?category=basic
```

Get educational content cards.

**Query Parameters:**
- `category` (optional): Filter by category (basic, advanced, comparison)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Why 1 Teaspoon Matters",
    "body": "Your blood contains only about 4-5 grams...",
    "animation_type": "bloodstream",
    "category": "basic",
    "sort_order": 1
  }
]
```

### Get Card by ID
```
GET /api/education/cards/{card_id}
```

Get a specific education card.

### Create Education Card (Admin)
```
POST /api/education/cards
```

Create a new education card.

**Request Body:**
```json
{
  "title": "Card Title",
  "body": "Card content...",
  "animation_type": "glucose_spike",
  "category": "basic",
  "sort_order": 1
}
```

### Update Education Card (Admin)
```
PUT /api/education/cards/{card_id}
```

Update an existing education card.

**Request Body:** Same as create

### Delete Education Card (Admin)
```
DELETE /api/education/cards/{card_id}
```

Delete an education card.

## Error Handling

All errors return appropriate HTTP status codes:

- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: API service down

**Error Response Format:**
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

No rate limiting in development. Consider adding in production.

## Authentication

Currently no authentication. Add in future versions for multi-user scenarios.

## Data Types

### LifestyleProfile

```typescript
{
  is_sedentary?: boolean;
  post_meal_walk_minutes?: number;
  regular_exercise?: boolean;
  exercise_intensity?: 'low' | 'moderate' | 'high';
  poor_sleep?: boolean;
  high_stress?: boolean;
  high_muscle_mass?: boolean;
  insulin_resistant?: boolean;
  prediabetic?: boolean;
  high_fiber_meal?: boolean;
  protein_first?: boolean;
}
```

### GlucoseTimepoint

```typescript
{
  minutes: number;
  glucose_mg_dl: number;
  glucose_grams: number;
  glucose_percentage_remaining: number;
}
```

## Example Workflows

### 1. Analyze a Single Food

```bash
# Search for apple
curl http://localhost:8000/api/foods/search?query=apple

# Get apple ID from response (e.g., 1)
# Create meal with apple
curl -X POST http://localhost:8000/api/meals/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_session_id": "user_123",
    "name": "Apple",
    "items": [{"food_id": 1, "quantity": 1, "serving_multiplier": 1.0}]
  }'

# Get meal ID from response (e.g., 5)
# Create simulation
curl -X POST http://localhost:8000/api/simulations/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_id": 5,
    "lifestyle_profile": {
      "is_sedentary": true,
      "post_meal_walk_minutes": 0,
      "regular_exercise": false,
      "poor_sleep": false,
      "high_stress": false,
      "high_muscle_mass": false,
      "insulin_resistant": false,
      "prediabetic": false,
      "high_fiber_meal": false,
      "protein_first": false
    }
  }'

# Get simulation results
```

### 2. Compare Two Meals

```bash
# Create two meals as above (meal IDs: 5, 6)
# Compare them
curl -X POST http://localhost:8000/api/simulations/compare \
  -H "Content-Type: application/json" \
  -d '{
    "meal_ids": [5, 6],
    "lifestyle": {
      "is_sedentary": true,
      "post_meal_walk_minutes": 15,
      "regular_exercise": false,
      "poor_sleep": false,
      "high_stress": false,
      "high_muscle_mass": false,
      "insulin_resistant": false,
      "prediabetic": false,
      "high_fiber_meal": false,
      "protein_first": false
    }
  }'
```

## Testing

Use cURL, Postman, or the interactive docs at `/docs`

## Support

For API issues:
1. Check server logs
2. Verify JSON format
3. Check required fields
4. Review this documentation

