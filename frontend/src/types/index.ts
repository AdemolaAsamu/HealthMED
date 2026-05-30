// ============= Food Types =============
export interface Food {
  id: number;
  source: string;
  source_food_id: string;
  name: string;
  brand?: string;
  serving_size_g: number;
  calories?: number;
  carbs_g?: number;
  sugars_g?: number;
  fiber_g?: number;
  protein_g?: number;
  fat_g?: number;
  glycemic_category?: string;
  created_at: string;
  updated_at: string;
}

export interface FoodSearchResult {
  foods: Food[];
  total_results: number;
  query: string;
}

// ============= Meal Types =============
export interface MealItem {
  id: number;
  food_id: number;
  quantity: number;
  serving_multiplier: number;
  carbs_g?: number;
  sugars_g?: number;
  calories?: number;
  food?: Food;
}

export interface Meal {
  id: number;
  user_session_id: string;
  name?: string;
  created_at: string;
  meal_items: MealItem[];
}

export interface MealCreate {
  user_session_id: string;
  name?: string;
  items: MealItemCreate[];
}

export interface MealItemCreate {
  food_id: number;
  quantity?: number;
  serving_multiplier?: number;
}

export interface MealSummary {
  total_calories: number;
  total_carbs_g: number;
  total_sugars_g: number;
  total_fiber_g: number;
  total_protein_g: number;
  total_fat_g: number;
  net_carbs_g: number;
  estimated_glycemic_load: number;
}

// ============= Lifestyle Types =============
export interface LifestyleProfile {
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

// ============= Simulation Types =============
export interface GlucoseTimepoint {
  minutes: number;
  glucose_mg_dl: number;
  glucose_grams: number;
  glucose_percentage_remaining: number;
}

export interface Simulation {
  id: number;
  meal_id: number;
  estimated_peak_mg_dl: number;
  glucose_grams_baseline: number;
  glucose_grams_peak: number;
  insulin_load_score: number;
  storage_risk_score: number;
  glucose_curve: GlucoseTimepoint[];
  explanation: Record<string, any>;
  created_at: string;
}

export interface SimulationRequest {
  meal_id: number;
  lifestyle_profile: LifestyleProfile;
}

// ============= Education Types =============
export interface EducationCard {
  id: number;
  title: string;
  body: string;
  animation_type?: string;
  category?: 'basic' | 'advanced' | 'comparison';
  sort_order: number;
}

export interface EducationCardCreate {
  title: string;
  body: string;
  animation_type?: string;
  category?: 'basic' | 'advanced' | 'comparison';
  sort_order: number;
}

// ============= API Response Types =============
export interface ApiResponse<T> {
  status: string;
  data?: T;
  message?: string;
  error?: string;
}

export interface DisclaimerResponse {
  primary_disclaimer: string;
  glucose_response: string;
  cgm_recommendation: string;
  medical_conditions: string[];
  limitations: string[];
}

// ============= UI State Types =============
export interface AppState {
  currentUserSessionId: string;
  currentMeal: Meal | null;
  lastSimulation: Simulation | null;
  educationCards: EducationCard[];
  disclaimersSeen: boolean;

  // Actions
  setCurrentMeal: (meal: Meal | null) => void;
  setLastSimulation: (simulation: Simulation | null) => void;
  setEducationCards: (cards: EducationCard[]) => void;
  setDisclaimersSeen: (seen: boolean) => void;
}

