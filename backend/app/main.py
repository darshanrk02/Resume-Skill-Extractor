from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routers
from app.routers import resume, database, jd_matching
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Resume Skill Extractor API",
    description="API for resume parsing and job description matching",
    version="1.0.0"
)

# Get allowed origins from settings
origins = settings.get_cors_origins()
logger.info(f"Allowed CORS origins: {origins}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=86400,  # 24 hours
)

# Include routers
app.include_router(resume.router, prefix="/api/v1", tags=["resume"])
app.include_router(database.router, prefix="/api/v1", tags=["database"])
app.include_router(jd_matching.router, prefix="/api/v1", tags=["jd_matching"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up...")
    # Database initialization is handled by models/__init__.py

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint that returns a welcome message."""
    return {
        "message": "Welcome to Resume Skill Extractor API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
