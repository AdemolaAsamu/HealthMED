import { create } from 'zustand';
import { AppState, Meal, Simulation, EducationCard } from '@/types';

// Generate or retrieve session ID
const getOrCreateSessionId = (): string => {
  const stored = localStorage.getItem('userSessionId');
  if (stored) return stored;
  // Simple session ID generation using timestamp + random
  const newId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  localStorage.setItem('userSessionId', newId);
  return newId;
};

export const useAppStore = create<AppState>((set) => ({
  currentUserSessionId: getOrCreateSessionId(),
  currentMeal: null,
  lastSimulation: null,
  educationCards: [],
  disclaimersSeen: localStorage.getItem('disclaimersSeen') === 'true',

  setCurrentMeal: (meal: Meal | null) => {
    set({ currentMeal: meal });
  },

  setLastSimulation: (simulation: Simulation | null) => {
    set({ lastSimulation: simulation });
  },

  setEducationCards: (cards: EducationCard[]) => {
    set({ educationCards: cards });
  },

  setDisclaimersSeen: (seen: boolean) => {
    set({ disclaimersSeen: seen });
    if (seen) {
      localStorage.setItem('disclaimersSeen', 'true');
    }
  },
}));

