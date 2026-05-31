# Deployment Guide

This project is deployed as two services:

- Frontend: Vercel
- Backend API: Render
- Database: Render PostgreSQL

The frontend and backend depend on each other's deployed URLs, so deployment is done in two passes.

## 1. Backend Deployment On Render

Create a new Render **Web Service** from the GitHub repository.

Recommended settings:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set the Python version in Render environment variables:

```env
PYTHON_VERSION=3.11.9
```

This is important because Python 3.14 can break `psycopg2-binary`.

Backend environment variables:

```env
DATABASE_URL=<Render PostgreSQL internal database URL>
USDA_API_KEY=<USDA FoodData Central API key>
ADMIN_API_KEY=<strong private admin secret>
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=production
DEBUG=False
```

Use `http://localhost:5173` temporarily for `CORS_ORIGINS` until the frontend is deployed.

After the backend deploys successfully, copy the Render backend URL. It will look like:

```text
https://your-backend-name.onrender.com
```

## 2. Frontend Deployment On Vercel

Create a new Vercel project from the same GitHub repository.

Recommended settings:

```text
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Frontend environment variables:

```env
VITE_API_BASE_URL=https://your-backend-name.onrender.com
```

After Vercel deploys successfully, copy the frontend URL. It will look like:

```text
https://your-frontend-name.vercel.app
```

## 3. Update Backend CORS

Return to the Render backend service and update:

```env
CORS_ORIGINS=https://your-frontend-name.vercel.app
```

Redeploy or restart the backend after changing this value.

If you use multiple frontend URLs, separate them with commas:

```env
CORS_ORIGINS=https://your-frontend-name.vercel.app,https://custom-domain.com
```

## 4. Required External Values

`DATABASE_URL`

Get this from Render PostgreSQL. For a backend running on Render, prefer the internal database URL.

`USDA_API_KEY`

Get a free key from:

```text
https://fdc.nal.usda.gov/api-key-signup.html
```

`ADMIN_API_KEY`

Create this yourself. Use a long random secret from a password manager. This is used for admin login and protected content creation.

`VITE_API_BASE_URL`

Use the Render backend URL.

`CORS_ORIGINS`

Use the Vercel frontend URL.

## 5. Files That Support Deployment

Python runtime pins:

```text
.python-version
backend/.python-version
runtime.txt
backend/runtime.txt
```

These keep Render on Python 3.11.9.

Frontend browser icon:

```text
frontend/public/favicon.svg
```

Environment examples:

```text
backend/.env.example
frontend/.env.example
```

## 6. Local Checks Before Deploying

Frontend:

```powershell
cd C:\Users\asamu\HealthMED\frontend
npm run type-check
npm run build
```

Backend:

```powershell
cd C:\Users\asamu\HealthMED
.\.venv\Scripts\python.exe -m compileall backend
```

Optional local backend run:

```powershell
.\.venv\Scripts\python.exe backend\run.py
```

Optional local frontend run:

```powershell
cd C:\Users\asamu\HealthMED\frontend
npm run dev
```

## 7. Post-Deploy Smoke Test

After both services are deployed:

1. Open the Vercel frontend URL.
2. Confirm the IM favicon appears in the browser tab.
3. Open the Home page.
4. Open Analyze and search for a food.
5. Add a food and run meal analysis.
6. Confirm the glucose chart appears.
7. Open Compare and compare two foods.
8. Open Learn and confirm education cards load.
9. Open `/admin`.
10. Confirm invalid admin login fails.
11. Confirm valid admin login works.
12. Create a test education card if needed.

## 8. Common Render Issues

### Render Uses Python 3.14

Symptom:

```text
Using Python version 3.14.3 (default)
ImportError: psycopg2 ... undefined symbol: _PyInterpreterState_Get
```

Fix:

Set this Render environment variable:

```env
PYTHON_VERSION=3.11.9
```

Then redeploy with:

```text
Clear build cache & deploy
```

### Postgres URL Fails

Render may provide a URL beginning with:

```text
postgres://
```

The app normalizes this to:

```text
postgresql://
```

This is handled in:

```text
backend/app/database.py
```

### CORS Errors In Browser

If frontend requests fail with CORS errors, update the backend `CORS_ORIGINS` value on Render to exactly match the Vercel frontend URL.

Example:

```env
CORS_ORIGINS=https://health-med.vercel.app
```

Then restart/redeploy the backend.

## 9. Release Flow

After deployment is working:

```powershell
git status
git add .
git commit -m "Prepare first release deployment"
git push
git tag v1.0.0
git push origin v1.0.0
```

Create a GitHub release from the `v1.0.0` tag.

Suggested release title:

```text
Inside My Meal v1.0.0 - Educational Preview
```

Suggested release notes:

```text
Initial public release of Inside My Meal.

Includes:
- Meal analysis
- Food search
- Glucose response simulation
- Food comparison
- Education hub
- Admin login for education content creation

This app is educational only and is not medical advice.
```
