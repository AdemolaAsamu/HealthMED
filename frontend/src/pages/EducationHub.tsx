import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { educationAPI } from '@/services/api';
import { EducationCard } from '@/types';

export default function EducationHub() {
  const [cards, setCards] = useState<EducationCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  useEffect(() => {
    const loadCards = async () => {
      try {
        const allCards = await educationAPI.getCards();
        setCards(allCards);
      } catch (error) {
        console.error('Error loading education cards:', error);
      } finally {
        setLoading(false);
      }
    };

    loadCards();
  }, []);

  const categories = ['basic', 'advanced', 'comparison'];

  const filteredCards = selectedCategory
    ? cards.filter((card) => card.category === selectedCategory)
    : cards;

  return (
    <div className="section">
      <div className="container-responsive max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h1 className="text-4xl font-bold mb-6 text-center">
            Learn About Glucose & Metabolism
          </h1>
          <p className="text-xl text-gray-600 text-center mb-12 max-w-3xl mx-auto">
            Educational content to understand how your body processes food and maintains glucose balance
          </p>

          {/* Category Filter */}
          <div className="flex flex-wrap justify-center gap-3 mb-12">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-6 py-2 rounded-full font-semibold transition-all ${
                selectedCategory === null
                  ? 'bg-brand-primary text-white'
                  : 'bg-gray-200 text-brand-dark hover:bg-gray-300'
              }`}
            >
              All Topics
            </button>
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-full font-semibold transition-all capitalize ${
                  selectedCategory === category
                    ? 'bg-brand-primary text-white'
                    : 'bg-gray-200 text-brand-dark hover:bg-gray-300'
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* Cards Grid */}
          {loading ? (
            <div className="text-center py-20">
              <p className="text-lg text-gray-600">Loading educational content...</p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 gap-8">
              {filteredCards.map((card, idx) => (
                <motion.div
                  key={card.id}
                  className="card"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: (idx % 2) * 0.1 }}
                  viewport={{ once: true }}
                  whileHover={{ y: -5, boxShadow: '0 20px 40px rgba(0,0,0,0.1)' }}
                >
                  <div className="flex items-start gap-3 mb-3">
                    <div className="w-2 h-2 bg-brand-primary rounded-full mt-2 flex-shrink-0" />
                    <div className="flex-1">
                      <h3 className="text-xl font-bold">{card.title}</h3>
                      {card.category && (
                        <span className="inline-block mt-2 px-2 py-1 bg-brand-accent bg-opacity-30 text-brand-dark text-xs font-semibold rounded capitalize">
                          {card.category}
                        </span>
                      )}
                    </div>
                  </div>
                  <p className="text-gray-600 leading-relaxed mt-4">{card.body}</p>
                </motion.div>
              ))}
            </div>
          )}

          {filteredCards.length === 0 && !loading && (
            <div className="text-center py-20">
              <p className="text-lg text-gray-600">
                No content found for this category
              </p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}

