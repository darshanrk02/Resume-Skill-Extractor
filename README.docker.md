# Docker Deployment Guide

This guide explains how to deploy the Resume Skill Extractor application using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git (to clone the repository) or the local project files
- MongoDB Atlas account (as we'll be using Atlas exclusively)

## Deployment Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/resume-skill-extractor.git
   cd resume-skill-extractor
   ```

2. Create an environment file with your MongoDB Atlas connection string:

   ```bash
   # Create a .env file with your MongoDB Atlas connection string
   echo "MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority" > .env
   echo "MONGODB_DB_NAME=resume_extractor" >> .env
   ```

   Replace `<username>`, `<password>`, `<cluster>`, and `<database>` with your actual MongoDB Atlas credentials.

3. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Accessing the Application

- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## MongoDB Atlas Setup

1. Create a MongoDB Atlas account if you don't have one: https://www.mongodb.com/cloud/atlas/register
2. Create a new cluster (the free tier is sufficient for getting started)
3. Set up a database user with read/write permissions
4. Add your IP address to the IP access list (or use 0.0.0.0/0 for access from anywhere)
5. Get your connection string from MongoDB Atlas:
   - Click "Connect" on your cluster
   - Select "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user's password
6. Add this connection string to your .env file as shown in the deployment steps

## Troubleshooting

### Checking Container Status

```bash
docker-compose ps
```

### Viewing Container Logs

```bash
# All containers
docker-compose logs

# Specific container
docker-compose logs backend
docker-compose logs frontend
```

### Restarting Services

```bash
docker-compose restart
```

### Stopping and Removing Containers

```bash
docker-compose down
```

### Rebuilding Images

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Common Issues

1. **Connection to MongoDB Atlas fails**:

   - Verify your connection string in the .env file
   - Ensure your IP is whitelisted in MongoDB Atlas
   - Check that your database user has correct permissions

2. **Environment variables not loading**:
   - Make sure your .env file is in the project root
   - Try setting the environment variables directly in docker-compose.yml
