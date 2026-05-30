"""
Glucose simulation service - Educational model for glucose dynamics
This is NOT medical/diagnostic. It's for educational visualization.
"""
from typing import List, Dict, Any
from app.schemas import LifestyleProfile, MealSummary
from app.schemas import GlucoseTimepointResponse


class GlucoseSimulator:
    """
    Educational simulator for glucose dynamics and metabolic response.
    Uses simplified model for visualization purposes.
    """

    # Constants
    BASELINE_GLUCOSE_MG_DL = 90
    BASELINE_GLUCOSE_GRAMS = 4.5
    BLOOD_VOLUME_DL = 50  # 5 liters

    # Timepoint intervals (minutes)
    TIMEPOINTS = [0, 15, 30, 45, 60, 90, 120]

    @staticmethod
    def estimate_glycemic_index(carbs_g: float, sugars_g: float, fiber_g: float) -> str:
        """
        Estimate glycemic category based on nutrition data
        Categories: 'low', 'medium', 'high'
        """
        if carbs_g == 0:
            return 'low'

        sugar_ratio = sugars_g / carbs_g if sugars_g else 0
        fiber_ratio = fiber_g / carbs_g if fiber_g else 0

        # High fiber, low sugar = low GI
        if fiber_ratio > 0.15 and sugar_ratio < 0.2:
            return 'low'
        # High sugar, low fiber = high GI
        elif sugar_ratio > 0.5 and fiber_ratio < 0.05:
            return 'high'
        else:
            return 'medium'

    @staticmethod
    def calculate_meal_summary(meal_items: List[Dict[str, float]]) -> MealSummary:
        """
        Calculate total nutrition from meal items
        Each item should have: calories, carbs_g, sugars_g, fiber_g, protein_g, fat_g
        """
        total_calories = sum(item.get('calories', 0) or 0 for item in meal_items)
        total_carbs_g = sum(item.get('carbs_g', 0) or 0 for item in meal_items)
        total_sugars_g = sum(item.get('sugars_g', 0) or 0 for item in meal_items)
        total_fiber_g = sum(item.get('fiber_g', 0) or 0 for item in meal_items)
        total_protein_g = sum(item.get('protein_g', 0) or 0 for item in meal_items)
        total_fat_g = sum(item.get('fat_g', 0) or 0 for item in meal_items)

        net_carbs_g = max(0, total_carbs_g - total_fiber_g)

        # Estimated Glycemic Load
        estimated_gl = (net_carbs_g / 100.0) * 50 if net_carbs_g > 0 else 0

        return MealSummary(
            total_calories=total_calories,
            total_carbs_g=total_carbs_g,
            total_sugars_g=total_sugars_g,
            total_fiber_g=total_fiber_g,
            total_protein_g=total_protein_g,
            total_fat_g=total_fat_g,
            net_carbs_g=net_carbs_g,
            estimated_glycemic_load=estimated_gl
        )

    @staticmethod
    def simulate_glucose_response(
        meal_summary: MealSummary,
        lifestyle: LifestyleProfile
    ) -> Dict[str, Any]:
        """
        Simulate glucose response over time with lifestyle modifiers.
        Returns peak glucose, timing, and timeline data.
        """

        # Base glucose absorption from carbohydrates
        carbs_absorbed = meal_summary.net_carbs_g

        # 1g carb ≈ 1g glucose (simple conversion for education)
        glucose_from_meal_grams = carbs_absorbed

        # Calculate peak glucose mg/dL
        # Basic formula: glucose load affects blood glucose proportionally
        base_peak_increase = (glucose_from_meal_grams / GlucoseSimulator.BLOOD_VOLUME_DL) * 1000

        peak_mg_dl = GlucoseSimulator.BASELINE_GLUCOSE_MG_DL + base_peak_increase

        # ============= Lifestyle Modifiers =============

        # Fiber modifier: reduces spike by delaying absorption
        if meal_summary.total_fiber_g > 10:
            peak_mg_dl *= 0.75  # 25% reduction
        elif meal_summary.total_fiber_g > 5:
            peak_mg_dl *= 0.85  # 15% reduction
        else:
            peak_mg_dl *= 0.95  # 5% increase (low fiber)

        # Protein modifier: slows absorption
        if meal_summary.total_protein_g > 30:
            peak_mg_dl *= 0.80  # 20% reduction
        elif meal_summary.total_protein_g > 15:
            peak_mg_dl *= 0.90  # 10% reduction

        # Fat modifier: slows absorption
        if meal_summary.total_fat_g > 20:
            peak_mg_dl *= 0.85  # 15% reduction
        elif meal_summary.total_fat_g > 10:
            peak_mg_dl *= 0.92  # 8% reduction

        # Protein-first strategy: eat protein before carbs
        if lifestyle.protein_first:
            peak_mg_dl *= 0.85

        # Post-meal walking: very beneficial
        peak_reduction = 1.0
        if lifestyle.post_meal_walk_minutes >= 10:
            peak_reduction *= 0.75  # 25% reduction
        elif lifestyle.post_meal_walk_minutes >= 5:
            peak_reduction *= 0.85  # 15% reduction

        # Regular exercise: improves insulin sensitivity
        if lifestyle.regular_exercise:
            peak_reduction *= 0.85  # 15% reduction

        # Sleep quality: poor sleep increases peaks
        if lifestyle.poor_sleep:
            peak_reduction *= 1.2  # 20% increase

        # Stress: high stress increases peaks
        if lifestyle.high_stress:
            peak_reduction *= 1.15  # 15% increase

        # Insulin resistance/prediabetes: increases peaks significantly
        if lifestyle.insulin_resistant or lifestyle.prediabetic:
            peak_reduction *= 1.4  # 40% increase

        peak_mg_dl *= peak_reduction

        # Determine peak timing based on meal composition
        if lifestyle.protein_first or meal_summary.total_protein_g > 20:
            peak_time_minutes = 60  # Delayed peak
        elif lifestyle.post_meal_walk_minutes > 0:
            peak_time_minutes = 45  # Slightly delayed
        elif meal_summary.total_fiber_g > 5:
            peak_time_minutes = 60  # Delayed
        else:
            peak_time_minutes = 30  # Typical fast spike

        # ============= Generate Glucose Curve =============
        glucose_curve = []

        for minutes in GlucoseSimulator.TIMEPOINTS:
            # Glucose rises during absorption, then gradually returns to baseline
            if minutes <= peak_time_minutes:
                # During rising phase
                progress = minutes / peak_time_minutes
                current_glucose_mg_dl = (
                    GlucoseSimulator.BASELINE_GLUCOSE_MG_DL +
                    (peak_mg_dl - GlucoseSimulator.BASELINE_GLUCOSE_MG_DL) * progress
                )
            else:
                # During falling phase
                time_since_peak = minutes - peak_time_minutes
                remaining_elevation = peak_mg_dl - GlucoseSimulator.BASELINE_GLUCOSE_MG_DL

                # Clearance rate depends on lifestyle
                clearance_factor = 1.0
                if lifestyle.post_meal_walk_minutes >= 10:
                    clearance_factor *= 1.3  # Faster clearance
                elif lifestyle.regular_exercise:
                    clearance_factor *= 1.15

                if lifestyle.insulin_resistant:
                    clearance_factor *= 0.7  # Slower clearance

                # Exponential decay back to baseline
                decay_rate = 0.03 * clearance_factor
                remaining_elevation *= (2.718 ** (-decay_rate * time_since_peak))
                current_glucose_mg_dl = GlucoseSimulator.BASELINE_GLUCOSE_MG_DL + remaining_elevation

            # Ensure non-negative
            current_glucose_mg_dl = max(GlucoseSimulator.BASELINE_GLUCOSE_MG_DL, current_glucose_mg_dl)

            # Convert mg/dL to grams
            current_glucose_grams = (current_glucose_mg_dl * GlucoseSimulator.BLOOD_VOLUME_DL) / 1000

            # Calculate percentage remaining in bloodstream
            glucose_percentage_remaining = (current_glucose_grams / GlucoseSimulator.BASELINE_GLUCOSE_GRAMS) * 100

            glucose_curve.append(
                GlucoseTimepointResponse(
                    minutes=minutes,
                    glucose_mg_dl=round(current_glucose_mg_dl, 1),
                    glucose_grams=round(current_glucose_grams, 2),
                    glucose_percentage_remaining=round(glucose_percentage_remaining, 1)
                )
            )

        # ============= Calculate Risk Scores =============

        # Insulin load score: higher carbs = higher insulin demand
        insulin_load_score = min(100, (meal_summary.net_carbs_g / 100.0) * 100)

        # Reduce insulin load score by fiber
        if meal_summary.total_fiber_g > 0:
            insulin_load_score *= (1 - (min(meal_summary.total_fiber_g, 20) / 40))

        # Reduce by protein and fat
        if meal_summary.total_protein_g > 0:
            insulin_load_score *= 0.85
        if meal_summary.total_fat_g > 0:
            insulin_load_score *= 0.90

        # Storage risk score: high when food energy exceeds likely expenditure + high spike
        storage_risk_score = 0.0

        # Caloric excess risk
        if meal_summary.total_calories > 500:  # Likely not burned immediately
            storage_risk_score += 30
        elif meal_summary.total_calories > 300:
            storage_risk_score += 15

        # Peak glucose contribution
        peak_multiple = peak_mg_dl / 120  # 120 = mildly elevated
        if peak_multiple > 2:
            storage_risk_score += 40
        elif peak_multiple > 1.3:
            storage_risk_score += 20

        # Lifestyle contribution
        if lifestyle.is_sedentary:
            storage_risk_score += 25
        if lifestyle.poor_sleep:
            storage_risk_score += 15
        if lifestyle.high_stress:
            storage_risk_score += 10

        if lifestyle.post_meal_walk_minutes >= 10:
            storage_risk_score *= 0.6
        if lifestyle.regular_exercise:
            storage_risk_score *= 0.8

        storage_risk_score = max(0, min(100, storage_risk_score))

        # ============= Generate Explanation =============
        explanation = GlucoseSimulator.generate_explanation(
            meal_summary=meal_summary,
            lifestyle=lifestyle,
            peak_mg_dl=peak_mg_dl,
            insulin_load_score=insulin_load_score,
            storage_risk_score=storage_risk_score
        )

        return {
            "peak_mg_dl": round(peak_mg_dl, 1),
            "baseline_glucose_grams": GlucoseSimulator.BASELINE_GLUCOSE_GRAMS,
            "peak_glucose_grams": round((peak_mg_dl * GlucoseSimulator.BLOOD_VOLUME_DL) / 1000, 2),
            "insulin_load_score": round(insulin_load_score, 1),
            "storage_risk_score": round(storage_risk_score, 1),
            "peak_time_minutes": peak_time_minutes,
            "glucose_curve": glucose_curve,
            "explanation": explanation
        }

    @staticmethod
    def generate_explanation(
        meal_summary: MealSummary,
        lifestyle: LifestyleProfile,
        peak_mg_dl: float,
        insulin_load_score: float,
        storage_risk_score: float
    ) -> Dict[str, Any]:
        """Generate educational explanation of glucose response"""

        explanation = {
            "summary": "",
            "factors": [],
            "recommendations": [],
            "risks": []
        }

        # Main summary
        if peak_mg_dl > 140:
            explanation["summary"] = "This meal may cause a notable blood glucose spike."
        elif peak_mg_dl > 120:
            explanation["summary"] = "This meal may elevate blood glucose moderately."
        else:
            explanation["summary"] = "This meal has a relatively modest effect on blood glucose."

        # Factors affecting response
        explanation["factors"].append(
            f"Carbohydrates: {meal_summary.total_carbs_g:.0f}g (provides glucose)"
        )

        if meal_summary.total_fiber_g > 5:
            explanation["factors"].append(
                f"Fiber: {meal_summary.total_fiber_g:.0f}g (slows glucose absorption)"
            )
        elif meal_summary.total_fiber_g > 0:
            explanation["factors"].append(
                f"Fiber: {meal_summary.total_fiber_g:.0f}g (minimal glucose buffering)"
            )
        else:
            explanation["factors"].append("Fiber: Very low (glucose enters blood quickly)")

        if meal_summary.total_protein_g > 15:
            explanation["factors"].append(
                f"Protein: {meal_summary.total_protein_g:.0f}g (slows glucose rise)"
            )

        if meal_summary.total_fat_g > 10:
            explanation["factors"].append(
                f"Fat: {meal_summary.total_fat_g:.0f}g (slows gastric emptying)"
            )

        # Lifestyle factors
        if lifestyle.post_meal_walk_minutes >= 10:
            explanation["factors"].append(
                f"Post-meal activity: {lifestyle.post_meal_walk_minutes} min walk "
                "(significantly improves glucose uptake)"
            )
        elif lifestyle.post_meal_walk_minutes > 0:
            explanation["factors"].append(
                f"Post-meal activity: {lifestyle.post_meal_walk_minutes} min "
                "(helps with glucose uptake)"
            )
        else:
            explanation["factors"].append(
                "Post-meal activity: Sedentary (glucose stays in bloodstream longer)"
            )

        if lifestyle.insulin_resistant or lifestyle.prediabetic:
            explanation["factors"].append(
                "Metabolic status: Insulin resistant (glucose clearance may be impaired)"
            )
            explanation["risks"].append(
                "With reduced insulin sensitivity, this spike may be even more pronounced. "
                "Consult healthcare provider for personalized advice."
            )

        if lifestyle.poor_sleep:
            explanation["factors"].append(
                "Sleep quality: Poor (increases glucose spike risk)"
            )

        # Recommendations
        if meal_summary.total_fiber_g < 5:
            explanation["recommendations"].append(
                "Add more fiber (vegetables, whole grains, legumes) to slow glucose absorption"
            )

        if meal_summary.total_protein_g < 15:
            explanation["recommendations"].append(
                "Include more protein (meat, fish, eggs, legumes) to moderate glucose rise"
            )

        if not lifestyle.post_meal_walk_minutes:
            explanation["recommendations"].append(
                "A 10-15 minute walk after this meal can reduce glucose spike by 20-30%"
            )

        if lifestyle.is_sedentary:
            explanation["recommendations"].append(
                "Regular movement and exercise improve insulin sensitivity and glucose handling"
            )

        # Storage risk context
        if storage_risk_score > 70:
            explanation["risks"].append(
                "When glucose spikes are repeated regularly, the excess can accumulate as fat storage. "
                " A single meal doesn't cause weight gain, but repeated patterns can contribute to it."
            )
        elif storage_risk_score > 40:
            explanation["risks"].append(
                "This meal has moderate energy density. In context of your lifestyle, "
                "excess energy may accumulate if not balanced with activity."
            )

        # Fatty liver context
        if meal_summary.total_carbs_g > 100 and meal_summary.total_fiber_g < 5:
            explanation["risks"].append(
                "High-carbohydrate meals with low fiber may promote liver glucose storage as fat. "
                "Occasional meals are fine, but repeated high-carb/low-fiber patterns can contribute to fatty liver risk."
            )

        # Disclaimer
        explanation["disclaimer"] = (
            "This is an educational simulation, not medical advice. "
            "Individual glucose responses vary by genetics, fitness level, stress, sleep, and medications. "
            "If diabetic or prediabetic, consult your doctor or use a continuous glucose monitor (CGM) for personal data."
        )

        return explanation

