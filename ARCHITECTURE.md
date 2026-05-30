# Project Architecture

## Overview

Inside My Meal is a full-stack web application for educational visualization of how food affects blood glucose and metabolic health. The architecture follows clean separation of concerns with frontend and backend communicating via REST API.

## Technology Stack

### Frontend
- **React 18**: Modern UI framework with hooks
- **TypeScript**: Type safety and developer experience
- **Tailwind CSS**: Utility-first styling framework
- **Framer Motion**: Smooth animations and interactions
- **Recharts**: Data visualization for glucose curves
- **Zustand**: Lightweight state management
- **Axios**: HTTP client for API communication
- **Vite**: Fast build tool and dev server

### Backend
- **FastAPI**: Modern async Python web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **SQLite**: Lightweight embedded database
- **Httpx**: Async HTTP client for external APIs

### External Services
- **USDA FoodData Central API**: Food composition database
- **Open Food Facts API**: Packaged foods and nutrition labels

## Directory Structure

```
HealthMED/
├── backend/                          # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app initialization
│   │   ├── config.py                # Configuration
│   │   ├── database.py              # Database setup & session management
│   │   ├── models.py                # SQLAlchemy ORM models
│   │   ├── schemas.py               # Pydantic request/response models
│   │   ├── crud.py                  # Database operations
│   │   ├── api/                     # API route modules
│   │   │   ├── foods.py             # Food search & management
│   │   │   ├── meals.py             # Meal creation & queries
│   │   │   ├── simulations.py       # Glucose simulations
│   │   │   └── education.py         # Educational content
│   │   ├── services/                # Business logic
│   │   │   ├── glucose_simulator.py # Glucose calculation engine
│   │   │   └── food_api_service.py  # External API integration
│   │   └── migrations/              # Database initialization
│   │       └── init_db.py           # Seed data
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example
│   ├── run.py                       # Entry point
│   └── tests/                       # Unit tests (placeholder)
│
├── frontend/                         # React application
│   ├── src/
│   │   ├── components/              # Reusable React components
│   │   │   ├── common/              # Header, Footer, etc.
│   │   │   ├── landing/             # Home page components
│   │   │   ├── meal/                # Meal analysis components
│   │   │   ├── animation/           # Animation components
│   │   │   ├── education/           # Education components
│   │   │   └── admin/               # Admin panel
│   │   ├── pages/                   # Page-level components
│   │   │   ├── Home.tsx
│   │   │   ├── MealAnalysis.tsx
│   │   │   ├── ComparisonPage.tsx
│   │   │   ├── EducationHub.tsx
│   │   │   └── Admin.tsx
│   │   ├── services/                # API clients & utilities
│   │   │   ├── api.ts               # API client
│   │   │   └── calculations.ts      # Glucose calculations
│   │   ├── store/                   # Zustand state management
│   │   │   └── useAppStore.ts
│   │   ├── types/                   # TypeScript interfaces
│   │   │   └── index.ts
│   │   ├── App.tsx                  # Main component
│   │   ├── main.tsx                 # React entry point
│   │   └── index.css                # Global styles
│   ├── public/                      # Static assets
│   │   └── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   └── .env.local
│
├── README.md                        # Main documentation
├── SETUP.md                         # Setup instructions
├── API_DOCS.md                      # API documentation
├── ARCHITECTURE.md                  # This file
└── .gitignore
```

## Data Flow

### 1. User Searches for Food

```
Frontend (Search Input)
    ↓
Axios HTTP Request to Backend
    ↓
Backend (GET /api/foods/search)
    ↓
Check Local Cache (SQLite)
    ↓ (If not found)
Query USDA FoodData Central API
    ↓ (If not found)
Query Open Food Facts API
    ↓
Save to Local Cache
    ↓
Return Results to Frontend
    ↓
Frontend (Display Search Results)
```

### 2. User Creates Meal

```
Frontend (Select Foods & Quantities)
    ↓
Zustand State Update + Axios POST
    ↓
Backend (POST /api/meals/)
    ↓
SQLAlchemy ORM Creates Meal & MealItems
    ↓
Calculate Nutrition Totals
    ↓
Return Meal ID
    ↓
Frontend (Display Meal Summary)
```

### 3. User Runs Simulation

```
Frontend (Select Lifestyle Factors)
    ↓
Axios POST with Meal ID + Lifestyle Profile
    ↓
Backend (POST /api/simulations/)
    ↓
Fetch Meal & Nutrition Data from SQLite
    ↓
GlucoseSimulator.simulate_glucose_response()
    ↓
Calculate glucose curve (0, 15, 30, 45, 60, 90, 120 minutes)
    ↓
Apply lifestyle modifiers (walking, sleep, exercise, etc.)
    ↓
Calculate risk scores
    ↓
Generate educational explanations
    ↓
Save Simulation to SQLite
    ↓
Return Results to Frontend
    ↓
Frontend (Display Charts & Explanations)
```

## Database Schema

### Foods Table
Stores food items from external APIs with nutritional information.

```
id (PK)
source: 'usda' | 'openfoodfacts' | 'manual'
source_food_id: unique identifier from source
name: food name
brand: optional brand name
serving_size_g: standard serving size
calories, carbs_g, sugars_g, fiber_g, protein_g, fat_g
glycemic_category: 'low' | 'medium' | 'high'
raw_json: full API response for future reference
created_at, updated_at: timestamps
```

### Meals Table
User meal sessions for analysis.

```
id (PK)
user_session_id: browser session identifier
name: optional meal name (e.g., "Breakfast")
created_at: timestamp
```

### MealItems Table
Individual foods in a meal.

```
id (PK)
meal_id (FK): reference to meal
food_id (FK): reference to food
quantity: number of portions
serving_multiplier: portion size modifier
carbs_g, sugars_g, calories: calculated values
```

### Simulations Table
Glucose simulation results.

```
id (PK)
meal_id (FK): reference to meal
lifestyle_profile: JSON object of lifestyle settings
estimated_peak_mg_dl: calculated peak glucose
glucose_grams_baseline: normal blood glucose
glucose_grams_peak: peak glucose in grams
insulin_load_score: 0-100 score
storage_risk_score: 0-100 score
explanation_json: educational explanation and recommendations
created_at: timestamp
```

### EducationCards Table
Educational content blocks.

```
id (PK)
title: card title
body: card content
animation_type: suggested animation
category: 'basic' | 'advanced' | 'comparison'
sort_order: display order
created_at: timestamp
```

## API Architecture

### Layered Design

```
Frontend (React Components)
    ↓
HTTP Layer (Axios Client)
    ↓
Pydantic Schemas (Request Validation)
    ↓
Route Handlers (/api/...)
    ↓
Business Logic (Services)
    ↓
CRUD Operations (SQLAlchemy)
    ↓
SQLite Database
```

### Key Endpoints

**Foods API**
- `GET /api/foods/search` - Search foods
- `GET /api/foods/{id}` - Get food details
- `POST /api/foods/manual` - Add custom food

**Meals API**
- `POST /api/meals` - Create meal
- `GET /api/meals/{id}` - Get meal details
- `GET /api/meals/user/{session_id}` - Get user meals
- `GET /api/meals/{id}/summary` - Get nutrition summary

**Simulations API**
- `POST /api/simulations` - Run simulation
- `GET /api/simulations/{id}` - Get simulation
- `POST /api/simulations/compare` - Compare meals

**Education API**
- `GET /api/education/cards` - Get education content
- `POST /api/education/cards` - Create card (admin)

## Glucose Simulation Algorithm

The educational glucose simulator uses a simplified model that:

1. **Baseline**: 90 mg/dL (~4.5g glucose in 5L blood)

2. **Absorption** 
   - Carbohydrates → glucose in bloodstream
   - Fiber delays absorption
   - Protein & fat slow stomach emptying

3. **Peak Calculation**
   - Base formula: carbs absorbed ÷ 50 mL/mg = spike
   - Fiber modifier: -25% per 10g fiber
   - Protein modifier: -20% per 30g protein
   - Fat modifier: -15% per 20g fat

4. **Lifestyle Modifiers**
   - Walking: -25% peak reduction
   - Exercise: -15% peak reduction
   - Poor sleep: +20% peak increase
   - Insulin resistance: +40% peak increase
   - Stress: +15% peak increase

5. **Glucose Curve**
   - Exponential rise to peak
   - Exponential decay back to baseline
   - Timepoints: 0, 15, 30, 45, 60, 90, 120 minutes

6. **Risk Scores**
   - Insulin Load: carb-based demand
   - Storage Risk: energy excess + spike + lifestyle

## State Management

### Zustand Store (Frontend)
```typescript
{
  currentUserSessionId,    // Browser session ID
  currentMeal,             // Active meal
  lastSimulation,          // Latest results
  educationCards,          // Educational content
  disclaimersSeen,         // User acknowledgment
}
```

Wrapped in localStorage for persistence.

## Caching Strategy

1. **Database Cache**: All fetched foods are stored in SQLite
2. **Memory Cache**: React component state
3. **Browser Cache**: LocalStorage for session data
4. **API Cache**: USDA results cached before second queries

## Error Handling

### Frontend
- User-friendly error messages
- Network error recovery
- Retry mechanisms
- Fallback content

### Backend
- Pydantic validation errors (400)
- Resource not found errors (404)
- Generic exception handling (500)
- CORS error handling

## Security Considerations

### Current Implementation
- No authentication (educational tool)
- CORS enabled for development
- Input validation via Pydantic
- SQLite constraints

### Production Recommendations
- Add user authentication
- Implement rate limiting
- Use HTTPS
- Add API key validation
- Scan for SQL injection/XSS
- GDPR compliance for user data

## Performance Optimizations

### Frontend
- Lazy loading routes with React Router
- Memoized components
- Virtualized lists for large datasets
- Code splitting with Vite

### Backend
- Database indexes on frequently queried columns
- Connection pooling (SQLAlchemy)
- Async HTTP with httpx
- Caching external API responses
- Query optimization

## Testing Strategy

### Frontend (Not Implemented v1.0)
- Unit tests with Vitest
- Component tests with React Testing Library
- E2E tests with Playwright

### Backend (Not Implemented v1.0)
- Unit tests with pytest
- API tests with FastAPI TestClient
- Integration tests

## Deployment Architecture

### Development
```
Local Machine
├── Backend: http://localhost:8000
└── Frontend: http://localhost:5173
```

### Production (Recommended)
```
Frontend
├── Build: npm run build
└── Host: Vercel, Netlify, AWS S3 + CloudFront

Backend
├── Package: Docker container
├── Database: PostgreSQL (migrate from SQLite)
└── Host: Railway, Heroku, AWS EC2, GCP Cloud Run
```

## Extensibility Points

### Add New Food Data Source
1. Create new parser in `food_api_service.py`
2. Add source type to Food model
3. Update search logic

### Add New Glucose Modifiers
1. Add parameters to `LifestyleProfile`
2. Update `GlucoseSimulator.simulate_glucose_response()`
3. Add UI controls in frontend

### Add User Authentication
1. Add User table to SQLite
2. Add JWT tokens to API
3. Protect endpoints with auth middleware

### Add Personal CGM Integration
1. Connect to CGM APIs (Dexcom, FreeStyle, etc.)
2. Store glucose readings in database
3. Compare with simulator predictions

## Future Enhancements

1. **Multi-language Support**: i18n for international users
2. **User Accounts**: Save preferences & history
3. **Mobile App**: React Native version
4. **Meal Plans**: Curated meal combinations
5. **Community**: Share meals & comparisons
6. **AI Integration**: Personalized recommendations
7. **CGM Integration**: Real glucose data comparison
8. **Nutrition Coaching**: Expert-created content
9. **Supplement Effects**: Modifier for various supplements
10. **Genetic Factors**: Personalization by genetics

## Maintenance

### Regular Tasks
- Update food database monthly
- Monitor API quotas
- Review error logs
- Backup database
- Update dependencies

### Monitoring
- Server uptime
- API response times
- Error rates
- Database size
- API quota usage

## Support & Documentation

- README.md: Overview and quick start
- SETUP.md: Installation guide
- API_DOCS.md: Endpoint documentation
- ARCHITECTURE.md: This file
- Code comments: Inline documentation

