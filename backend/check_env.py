import os
from dotenv import load_dotenv

# Load environment variables
print("Loading .env file...")
load_dotenv()

# Check if MongoDB URI is loaded
mongo_uri = os.getenv("MONGODB_URI")
print(f"MONGODB_URI: {mongo_uri}")

# Check if DB name is loaded
db_name = os.getenv("MONGODB_DB_NAME")
print(f"MONGODB_DB_NAME: {db_name}") 