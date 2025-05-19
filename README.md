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
- SQLAlchemy ORM with PostgreSQL
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
│   │   ├── api/          # API endpoints
│   │   │   └── endpoints/ # API route handlers
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   └── requirements.txt  # Python dependencies
└── README.md             # This file
```

## Setup and Installation

### Prerequisites

- Node.js 14+ and npm
- Python 3.8+
- PostgreSQL database

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

5. Set up the database:
   ```
   # Update database connection details in app/core/config.py
   # Then run the database initialization script (if available)
   python init_db.py
   ```

6. Start the backend server:
   ```
   uvicorn app.main:app --reload --port 8000
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

## API Documentation

Once the backend is running, you can access the Swagger documentation at:

```
http://localhost:8000/docs
```

This provides a complete API reference with request/response examples.

## Design System

The application follows a consistent design system with the following color palette:

- Primary Color: #1f2d3d
- Secondary Color: #4a90e2
- Accent: #50e3c2
- Success: #28a745
- Light Background: #f4f6f9

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
