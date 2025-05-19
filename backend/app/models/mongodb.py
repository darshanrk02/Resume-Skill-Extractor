import os
from pymongo import MongoClient
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded connection string for MongoDB Atlas (for testing)
# In production, this should be loaded from environment variables
MONGO_URI = "mongodb+srv://darsh:d45lRVKlxWyanKX3@test.rzdc49q.mongodb.net/Resume?retryWrites=true&w=majority"
DB_NAME = "Resume"

logger.info(f"Using MongoDB URI: {MONGO_URI}")
logger.info(f"Using DB name: {DB_NAME}")

try:
    # Create client
    client = MongoClient(MONGO_URI)
    
    # Get database
    db = client[DB_NAME]
    
    # Collections
    resumes_collection = db.resumes  # This will store resume data
    jd_collection = db.job_descriptions  # For job descriptions
    matches_collection = db.matches  # For storing job-resume matches
    
    # Test connection
    client.admin.command('ping')
    logger.info(f"Successfully connected to MongoDB at {MONGO_URI}")
    
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {str(e)}")
    raise

def get_resume_collection():
    """Return the resumes collection."""
    return resumes_collection

def get_jd_collection():
    """Return the job descriptions collection."""
    return jd_collection

def get_matches_collection():
    """Return the matches collection."""
    return matches_collection 