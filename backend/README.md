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
- Database storage for extracted resume data
- RESTful API for frontend integration

## Tech Stack

- Python 3.8+
- FastAPI
- SQLAlchemy (with async support)
- PostgreSQL
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

### 4. Configure Database

Make sure PostgreSQL is installed and running. Create a database named `resume_extractor`:

```bash
createdb resume_extractor
```

Update the `.env` file with your database credentials if needed.

### 5. Run the Application

```bash
python main.py
```

The API will be available at http://localhost:8000

## API Endpoints

- `POST /api/resume/upload` - Upload a resume and extract information
- `POST /api/resume/save` - Save extracted resume data to database
- `DELETE /api/resume/{resume_id}` - Delete a resume
- `POST /api/database/init` - Initialize database tables
- `GET /api/database/status` - Check database connection status

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── routers/          # API route handlers
│   ├── models/           # Database models and schemas
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── uploads/              # Directory for uploaded resumes
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env                  # Environment variables
```
