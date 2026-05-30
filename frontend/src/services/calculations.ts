import { MealSummary, GlucoseTimepoint } from '@/types';

// Educational glucose calculation utilities
export const glucoseCalculations = {
  // Constants
  BASELINE_GLUCOSE_MG_DL: 90,
  BASELINE_GLUCOSE_GRAMS: 4.5,
  TEASPOON_GRAMS: 4.5,

  /**
   * Convert mg/dL to grams of glucose in blood
   * Normal blood volume: 5 liters (50 deciliters)
   */
  mgDlToGrams(mgDl: number): number {
    return (mgDl * 50) / 1000; // 50 dL total blood volume
  },

  /**
   * Convert grams of glucose to mg/dL
   */
  gramsToMgDl(grams: number): number {
    return (grams * 1000) / 50;
  },

  /**
   * Calculate glucose spike severity
   */
  getSpikeSeverity(peakMgDl: number): 'low' | 'mild' | 'moderate' | 'high' {
    if (peakMgDl <= 120) return 'low';
    if (peakMgDl <= 140) return 'mild';
    if (peakMgDl <= 160) return 'moderate';
    return 'high';
  },

  /**
   * Calculate insulin load score context
   */
  getInsulinLoadContext(score: number): string {
    if (score < 20) return 'Very low insulin demand';
    if (score < 40) return 'Low insulin demand';
    if (score < 60) return 'Moderate insulin demand';
    if (score < 80) return 'High insulin demand';
    return 'Very high insulin demand';
  },

  /**
   * Calculate storage risk context
   */
  getStorageRiskContext(score: number): string {
    if (score < 20) return 'Low fat storage risk';
    if (score < 40) return 'Modest fat storage risk';
    if (score < 60) return 'Moderate fat storage risk';
    if (score < 80) return 'Elevated fat storage risk';
    return 'High fat storage risk';
  },

  /**
   * Get color for glucose level
   */
  getGlucoseColor(mgDl: number): string {
    if (mgDl <= 100) return '#95E1D3'; // Low - teal
    if (mgDl <= 140) return '#FFB84D'; // Normal-elevated - orange
    if (mgDl <= 160) return '#FF9A55'; // High - darker orange
    return '#FF6B6B'; // Very high - red
  },

  /**
   * Get color for risk score
   */
  getRiskColor(score: number): string {
    if (score < 30) return '#4ECDC4'; // Low - green
    if (score < 50) return '#FFE66D'; // Moderate - yellow
    if (score < 70) return '#FFB84D'; // High - orange
    return '#FF6B6B'; // Very high - red
  },

  /**
   * Format glucose for display
   */
  formatGlucose(mg_dl: number, decimals: number = 1): string {
    return `${mg_dl.toFixed(decimals)} mg/dL`;
  },

  /**
   * Format grams to teaspoons (1 tsp ≈ 4.5g)
   */
  gramsToTeaspoons(grams: number): number {
    return grams / this.TEASPOON_GRAMS;
  },

  /**
   * Get dietary recommendations based on meal
   */
  getDietaryRecommendations(meal: MealSummary): string[] {
    const recommendations: string[] = [];

    if (meal.total_fiber_g < 5) {
      recommendations.push('💪 Add more fiber (vegetables, whole grains) to slow glucose absorption');
    }

    if (meal.total_protein_g < 15) {
      recommendations.push('🥚 Include protein (eggs, meat, legumes) to moderate glucose rise');
    }

    if (meal.total_fat_g < 10) {
      recommendations.push('🥑 Add healthy fats to slow digestion');
    }

    if (meal.total_carbs_g > 60 && meal.total_fiber_g < 10) {
      recommendations.push('🌾 This is a high-carb meal with low fiber. Consider protein + vegetables first');
    }

    if (meal.total_calories > 500) {
      recommendations.push('🚴 A 10-15 minute walk after this meal will significantly help glucose control');
    }

    return recommendations.length > 0 ? recommendations : ['✓ Balanced meal!'];
  },

  /**
   * Compare two meals
   */
  compareMeals(meal1: MealSummary, meal2: MealSummary): {
    carb_difference_g: number;
    fiber_difference_g: number;
    protein_difference_g: number;
    calorie_difference: number;
    gl_difference: number;
  } {
    return {
      carb_difference_g: meal2.total_carbs_g - meal1.total_carbs_g,
      fiber_difference_g: meal2.total_fiber_g - meal1.total_fiber_g,
      protein_difference_g: meal2.total_protein_g - meal1.total_protein_g,
      calorie_difference: meal2.total_calories - meal1.total_calories,
      gl_difference: meal2.estimated_glycemic_load - meal1.estimated_glycemic_load,
    };
  }
};

// Utility function to generate glucose curve points for visualization
export const generateGlucoseCurvePoints = (
  baseline: number,
  peak: number,
  peakTimeMinutes: number
): GlucoseTimepoint[] => {
  const points: GlucoseTimepoint[] = [];
  const timepoints = [0, 15, 30, 45, 60, 90, 120];

  for (const minutes of timepoints) {
    let mgDl: number;

    if (minutes <= peakTimeMinutes) {
      // Rising phase
      const progress = minutes / peakTimeMinutes;
      mgDl = baseline + (peak - baseline) * progress;
    } else {
      // Falling phase
      const timeSincePeak = minutes - peakTimeMinutes;
      const remaining = peak - baseline;
      const decayRate = 0.03;
      const newRemaining = remaining * Math.exp(-decayRate * timeSincePeak);
      mgDl = baseline + newRemaining;
    }

    const grams = glucoseCalculations.mgDlToGrams(mgDl);
    const percentage = (grams / glucoseCalculations.BASELINE_GLUCOSE_GRAMS) * 100;

    points.push({
      minutes,
      glucose_mg_dl: parseFloat(mgDl.toFixed(1)),
      glucose_grams: parseFloat(grams.toFixed(2)),
      glucose_percentage_remaining: parseFloat(percentage.toFixed(1)),
    });
  }

  return points;
};

