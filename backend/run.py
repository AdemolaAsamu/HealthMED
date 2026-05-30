"""
Entry point for running the FastAPI server
"""
import uvicorn
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Initialize database before running
from app.migrations.init_db import main as init_database

if __name__ == "__main__":
    print("📊 Inside My Meal Backend")
    print("=" * 50)

    # Initialize database
    print("\n🗄️  Initializing database...")
    init_database()

    # Run server
    print("\n🚀 Starting FastAPI server...")
    print("📍 Available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("=" * 50 + "\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

