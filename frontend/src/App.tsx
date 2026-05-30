import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Header from './components/common/Header';
import DisclaimerBanner from './components/common/DisclaimerBanner';
import Home from './pages/Home';
import MealAnalysis from './pages/MealAnalysis';
import ComparisonPage from './pages/ComparisonPage';
import EducationHub from './pages/EducationHub';
import Admin from './pages/Admin';
import { DisclaimerResponse } from './types';
import { useAppStore } from './store/useAppStore';
import { generalAPI } from './services/api';

function App() {
  const [disclaimersSeen, setDisclaimersSeen] = useAppStore((state) => [
    state.disclaimersSeen,
    state.setDisclaimersSeen,
  ]);
  const [disclaimerData, setDisclaimerData] = useState<DisclaimerResponse | null>(null);

  useEffect(() => {
    const loadDisclaimers = async () => {
      try {
        const data = await generalAPI.getDisclaimers();
        setDisclaimerData(data);
      } catch (error) {
        console.error('Error loading disclaimers:', error);
      }
    };

    loadDisclaimers();
  }, []);

  const handleDismissDisclaimer = () => {
    setDisclaimersSeen(true);
  };

  return (
    <Router>
      <div className="min-h-screen bg-brand-light">
        {!disclaimersSeen && disclaimerData && (
          <DisclaimerBanner
            data={disclaimerData}
            onDismiss={handleDismissDisclaimer}
          />
        )}

        <Header />

        <main className="pt-20">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyze" element={<MealAnalysis />} />
            <Route path="/compare" element={<ComparisonPage />} />
            <Route path="/learn" element={<EducationHub />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>

        <footer className="bg-brand-dark text-white py-12 mt-20">
          <div className="container-responsive text-center">
            <p className="mb-4">
              © 2024 Inside My Meal - Educational Platform
            </p>
            <p className="text-sm text-gray-400 mb-6">
              This is an educational tool only. Not medical advice. Always consult healthcare providers.
            </p>
            <div className="flex justify-center gap-6">
              <a href="/" className="hover:text-brand-primary transition">Privacy</a>
              <a href="/" className="hover:text-brand-primary transition">Terms</a>
              <a href="/" className="hover:text-brand-primary transition">Contact</a>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;

