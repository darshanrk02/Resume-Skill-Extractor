#!/bin/bash

# Script to set up MongoDB Atlas connection for the Resume Skill Extractor

echo "MongoDB Atlas Setup Script"
echo "=========================="
echo ""
echo "This script will help you configure your application to use MongoDB Atlas."
echo ""

# Ask for MongoDB Atlas connection details
read -p "Enter your MongoDB Atlas Connection String (mongodb+srv://...): " MONGODB_URI
read -p "Enter your MongoDB Database Name [resume_extractor]: " MONGODB_DB_NAME
MONGODB_DB_NAME=${MONGODB_DB_NAME:-resume_extractor}

# Create .env file
echo "Creating .env file..."
echo "MONGODB_URI=$MONGODB_URI" > .env
echo "MONGODB_DB_NAME=$MONGODB_DB_NAME" >> .env
echo "PORT=8000" >> .env

echo ""
echo "Configuration complete! Your .env file has been created with the following settings:"
echo "------------------------------------------------------------------------------"
echo "MONGODB_URI=$MONGODB_URI"
echo "MONGODB_DB_NAME=$MONGODB_DB_NAME"
echo "PORT=8000"
echo "------------------------------------------------------------------------------"
echo ""
echo "You can now run 'docker-compose up -d' to start the application using MongoDB Atlas." 