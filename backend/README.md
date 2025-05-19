# Resume Skill Extractor - Backend

This is the backend API for the Resume Skill Extractor application, built with FastAPI and Python.

## Features

- PDF resume upload and processing
- Extraction of key information from resumes:
  - Contact information
  - Skills
  - Education
  - Work experience
  - Projects
- MongoDB database storage for extracted resume data
- RESTful API for frontend integration

## Tech Stack

- Python 3.8+
- FastAPI
- MongoDB with PyMongo
- PyPDF2 and pdfplumber for PDF processing
- spaCy and NLTK for NLP

## Setup Instructions

### 1. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 4. Configure MongoDB

You have two options for MongoDB:

#### Option A: Use MongoDB Atlas (Cloud Database)

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Set up a database user with password
4. Get your connection string from MongoDB Atlas dashboard
5. Create a `.env` file in the backend directory:

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/resume_extractor?retryWrites=true&w=majority
MONGODB_DB_NAME=Resume
```

Replace `<username>`, `<password>`, and `<cluster>` with your MongoDB Atlas credentials.

#### Option B: Use Local MongoDB Instance

1. Install MongoDB locally following the [official instructions](https://docs.mongodb.com/manual/installation/)
2. Start the MongoDB service
3. Create a `.env` file in the backend directory:

```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=Resume
```

### 5. Run the Application

```bash
python main.py
```

The API will be available at http://localhost:8000

## API Endpoints

- `POST /api/v1/resume/upload` - Upload a resume and extract information
- `POST /api/v1/resume/save` - Save extracted resume data to MongoDB
- `GET /api/v1/resumes` - Get all resumes
- `GET /api/v1/resumes/{resume_id}` - Get a specific resume
- `DELETE /api/v1/resumes/{resume_id}` - Delete a resume

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── routers/          # API route handlers
│   ├── models/           # Database models and schemas
│   │   └── mongodb.py    # MongoDB connection
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── uploads/              # Directory for uploaded resumes
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env                  # Environment variables
```
