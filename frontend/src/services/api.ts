import axios, { AxiosInstance } from 'axios';
import {
  Food,
  FoodSearchResult,
  Meal,
  MealCreate,
  MealSummary,
  Simulation,
  SimulationRequest,
  EducationCard,
  EducationCardCreate,
  DisclaimerResponse,
  AdminLoginResponse,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const getAdminHeaders = (adminKey?: string) =>
  adminKey ? { 'X-Admin-Key': adminKey } : undefined;

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============= Food API =============
export const foodAPI = {
  search: async (query: string, limit: number = 20): Promise<FoodSearchResult> => {
    const response = await apiClient.get<FoodSearchResult>('/api/foods/search', {
      params: { query, limit },
    });
    return response.data;
  },

  getById: async (foodId: number): Promise<Food> => {
    const response = await apiClient.get<Food>(`/api/foods/${foodId}`);
    return response.data;
  },

  addManual: async (food: Partial<Food>): Promise<Food> => {
    const response = await apiClient.post<Food>('/api/foods/manual', food);
    return response.data;
  },
};

// ============= Meal API =============
export const mealAPI = {
  create: async (meal: MealCreate): Promise<Meal> => {
    const response = await apiClient.post<Meal>('/api/meals/', meal);
    return response.data;
  },

  getById: async (mealId: number): Promise<Meal> => {
    const response = await apiClient.get<Meal>(`/api/meals/${mealId}`);
    return response.data;
  },

  getUserMeals: async (userSessionId: string, limit: number = 50): Promise<Meal[]> => {
    const response = await apiClient.get<Meal[]>(
      `/api/meals/user/${userSessionId}`,
      { params: { limit } }
    );
    return response.data;
  },

  addItem: async (mealId: number, item: Record<string, any>): Promise<any> => {
    const response = await apiClient.post(`/api/meals/${mealId}/items`, item);
    return response.data;
  },

  removeItem: async (mealId: number, itemId: number): Promise<any> => {
    const response = await apiClient.delete(`/api/meals/${mealId}/items/${itemId}`);
    return response.data;
  },

  delete: async (mealId: number): Promise<any> => {
    const response = await apiClient.delete(`/api/meals/${mealId}`);
    return response.data;
  },

  getSummary: async (mealId: number): Promise<MealSummary> => {
    const response = await apiClient.get<MealSummary>(`/api/meals/${mealId}/summary`);
    return response.data;
  },
};

// ============= Simulation API =============
export const simulationAPI = {
  create: async (request: SimulationRequest): Promise<Simulation> => {
    const response = await apiClient.post<Simulation>('/api/simulations/', request);
    return response.data;
  },

  getById: async (simulationId: number): Promise<Simulation> => {
    const response = await apiClient.get<Simulation>(`/api/simulations/${simulationId}`);
    return response.data;
  },

  getMealSimulations: async (mealId: number): Promise<Simulation[]> => {
    const response = await apiClient.get<Simulation[]>(`/api/simulations/meal/${mealId}`);
    return response.data;
  },

  compare: async (mealIds: number[], lifestyle: Record<string, any>): Promise<any> => {
    const response = await apiClient.post('/api/simulations/compare', {
      meal_ids: mealIds,
      lifestyle,
    });
    return response.data;
  },
};

// ============= Education API =============
export const educationAPI = {
  getCards: async (category?: string): Promise<EducationCard[]> => {
    const response = await apiClient.get<EducationCard[]>('/api/education/cards', {
      params: category ? { category } : {},
    });
    return response.data;
  },

  getCardById: async (cardId: number): Promise<EducationCard> => {
    const response = await apiClient.get<EducationCard>(`/api/education/cards/${cardId}`);
    return response.data;
  },

  createCard: async (
    card: EducationCardCreate,
    adminKey?: string
  ): Promise<EducationCard> => {
    const response = await apiClient.post<EducationCard>('/api/education/cards', card, {
      headers: getAdminHeaders(adminKey),
    });
    return response.data;
  },

  updateCard: async (
    cardId: number,
    card: EducationCardCreate,
    adminKey?: string
  ): Promise<EducationCard> => {
    const response = await apiClient.put<EducationCard>(
      `/api/education/cards/${cardId}`,
      card,
      { headers: getAdminHeaders(adminKey) }
    );
    return response.data;
  },

  deleteCard: async (cardId: number, adminKey?: string): Promise<any> => {
    const response = await apiClient.delete(`/api/education/cards/${cardId}`, {
      headers: getAdminHeaders(adminKey),
    });
    return response.data;
  },
};

// ============= Admin API =============
export const adminAPI = {
  login: async (adminKey: string): Promise<AdminLoginResponse> => {
    const response = await apiClient.post<AdminLoginResponse>('/api/admin/login', {
      admin_key: adminKey,
    });
    return response.data;
  },
};

// ============= General API =============
export const generalAPI = {
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  getDisclaimers: async (): Promise<DisclaimerResponse> => {
    const response = await apiClient.get<DisclaimerResponse>('/api/disclaimers');
    return response.data;
  },
};

export default apiClient;

