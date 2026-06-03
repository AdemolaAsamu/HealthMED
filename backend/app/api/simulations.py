"""
Glucose simulation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, models
from app.services.glucose_simulator import GlucoseSimulator

router = APIRouter(prefix="/api/simulations", tags=["simulations"])


@router.post("/", response_model=schemas.SimulationResponse)
def create_simulation(
    request: schemas.SimulationRequest,
    db: Session = Depends(get_db)
):
    """
    Create a glucose simulation for a meal with lifestyle modifiers.
    Returns estimated glucose curve, peak glucose, and risk scores.
    """
    # Get meal
    meal = crud.get_meal(db, request.meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    # Calculate meal summary
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

    meal_summary = GlucoseSimulator.calculate_meal_summary(meal_items_data)

    # Run simulation
    simulation_result = GlucoseSimulator.simulate_glucose_response(
        meal_summary,
        request.lifestyle_profile
    )
    explanation = {
        **simulation_result["explanation"],
        "fat_storage_estimate": simulation_result["fat_storage_estimate"],
        "glucose_curve": [
            point.model_dump() for point in simulation_result["glucose_curve"]
        ],
    }

    # Save to database
    db_simulation = models.Simulation(
        meal_id=request.meal_id,
        lifestyle_profile=request.lifestyle_profile.model_dump(),
        estimated_peak_mg_dl=simulation_result["peak_mg_dl"],
        glucose_grams_baseline=simulation_result["baseline_glucose_grams"],
        glucose_grams_peak=simulation_result["peak_glucose_grams"],
        insulin_load_score=simulation_result["insulin_load_score"],
        storage_risk_score=simulation_result["storage_risk_score"],
        explanation_json=explanation
    )

    saved_simulation = crud.create_simulation(db, db_simulation)

    # Convert glucose curve to response format
    glucose_curve = [
        schemas.GlucoseTimepointResponse.model_validate(point)
        for point in simulation_result["glucose_curve"]
    ]

    return schemas.SimulationResponse(
        id=saved_simulation.id,
        meal_id=saved_simulation.meal_id,
        estimated_peak_mg_dl=saved_simulation.estimated_peak_mg_dl,
        glucose_grams_baseline=saved_simulation.glucose_grams_baseline,
        glucose_grams_peak=saved_simulation.glucose_grams_peak,
        insulin_load_score=saved_simulation.insulin_load_score,
        storage_risk_score=saved_simulation.storage_risk_score,
        glucose_curve=glucose_curve,
        fat_storage_estimate=schemas.FatStorageEstimate.model_validate(
            simulation_result["fat_storage_estimate"]
        ),
        explanation=saved_simulation.explanation_json,
        created_at=saved_simulation.created_at
    )


@router.get("/{simulation_id}", response_model=schemas.SimulationResponse)
def get_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Get a specific simulation by ID"""
    simulation = crud.get_simulation(db, simulation_id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Reconstruct glucose curve from timepoints
    # In a real implementation, you'd store individual timepoints separately
    explanation = simulation.explanation_json or {}
    glucose_curve = [
        schemas.GlucoseTimepointResponse.model_validate(point)
        for point in explanation.get("glucose_curve", [])
    ]

    return schemas.SimulationResponse(
        id=simulation.id,
        meal_id=simulation.meal_id,
        estimated_peak_mg_dl=simulation.estimated_peak_mg_dl,
        glucose_grams_baseline=simulation.glucose_grams_baseline,
        glucose_grams_peak=simulation.glucose_grams_peak,
        insulin_load_score=simulation.insulin_load_score,
        storage_risk_score=simulation.storage_risk_score,
        glucose_curve=glucose_curve,
        fat_storage_estimate=schemas.FatStorageEstimate.model_validate(
            explanation.get("fat_storage_estimate", {
                "estimated_energy_surplus_kcal": 0,
                "potential_fat_storage_g_low": 0,
                "potential_fat_storage_g_high": 0,
                "storage_efficiency_percent": 0,
                "activity_offset_kcal": 0,
                "assumption": "Estimate unavailable for older simulations."
            })
        ),
        explanation=explanation,
        created_at=simulation.created_at
    )


@router.get("/meal/{meal_id}", response_model=list[schemas.SimulationResponse])
def get_meal_simulations(meal_id: int, db: Session = Depends(get_db)):
    """Get all simulations for a meal"""
    meal = crud.get_meal(db, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    simulations = crud.get_meal_simulations(db, meal_id)

    results = []
    for simulation in simulations:
        glucose_curve = []
        # Try to extract glucose_curve if stored in explanation
        if simulation.explanation_json and "glucose_curve" in simulation.explanation_json:
            for point in simulation.explanation_json["glucose_curve"]:
                glucose_curve.append(
                    schemas.GlucoseTimepointResponse.model_validate(point)
                )

        results.append(
            schemas.SimulationResponse(
                id=simulation.id,
                meal_id=simulation.meal_id,
                estimated_peak_mg_dl=simulation.estimated_peak_mg_dl,
                glucose_grams_baseline=simulation.glucose_grams_baseline,
                glucose_grams_peak=simulation.glucose_grams_peak,
                insulin_load_score=simulation.insulin_load_score,
                storage_risk_score=simulation.storage_risk_score,
                glucose_curve=glucose_curve,
                fat_storage_estimate=schemas.FatStorageEstimate.model_validate(
                    simulation.explanation_json.get("fat_storage_estimate", {
                        "estimated_energy_surplus_kcal": 0,
                        "potential_fat_storage_g_low": 0,
                        "potential_fat_storage_g_high": 0,
                        "storage_efficiency_percent": 0,
                        "activity_offset_kcal": 0,
                        "assumption": "Estimate unavailable for older simulations."
                    }) if simulation.explanation_json else {
                        "estimated_energy_surplus_kcal": 0,
                        "potential_fat_storage_g_low": 0,
                        "potential_fat_storage_g_high": 0,
                        "storage_efficiency_percent": 0,
                        "activity_offset_kcal": 0,
                        "assumption": "Estimate unavailable for older simulations."
                    }
                ),
                explanation=simulation.explanation_json,
                created_at=simulation.created_at
            )
        )

    return results


@router.post("/compare")
def compare_meals(
    meal_ids: list[int],
    lifestyle: schemas.LifestyleProfile,
    db: Session = Depends(get_db)
):
    """
    Compare glucose responses across multiple meals with same lifestyle.
    Returns comparison data for side-by-side visualization.
    """
    if not meal_ids or len(meal_ids) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 meals to compare")

    comparisons = []
    for meal_id in meal_ids:
        meal = crud.get_meal(db, meal_id)
        if not meal:
            continue

        # Calculate meal summary
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

        meal_summary = GlucoseSimulator.calculate_meal_summary(meal_items_data)

        # Simulate
        simulation_result = GlucoseSimulator.simulate_glucose_response(
            meal_summary,
            lifestyle
        )

        comparisons.append({
            "meal_id": meal_id,
            "meal_name": meal.name or f"Meal {meal_id}",
            "peak_mg_dl": simulation_result["peak_mg_dl"],
            "insulin_load_score": simulation_result["insulin_load_score"],
            "storage_risk_score": simulation_result["storage_risk_score"],
            "meal_summary": meal_summary.model_dump()
        })

    return {
        "comparisons": comparisons,
        "lifestyle_profile": lifestyle.model_dump(),
        "best_option": min(comparisons, key=lambda x: x["peak_mg_dl"]) if comparisons else None
    }

