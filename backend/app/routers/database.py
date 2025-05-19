from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, init_db

router = APIRouter()

@router.post("/database/init", response_model=dict)
def initialize_database():
    """
    Initialize the database by creating all tables
    """
    try:
        init_db()
        return {"message": "Database initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing database: {str(e)}")

@router.get("/database/status", response_model=dict)
def check_database_status(db: Session = Depends(get_db)):
    """
    Check the status of the database connection
    """
    try:
        # Try to execute a simple query
        result = db.execute("SELECT 1").scalar()
        if result:
            return {"status": "connected", "message": "Database connection is working"}
        else:
            return {"status": "error", "message": "Database connection failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
