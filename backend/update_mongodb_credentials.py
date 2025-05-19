import os

print("Update your MongoDB Atlas credentials:")
username = input("MongoDB Atlas username: ")
password = input("MongoDB Atlas password: ")
cluster = input("MongoDB Atlas cluster address (e.g. cluster0.xxxxx.mongodb.net): ")
db_name = input("Database name (press Enter for default 'resume_extractor'): ") or "resume_extractor"

# Format the connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority"

# Update the .env file
with open('.env', 'w', encoding='utf-8') as f:
    f.write(f'MONGODB_URI={connection_string}\n')
    f.write(f'MONGODB_DB_NAME={db_name}\n')

print("\nCredentials updated successfully!")
print("Now try running: python main.py") 