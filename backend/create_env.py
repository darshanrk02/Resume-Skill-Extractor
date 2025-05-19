# Script to create a properly formatted .env file
with open('.env', 'w', encoding='utf-8') as f:
    f.write('MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/resume_extractor?retryWrites=true&w=majority\n')
    f.write('MONGODB_DB_NAME=resume_extractor\n')
 
print("Created .env file - please edit it with your actual MongoDB Atlas credentials")
print("Then run: python check_env.py to verify it's loading correctly") 