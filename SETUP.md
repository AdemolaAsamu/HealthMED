# Setup and Installation Guide

## Project Overview

Inside My Meal is a full-stack web application built with:
- **Frontend**: React 18 + TypeScript + Tailwind CSS + Framer Motion
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **APIs**: USDA FoodData Central, Open Food Facts

## System Requirements

- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- npm or yarn
- pip
- Git (optional)

## Backend Setup

### 1. Navigate to backend directory

```bash
cd backend
```

### 2. Create and activate virtual environment

**On Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

```bash
cp .env.example .env
```

Edit `.env` and add your USDA API key (get free key at https://api.nal.usda.gov/):

```
DATABASE_URL=sqlite:///./app.db
USDA_API_KEY=your_actual_key_here
ADMIN_API_KEY=change-me
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 5. Initialize database

```bash
python run.py
```

This will:
- Create database tables
- Seed 20+ common foods
- Seed 13 educational cards
- Start the FastAPI server

The server will run at: http://localhost:8000

## Frontend Setup

### 1. Navigate to frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Create environment file

```bash
cp .env.example .env.local
```

Or create `.env.local` manually:
```
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Start development server

```bash
npm run dev
```

The application will run at: http://localhost:5173

## Running Both Servers

You'll need two terminal windows/tabs:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
python run.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## API Documentation

Once the backend is running, access API docs at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Database

SQLite database file: `backend/app.db`

To reset the database:
1. Delete `backend/app.db`
2. Run `python run.py` again

## Common Issues

### Port Already in Use

**Backend (Port 8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 5173):**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5173 | xargs kill -9
```

### CORS Errors

Make sure `CORS_ORIGINS` in backend `.env` includes your frontend URL:
```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
```

### USDA API Not Working

- Verify your API key in `.env`
- Test at https://api.nal.usda.gov/
- If using DEMO_KEY, only limited results will work
- Get your free key at https://api.nal.usda.gov/

### Vite Dev Server Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Building for Production

### Backend

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Frontend

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

## Database Schema

### foods
- id, source, source_food_id, name, brand
- serving_size_g, calories, carbs_g, sugars_g, fiber_g, protein_g, fat_g
- glycemic_category, raw_json, created_at, updated_at

### meals
- id, user_session_id, name, created_at

### meal_items
- id, meal_id, food_id, quantity, serving_multiplier
- carbs_g, sugars_g, calories

### simulations
- id, meal_id, lifestyle_profile (JSON)
- estimated_peak_mg_dl, glucose_grams_baseline, glucose_grams_peak
- insulin_load_score, storage_risk_score
- explanation_json, created_at

### education_cards
- id, title, body, animation_type, category, sort_order, created_at

## Environment Variables

### Backend

```
DATABASE_URL=sqlite:///./app.db
USDA_API_KEY=your_key_here
ADMIN_API_KEY=change-me
ENVIRONMENT=development/production
DEBUG=True/False
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend

```
VITE_API_BASE_URL=http://localhost:8000
```

## File Structure

```
HealthMED/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── crud.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── run.py
│   ├── .env.example
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── types/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   └── .env.local
└── README.md
```

## Troubleshooting

### Backend won't start

1. Check Python version: `python --version` (needs 3.9+)
2. Verify virtual environment is activated
3. Check all requirements installed: `pip list`
4. Clear database and reinitialize: delete `app.db` and run `python run.py`

### Frontend build fails

1. Clear node_modules: `rm -rf node_modules && npm install`
2. Check Node version: `node --version` (needs 18+)
3. Check for TypeScript errors: `npm run type-check`

### API calls returning 401/403

1. Check CORS_ORIGINS in backend .env
2. Verify frontend is using correct API_BASE_URL
3. Restart both services after changing environment variables

### Slow food search

1. First time searches hit external APIs (slower)
2. Results are cached in local database for faster subsequent searches
3. USDA API default has Demo Key - get your own for better performance

## Next Steps

1. Get a free USDA API key at https://api.nal.usda.gov/
2. Add more food items to database
3. Create curated meal plans
4. Add user authentication (not included in v1.0)
5. Deploy to cloud platform (Heroku, Vercel, Railway, etc.)

## Support

For issues or questions:
1. Check the main README.md
2. Review API documentation at http://localhost:8000/docs
3. Check console logs for error messages
4. Verify all environment variables are set correctly

