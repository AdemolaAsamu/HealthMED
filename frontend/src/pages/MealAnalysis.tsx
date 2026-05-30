import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Plus, Trash2, Send } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { foodAPI, mealAPI, simulationAPI } from '@/services/api';
import { Food, LifestyleProfile } from '@/types';
import { glucoseCalculations } from '@/services/calculations';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function MealAnalysis() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Food[]>([]);
  const [selectedFoods, setSelectedFoods] = useState<Array<{ food: Food; multiplier: number }>>([]);
  const setCurrentMeal = useAppStore((state) => state.setCurrentMeal);
  const [lastSimulation, setLastSimulation] = useAppStore((state) => [
    state.lastSimulation,
    state.setLastSimulation,
  ]);
  const [loading, setLoading] = useState(false);
  const [mealLoading, setMealLoading] = useState(false);
  const [lifestyle, setLifestyle] = useState<LifestyleProfile>({
    is_sedentary: true,
    post_meal_walk_minutes: 0,
    regular_exercise: false,
    poor_sleep: false,
    high_stress: false,
    high_muscle_mass: false,
    insulin_resistant: false,
    prediabetic: false,
    high_fiber_meal: false,
    protein_first: false,
  });

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim() || loading) return;

    setLoading(true);
    try {
      const results = await foodAPI.search(searchQuery, 20);
      setSearchResults(results.foods);
    } catch (error) {
      console.error('Error searching foods:', error);
      alert('Error searching foods. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const addFood = (food: Food) => {
    setSelectedFoods([...selectedFoods, { food, multiplier: 1 }]);
    setSearchResults([]);
    setSearchQuery('');
  };

  const removeFood = (index: number) => {
    setSelectedFoods(selectedFoods.filter((_, i) => i !== index));
  };

  const updateMultiplier = (index: number, multiplier: number) => {
    const updated = [...selectedFoods];
    updated[index].multiplier = Math.max(0.1, multiplier);
    setSelectedFoods(updated);
  };

  const handleCreateMeal = async () => {
    if (selectedFoods.length === 0) {
      alert('Please add at least one food');
      return;
    }

    setMealLoading(true);
    try {
      const mealData = {
        user_session_id: useAppStore.getState().currentUserSessionId,
        name: `Meal at ${new Date().toLocaleTimeString()}`,
        items: selectedFoods.map((item) => ({
          food_id: item.food.id,
          quantity: 1,
          serving_multiplier: item.multiplier,
        })),
      };

      const createdMeal = await mealAPI.create(mealData);
      setCurrentMeal(createdMeal);

      // Run simulation
      const simulation = await simulationAPI.create({
        meal_id: createdMeal.id,
        lifestyle_profile: lifestyle,
      });
      setLastSimulation(simulation);
    } catch (error) {
      console.error('Error creating meal:', error);
      alert('Error creating meal. Please try again.');
    } finally {
      setMealLoading(false);
    }
  };

  const calculateMealTotals = () => {
    const totals = {
      calories: 0,
      carbs: 0,
      sugars: 0,
      fiber: 0,
      protein: 0,
      fat: 0,
    };

    selectedFoods.forEach(({ food, multiplier }) => {
      totals.calories += (food.calories || 0) * multiplier;
      totals.carbs += (food.carbs_g || 0) * multiplier;
      totals.sugars += (food.sugars_g || 0) * multiplier;
      totals.fiber += (food.fiber_g || 0) * multiplier;
      totals.protein += (food.protein_g || 0) * multiplier;
      totals.fat += (food.fat_g || 0) * multiplier;
    });

    return totals;
  };

  const mealTotals = calculateMealTotals();

  return (
    <div className="section">
      <div className="container-responsive max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-12 text-center">
          Analyze Your Meal
        </h1>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Left Column: Food Search and Selection */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            {/* Search */}
            <div className="card mb-8">
              <h2 className="text-2xl font-bold mb-4">Search Foods</h2>
              <form onSubmit={handleSearch} className="flex gap-2 mb-4">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by name (e.g., apple, chicken, rice)..."
                  className="input-field"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary disabled:opacity-50 p-3"
                >
                  <Search size={20} />
                </button>
              </form>

              {/* Search Results */}
              {searchResults.length > 0 && (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {searchResults.map((food) => (
                    <div
                      key={food.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                    >
                      <div className="flex-1">
                        <p className="font-semibold">{food.name}</p>
                        <p className="text-sm text-gray-600">
                          {food.calories}cal | {food.carbs_g}g carbs | {food.fiber_g}g fiber
                        </p>
                      </div>
                      <button
                        onClick={() => addFood(food)}
                        className="btn-secondary p-2"
                      >
                        <Plus size={20} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Selected Foods */}
            <div className="card">
              <h2 className="text-2xl font-bold mb-4">Selected Foods</h2>
              {selectedFoods.length === 0 ? (
                <p className="text-gray-600">Add foods above to analyze</p>
              ) : (
                <div className="space-y-3">
                  {selectedFoods.map(({ food, multiplier }, idx) => (
                    <div key={idx} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <p className="font-semibold">{food.name}</p>
                        <p className="text-sm text-gray-600">
                          {(food.calories || 0) * multiplier}cal
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <input
                          type="number"
                          min="0.1"
                          step="0.1"
                          value={multiplier.toFixed(1)}
                          onChange={(e) =>
                            updateMultiplier(idx, parseFloat(e.target.value))
                          }
                          className="w-16 px-2 py-1 border rounded text-center"
                        />
                        <span className="text-sm text-gray-600">x</span>
                      </div>
                      <button
                        onClick={() => removeFood(idx)}
                        className="p-2 text-brand-primary hover:bg-red-100 rounded transition"
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>

          {/* Right Column: Meal Summary and Lifestyle */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
          >
            {/* Meal Summary */}
            <div className="card mb-8">
              <h2 className="text-2xl font-bold mb-6">Meal Summary</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-brand-light rounded-lg">
                  <p className="text-sm text-gray-600">Calories</p>
                  <p className="text-3xl font-bold text-brand-primary">
                    {mealTotals.calories.toFixed(0)}
                  </p>
                </div>
                <div className="p-4 bg-brand-light rounded-lg">
                  <p className="text-sm text-gray-600">Carbs</p>
                  <p className="text-3xl font-bold text-brand-primary">
                    {mealTotals.carbs.toFixed(1)}g
                  </p>
                </div>
                <div className="p-4 bg-brand-light rounded-lg">
                  <p className="text-sm text-gray-600">Sugars</p>
                  <p className="text-3xl font-bold text-brand-primary">
                    {mealTotals.sugars.toFixed(1)}g
                  </p>
                </div>
                <div className="p-4 bg-brand-light rounded-lg">
                  <p className="text-sm text-gray-600">Fiber</p>
                  <p className="text-3xl font-bold text-glucose-baseline">
                    {mealTotals.fiber.toFixed(1)}g
                  </p>
                </div>
                <div className="p-4 bg-brand-light rounded-lg">
                  <p className="text-sm text-gray-600">Protein</p>
                  <p className="text-3xl font-bold">
                    {mealTotals.protein.toFixed(1)}g
                  </p>
                </div>
                <div className="p-4 bg-brand-light rounded-lg">
                  <p className="text-sm text-gray-600">Fat</p>
                  <p className="text-3xl font-bold">
                    {mealTotals.fat.toFixed(1)}g
                  </p>
                </div>
              </div>
            </div>

            {/* Lifestyle Settings */}
            <div className="card">
              <h2 className="text-2xl font-bold mb-6">Lifestyle Factors</h2>
              <div className="space-y-4">
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={lifestyle.is_sedentary || false}
                    onChange={(e) =>
                      setLifestyle({
                        ...lifestyle,
                        is_sedentary: e.target.checked,
                      })
                    }
                    className="w-5 h-5 rounded"
                  />
                  <span>Sedentary (no walking planned)</span>
                </label>

                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Post-meal walk: {lifestyle.post_meal_walk_minutes} minutes
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="60"
                    value={lifestyle.post_meal_walk_minutes || 0}
                    onChange={(e) =>
                      setLifestyle({
                        ...lifestyle,
                        post_meal_walk_minutes: parseInt(e.target.value),
                      })
                    }
                    className="w-full"
                  />
                </div>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={lifestyle.regular_exercise || false}
                    onChange={(e) =>
                      setLifestyle({
                        ...lifestyle,
                        regular_exercise: e.target.checked,
                      })
                    }
                    className="w-5 h-5 rounded"
                  />
                  <span>Regular exercise routine</span>
                </label>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={lifestyle.poor_sleep || false}
                    onChange={(e) =>
                      setLifestyle({
                        ...lifestyle,
                        poor_sleep: e.target.checked,
                      })
                    }
                    className="w-5 h-5 rounded"
                  />
                  <span>Poor sleep (&lt; 7 hours)</span>
                </label>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={lifestyle.insulin_resistant || false}
                    onChange={(e) =>
                      setLifestyle({
                        ...lifestyle,
                        insulin_resistant: e.target.checked,
                      })
                    }
                    className="w-5 h-5 rounded"
                  />
                  <span>Insulin resistant / Prediabetic</span>
                </label>

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={lifestyle.protein_first || false}
                    onChange={(e) =>
                      setLifestyle({
                        ...lifestyle,
                        protein_first: e.target.checked,
                      })
                    }
                    className="w-5 h-5 rounded"
                  />
                  <span>Eating protein first</span>
                </label>
              </div>

              <button
                onClick={handleCreateMeal}
                disabled={mealLoading || selectedFoods.length === 0}
                className="btn-primary w-full mt-8 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                <Send size={20} />
                {mealLoading ? 'Analyzing...' : 'Analyze Meal'}
              </button>
            </div>
          </motion.div>
        </div>

        {/* Simulation Results */}
        {lastSimulation && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mt-20 card"
          >
            <h2 className="text-3xl font-bold mb-8">Glucose Response Simulation</h2>

            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <div className="bg-gradient-to-br from-brand-primary to-red-600 text-white p-8 rounded-xl">
                <p className="text-sm font-semibold mb-2">Peak Glucose</p>
                <p className="text-4xl font-bold">
                  {lastSimulation.estimated_peak_mg_dl.toFixed(1)} mg/dL
                </p>
                <p className="text-sm mt-2 text-white text-opacity-80">
                  {glucoseCalculations.getSpikeSeverity(
                    lastSimulation.estimated_peak_mg_dl
                  )}
                </p>
              </div>

              <div className="bg-gradient-to-br from-brand-secondary to-teal-600 text-white p-8 rounded-xl">
                <p className="text-sm font-semibold mb-2">Insulin Load Score</p>
                <p className="text-4xl font-bold">
                  {lastSimulation.insulin_load_score.toFixed(1)}/100
                </p>
                <p className="text-sm mt-2 text-white text-opacity-80">
                  {glucoseCalculations.getInsulinLoadContext(
                    lastSimulation.insulin_load_score
                  )}
                </p>
              </div>

              <div className="bg-gradient-to-br from-yellow-500 to-orange-600 text-white p-8 rounded-xl">
                <p className="text-sm font-semibold mb-2">Storage Risk Score</p>
                <p className="text-4xl font-bold">
                  {lastSimulation.storage_risk_score.toFixed(1)}/100
                </p>
                <p className="text-sm mt-2 text-white text-opacity-80">
                  {glucoseCalculations.getStorageRiskContext(
                    lastSimulation.storage_risk_score
                  )}
                </p>
              </div>
            </div>

            {/* Glucose Curve Chart */}
            <div className="bg-brand-light p-8 rounded-xl">
              <h3 className="text-lg font-bold mb-6">Blood Glucose Timeline</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={lastSimulation.glucose_curve}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="minutes"
                    label={{ value: 'Minutes', position: 'insideBottomRight', offset: -5 }}
                  />
                  <YAxis
                    label={{ value: 'Glucose (mg/dL)', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="glucose_mg_dl"
                    stroke="#FF6B6B"
                    strokeWidth={3}
                    name="Blood Glucose"
                    dot={{ fill: '#FF6B6B', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Explanation */}
            {lastSimulation.explanation && (
              <div className="mt-8 space-y-6">
                <div>
                  <h3 className="text-lg font-bold mb-3">Summary</h3>
                  <p className="text-gray-700">{lastSimulation.explanation.summary}</p>
                </div>

                {lastSimulation.explanation.factors && (
                  <div>
                    <h3 className="text-lg font-bold mb-3">Key Factors</h3>
                    <ul className="space-y-2">
                      {lastSimulation.explanation.factors.map((factor: string, idx: number) => (
                        <li key={idx} className="flex gap-2">
                          <span className="text-brand-primary font-bold">→</span>
                          <span>{factor}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {lastSimulation.explanation.recommendations && (
                  <div>
                    <h3 className="text-lg font-bold mb-3">Recommendations</h3>
                    <ul className="space-y-2">
                      {lastSimulation.explanation.recommendations.map((rec: string, idx: number) => (
                        <li key={idx} className="flex gap-2">
                          <span className="text-glucose-baseline font-bold">✓</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}

