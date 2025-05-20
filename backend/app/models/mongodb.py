import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure
import logging
from pathlib import Path
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get MongoDB connection information from environment variables
MONGO_URI = settings.MONGODB_URI
DB_NAME = settings.MONGODB_DB_NAME

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
    tag_collection = db.tags  # For storing tags
    
    # Create indexes
    try:
        # Create unique index on tag name
        tag_collection.create_index([("name", ASCENDING)], unique=True)
        logger.info("Created unique index on tags.name")
    except OperationFailure as e:
        logger.warning(f"Index creation failed (may already exist): {str(e)}")
    
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

def get_tag_collection():
    """Return the tags collection."""
    return tag_collection 