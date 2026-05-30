import { useState } from 'react';
import { motion } from 'framer-motion';
import { educationAPI } from '@/services/api';
import { EducationCardCreate } from '@/types';

type EducationCategory = NonNullable<EducationCardCreate['category']>;

export default function Admin() {
  const [adminKey, setAdminKey] = useState(localStorage.getItem('adminKey') || '');
  const [isUnlocked, setIsUnlocked] = useState(
    !import.meta.env.VITE_REQUIRE_ADMIN_KEY || localStorage.getItem('adminKey') !== null
  );
  const [newCard, setNewCard] = useState<EducationCardCreate>({
    title: '',
    body: '',
    animation_type: '',
    category: 'basic',
    sort_order: 0,
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const unlockAdmin = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('adminKey', adminKey);
    setIsUnlocked(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newCard.title.trim() || !newCard.body.trim()) {
      setMessage({ type: 'error', text: 'Please fill in all required fields' });
      return;
    }

    setLoading(true);
    try {
      await educationAPI.createCard(newCard, adminKey);
      setMessage({ type: 'success', text: 'Education card created successfully!' });
      setNewCard({
        title: '',
        body: '',
        animation_type: '',
        category: 'basic',
        sort_order: 0,
      });
    } catch (error) {
      console.error('Error creating card:', error);
      setMessage({ type: 'error', text: 'Error creating card. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section">
      <div className="container-responsive max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h1 className="text-4xl font-bold mb-8">Admin Panel</h1>

          {!isUnlocked && (
            <div className="card mb-8">
              <h2 className="text-2xl font-bold mb-6">Admin Access</h2>
              <form onSubmit={unlockAdmin} className="space-y-4">
                <input
                  type="password"
                  value={adminKey}
                  onChange={(e) => setAdminKey(e.target.value)}
                  placeholder="Admin key"
                  className="input-field"
                />
                <button type="submit" className="btn-primary">
                  Unlock Admin Tools
                </button>
              </form>
            </div>
          )}

          {isUnlocked && (
          <div className="card">
            <h2 className="text-2xl font-bold mb-6">Add Education Content</h2>

            {message && (
              <div
                className={`p-4 rounded-lg mb-6 ${
                  message.type === 'success'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                {message.text}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  value={newCard.title}
                  onChange={(e) =>
                    setNewCard({ ...newCard, title: e.target.value })
                  }
                  placeholder="Enter card title"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">
                  Content Body *
                </label>
                <textarea
                  value={newCard.body}
                  onChange={(e) =>
                    setNewCard({ ...newCard, body: e.target.value })
                  }
                  placeholder="Enter detailed content"
                  rows={6}
                  className="input-field"
                  required
                />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Category
                  </label>
                  <select
                    value={newCard.category || 'basic'}
                    onChange={(e) =>
                      setNewCard({
                        ...newCard,
                        category: e.target.value as EducationCategory,
                      })
                    }
                    className="input-field"
                  >
                    <option value="basic">Basic</option>
                    <option value="advanced">Advanced</option>
                    <option value="comparison">Comparison</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Animation Type
                  </label>
                  <select
                    value={newCard.animation_type || ''}
                    onChange={(e) =>
                      setNewCard({
                        ...newCard,
                        animation_type: e.target.value,
                      })
                    }
                    className="input-field"
                  >
                    <option value="">None</option>
                    <option value="glucose_spike">Glucose Spike</option>
                    <option value="insulin_action">Insulin Action</option>
                    <option value="glucose_curve">Glucose Curve</option>
                    <option value="comparison">Comparison</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">
                  Sort Order
                </label>
                <input
                  type="number"
                  value={newCard.sort_order}
                  onChange={(e) =>
                    setNewCard({
                      ...newCard,
                      sort_order: parseInt(e.target.value),
                    })
                  }
                  className="input-field"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Education Card'}
              </button>
            </form>
          </div>
          )}

          {isUnlocked && (
          <div className="mt-12 card">
            <h2 className="text-2xl font-bold mb-6">Admin Notes</h2>
            <ul className="space-y-3 text-gray-700">
              <li>• This panel allows you to add educational content to the platform</li>
              <li>• All content is reviewed before display to ensure accuracy</li>
              <li>• Use clear, educational language avoiding medical claims</li>
              <li>• Include disclaimers where appropriate</li>
              <li>• Sort order determines appearance on the Learn page</li>
              <li>• Categories help users find relevant information</li>
            </ul>
          </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}

