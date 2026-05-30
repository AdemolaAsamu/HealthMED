import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Plus, BarChart3 } from 'lucide-react';
import { foodAPI, mealAPI, simulationAPI } from '@/services/api';
import { Food, LifestyleProfile, MealSummary } from '@/types';
import { useAppStore } from '@/store/useAppStore';

interface ComparisonResult {
  meal_id: number;
  meal_name: string;
  peak_mg_dl: number;
  insulin_load_score: number;
  storage_risk_score: number;
  meal_summary: MealSummary;
}

interface ComparisonResponse {
  comparisons: ComparisonResult[];
  best_option: ComparisonResult | null;
}

type Side = 'left' | 'right';

const defaultLifestyle: LifestyleProfile = {
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
};

export default function ComparisonPage() {
  const userSessionId = useAppStore((state) => state.currentUserSessionId);
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Food[]>([]);
  const [leftFood, setLeftFood] = useState<Food | null>(null);
  const [rightFood, setRightFood] = useState<Food | null>(null);
  const [lifestyle, setLifestyle] = useState<LifestyleProfile>(defaultLifestyle);
  const [loading, setLoading] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [comparison, setComparison] = useState<ComparisonResponse | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const results = await foodAPI.search(query, 12);
      setSearchResults(results.foods);
    } catch (error) {
      console.error('Error searching foods:', error);
      alert('Error searching foods. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const selectFood = (side: Side, food: Food) => {
    if (side === 'left') {
      setLeftFood(food);
    } else {
      setRightFood(food);
    }
    setComparison(null);
  };

  const createSingleFoodMeal = async (food: Food, name: string) => {
    return mealAPI.create({
      user_session_id: userSessionId,
      name,
      items: [{ food_id: food.id, quantity: 1, serving_multiplier: 1 }],
    });
  };

  const compareFoods = async () => {
    if (!leftFood || !rightFood) {
      alert('Choose two foods to compare.');
      return;
    }

    setComparing(true);
    try {
      const [leftMeal, rightMeal] = await Promise.all([
        createSingleFoodMeal(leftFood, leftFood.name),
        createSingleFoodMeal(rightFood, rightFood.name),
      ]);
      const result = await simulationAPI.compare(
        [leftMeal.id, rightMeal.id],
        lifestyle
      );
      setComparison(result);
    } catch (error) {
      console.error('Error comparing foods:', error);
      alert('Error comparing foods. Please try again.');
    } finally {
      setComparing(false);
    }
  };

  const renderFoodCard = (side: Side, food: Food | null) => (
    <div className="bg-white border border-gray-200 rounded-lg p-5 min-h-48">
      <p className="text-sm font-semibold text-gray-500 mb-3">
        {side === 'left' ? 'Option A' : 'Option B'}
      </p>
      {food ? (
        <div>
          <h3 className="text-xl font-bold mb-4">{food.name}</h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <p>Calories: {(food.calories || 0).toFixed(0)}</p>
            <p>Carbs: {(food.carbs_g || 0).toFixed(1)}g</p>
            <p>Sugars: {(food.sugars_g || 0).toFixed(1)}g</p>
            <p>Fiber: {(food.fiber_g || 0).toFixed(1)}g</p>
          </div>
        </div>
      ) : (
        <div className="h-full flex items-center justify-center text-gray-500">
          Select a food from search results
        </div>
      )}
    </div>
  );

  return (
    <div className="section">
      <div className="container-responsive max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h1 className="text-4xl font-bold mb-8">Compare Foods</h1>

          <div className="grid lg:grid-cols-[360px,1fr] gap-8">
            <div className="card">
              <h2 className="text-2xl font-bold mb-4">Search</h2>
              <form onSubmit={handleSearch} className="flex gap-2 mb-5">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search apple, rice, bread..."
                  className="input-field"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary p-3 disabled:opacity-50"
                >
                  <Search size={20} />
                </button>
              </form>

              <div className="space-y-2 max-h-[36rem] overflow-y-auto">
                {searchResults.map((food) => (
                  <div
                    key={food.id}
                    className="p-3 bg-gray-50 rounded-lg border border-gray-100"
                  >
                    <p className="font-semibold">{food.name}</p>
                    <p className="text-sm text-gray-600 mb-3">
                      {(food.carbs_g || 0).toFixed(1)}g carbs, {(food.fiber_g || 0).toFixed(1)}g fiber
                    </p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => selectFood('left', food)}
                        className="btn-secondary px-3 py-2 text-sm flex items-center gap-1"
                      >
                        <Plus size={16} /> A
                      </button>
                      <button
                        onClick={() => selectFood('right', food)}
                        className="btn-secondary px-3 py-2 text-sm flex items-center gap-1"
                      >
                        <Plus size={16} /> B
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-8">
              <div className="card">
                <div className="grid md:grid-cols-2 gap-6 mb-8">
                  {renderFoodCard('left', leftFood)}
                  {renderFoodCard('right', rightFood)}
                </div>

                <div className="grid md:grid-cols-3 gap-4 mb-8">
                  <label className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={lifestyle.is_sedentary || false}
                      onChange={(e) =>
                        setLifestyle({ ...lifestyle, is_sedentary: e.target.checked })
                      }
                      className="w-5 h-5"
                    />
                    <span>Sedentary</span>
                  </label>
                  <label className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={lifestyle.regular_exercise || false}
                      onChange={(e) =>
                        setLifestyle({ ...lifestyle, regular_exercise: e.target.checked })
                      }
                      className="w-5 h-5"
                    />
                    <span>Regular exercise</span>
                  </label>
                  <label className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={lifestyle.insulin_resistant || false}
                      onChange={(e) =>
                        setLifestyle({ ...lifestyle, insulin_resistant: e.target.checked })
                      }
                      className="w-5 h-5"
                    />
                    <span>Insulin resistant</span>
                  </label>
                </div>

                <button
                  onClick={compareFoods}
                  disabled={comparing || !leftFood || !rightFood}
                  className="btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  <BarChart3 size={20} />
                  {comparing ? 'Comparing...' : 'Compare Selected Foods'}
                </button>
              </div>

              {comparison && (
                <div className="card">
                  <h2 className="text-2xl font-bold mb-6">Comparison Results</h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    {comparison.comparisons.map((item) => (
                      <div
                        key={item.meal_id}
                        className={`border rounded-lg p-5 ${
                          comparison.best_option?.meal_id === item.meal_id
                            ? 'border-glucose-baseline bg-green-50'
                            : 'border-gray-200'
                        }`}
                      >
                        <h3 className="text-xl font-bold mb-4">{item.meal_name}</h3>
                        <div className="space-y-3">
                          <p>Peak glucose: {item.peak_mg_dl.toFixed(1)} mg/dL</p>
                          <p>Insulin load: {item.insulin_load_score.toFixed(1)}/100</p>
                          <p>Storage risk: {item.storage_risk_score.toFixed(1)}/100</p>
                          <p>Net carbs: {item.meal_summary.net_carbs_g.toFixed(1)}g</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
