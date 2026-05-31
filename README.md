# Inside My Meal - Full Stack Educational Application
# Blood Sugar & Metabolic Health Education Platform

## Project Overview

"Inside My Meal" is an interactive, animated educational website that helps users visually understand how food affects:
- Blood sugar levels
- Insulin response
- Energy storage
- Lifestyle impact
- Weight gain risk
- Fatty liver risk
- Long-term metabolic health

**Important**: This is strictly an educational tool, NOT medical advice or diagnostic tool.

Fat-storage values are energy-equivalent estimates only. They do not predict personal body-fat gain,
and the avatar is an educational representation rather than a medical or legal digital twin.

## Features

### 1. Landing Page
- Animated bloodstream with 1 teaspoon glucose visualization
- Strong headline: "Your blood only carries about 1 teaspoon of sugar. So what happens when you eat 10 teaspoons?"
- CTA: "Analyze a meal"

### 2. Meal Analyzer
- Search foods from USDA and Open Food Facts databases
- Add multiple foods with portion size adjustment
- Display nutrition summary: total sugar, carbs, fiber, calories

### 3. Glucose Animation
- Baseline blood glucose visualization (~4.5g)
- Animated glucose load entering digestion
- Estimated glucose rise and insulin response
- Show glucose distribution: immediate energy, muscle glycogen, liver glycogen, fat storage
- Educational potential fat-storage equivalent range when a meal may create surplus energy
- Non-identifying metabolic avatar that visualizes response state without storing biometric identity

### 4. Lifestyle Modifiers
- Sedentary vs. active
- Post-meal walking (10-20 minutes)
- Regular exercise routine
- Sleep quality
- Stress levels
- Muscle mass
- Insulin resistance mode
- Fiber content
- Protein-first meal order

### 5. Educational Content
- Sugar vs. carbohydrate differences
- Juice vs. whole fruit comparison
- Fiber importance
- Post-meal movement benefits
- Sedentary lifestyle risks
- Repeated excess energy impact

### 6. Compare Foods
- Side-by-side food comparisons
- Different meal compositions
- Before/after lifestyle impacts

### 7. Admin Panel
- Add educational content
- Manage curated food examples

## Tech Stack

### Frontend
- **React 18** + **TypeScript**
- **Tailwind CSS** (styling)
- **Framer Motion** (animations)
- **Recharts** (charts)
- **Axios** (HTTP client)
- **Zustand** (state management)

### Backend
- **FastAPI** (Python web framework)
- **SQLAlchemy** (ORM)
- **SQLite** (database)
- **Pydantic** (data validation)
- **Httpx** (async HTTP client)

### External APIs
- **USDA FoodData Central API** - Food composition data
- **Open Food Facts API** - Packaging, barcode, ingredients

## Project Structure

```
HealthMED/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── foods.py
│   │   │   ├── meals.py
│   │   │   ├── simulations.py
│   │   │   └── education.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── food_api_service.py
│   │   │   └── glucose_simulator.py
│   │   └── migrations/
│   │       └── init_db.py
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── landing/
│   │   │   │   └── BloodstreamAnimation.tsx
│   │   │   └── common/
│   │   │       ├── Header.tsx
│   │   │       └── DisclaimerBanner.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── MealAnalysis.tsx
│   │   │   ├── ComparisonPage.tsx
│   │   │   ├── EducationHub.tsx
│   │   │   └── Admin.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── calculations.ts
│   │   ├── store/
│   │   │   └── useAppStore.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── .env.example
│   └── vite.config.ts
├── README.md
├── API_DOCS.md
├── ARCHITECTURE.md
├── SETUP.md
└── main.py
```

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.9+
- pip

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Initialize database:
```bash
python -m app.migrations.init_db
```

6. Run server:
```bash
python run.py
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```
VITE_API_BASE_URL=http://localhost:8000
```

4. Run development server:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./app.db
USDA_API_KEY=your_usda_key_here
ADMIN_API_KEY=change-me
ENVIRONMENT=development
DEBUG=True
```

### Frontend (.env.local)
```
VITE_API_BASE_URL=http://localhost:8000
```

## Database Schema

### foods
Stores food items from external APIs with nutritional information

### meals
User meal sessions

### meal_items
Individual foods that make up a meal

### simulations
Glucose simulation results based on meal and lifestyle

### education_cards
Educational content blocks

## Medical/Legal Disclaimer

This application is for **educational purposes only** and does NOT:
- Provide medical diagnosis
- Provide medical treatment advice
- Replace consultation with healthcare providers
- Claim exact personal glucose response accuracy
- Recommend specific dietary changes

Language used:
- "may contribute to"
- "can increase risk"
- "estimated"
- "educational only"

Special disclaimers for:
- Diabetes/prediabetes: Consult healthcare provider
- Children/pregnancy: Consult healthcare provider
- Eating disorders: Seek professional help

## API Documentation

### Food Search
`GET /api/foods/search?query=apple`

### Create Meal Analysis
`POST /api/meals/`

### Get Glucose Simulation
`POST /api/simulations/`

### Get Education Cards
`GET /api/education/cards`

## Data Sources

1. **USDA FoodData Central API**
   - https://fdc.nal.usda.gov/
   - Provides comprehensive food composition database

2. **Open Food Facts API**
   - https://world.openfoodfacts.org/
   - Packaged foods, barcodes, ingredients

## Simulation Model

### Baseline Calculation
- Blood volume: 5 liters
- Normal fasting glucose: 90 mg/dL
- Glucose in blood = mg/dL × 50 dL / 1000
  - 90 mg/dL = 4.5g
  - 140 mg/dL = 7g
  - 180 mg/dL = 9g

### Modifiers
- **Fiber**: Reduces spike by 20-40%
- **Protein/Fat**: Slows absorption by 30-50%
- **Walking After**: Reduces peak by 20-30%, improves clearance
- **Exercise**: Improves insulin sensitivity by 15-25%
- **Poor Sleep**: Increases spike risk by 15-20%
- **Sedentary**: Increases storage risk by 25-40%
- **Insulin Resistance**: Increases peak by 25-50%

## Contributing

This is an educational visualization tool. All contributions should maintain:
- Scientific accuracy
- Appropriate medical language and disclaimers
- Educational value
- No fearmongering
- Support for different body types and metabolic states

## License

MIT

---

**Built with care to demystify nutrition and metabolic health.**

