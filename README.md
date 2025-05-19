# Resume Skill Extractor

A comprehensive tool that extracts structured data from PDF resumes, matches them against job descriptions, and provides AI-powered recommendations.

## Project Overview

This project consists of two main components:

1. **Frontend**: React.js application with TypeScript and Material-UI
2. **Backend**: Python FastAPI application with NLP capabilities

The frontend and backend are fully integrated with a robust API layer, error handling, and fallback mechanisms for development.

## Features

- PDF Resume Upload & Processing
- Data Extraction (contact info, skills, experience, education)
- Resume Summary View
- Resume-JD Matching
- AI Scoring & Recommendations
- Filtering System

## Tech Stack

### Frontend

- React.js with TypeScript
- Material-UI for components and styling
- React Router for navigation
- Axios for API communication
- Context API for state management

### Backend

- FastAPI (Python)
- MongoDB as NoSQL database
- PyMongo for MongoDB integration
- spaCy and Hugging Face Transformers for NLP
- PyPDF2 and pdfplumber for PDF processing
- CORS middleware for cross-origin requests

## Project Structure

```
resume-skill-extractor/
├── frontend/             # Frontend React application
│   ├── src/              # Frontend source code
│   │   ├── components/   # React components
│   │   │   ├── common/   # Common UI components
│   │   │   ├── layout/   # Layout components
│   │   │   ├── resume/   # Resume-related components
│   │   │   ├── upload/   # File upload components
│   │   │   └── jdmatching/ # Job description matching components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── utils/        # Utility functions
│   │   ├── context/      # React context providers
│   │   ├── config/       # Configuration files
│   │   ├── data/         # Sample data for development
│   │   └── styles/       # Styling and theme configuration
│   ├── public/           # Public assets
│   └── README.md         # Frontend documentation
├── backend/              # Backend FastAPI application
│   ├── app/              # Main application code
│   │   ├── routers/      # API endpoints
│   │   ├── models/       # Data models and MongoDB connection
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   └── requirements.txt  # Python dependencies
└── README.md             # This file
```

## Setup and Installation

### Prerequisites

- Node.js 14+ and npm
- Python 3.8+
- MongoDB (local installation or MongoDB Atlas account)

### Frontend

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The frontend will be available at http://localhost:3000

### Backend

1. Navigate to the backend directory:

   ```
   cd backend
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Set up MongoDB:

   - Option A: Use MongoDB Atlas (Cloud)

     - Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
     - Create a new cluster
     - Add a database user with password
     - Get your connection string

   - Option B: Install MongoDB locally
     - Follow [MongoDB installation guide](https://docs.mongodb.com/manual/installation/)
     - Start the MongoDB service

6. Create a `.env` file in the backend directory with your MongoDB connection:

   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/resume_extractor?retryWrites=true&w=majority
   MONGODB_DB_NAME=Resume
   ```

   Or for local MongoDB:

   ```
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=Resume
   ```

7. Start the backend server:
   ```
   python main.py
   ```
   The API will be available at http://localhost:8000

## Frontend-Backend Integration

### API Services

The frontend communicates with the backend through a set of service modules:

- **api.ts**: Base API configuration with Axios
- **resumeService.ts**: Services for resume upload and management
- **jobDescriptionService.ts**: Services for job description management
- **matchService.ts**: Services for resume-job description matching

### Error Handling

The application implements robust error handling with:

- Standardized error responses
- Fallback to sample data during development
- User-friendly error notifications
- Detailed error logging

### CORS Configuration

The backend is configured to allow cross-origin requests from the frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


