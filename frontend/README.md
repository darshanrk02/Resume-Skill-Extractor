# Resume Skill Extractor - Frontend

This is the frontend application for the Resume Skill Extractor project, built with React, TypeScript, and Material-UI.

## Features

- PDF resume upload with drag-and-drop functionality
- Resume summary view with structured information display
- Job description input and matching analysis
- Visual representation of match percentage and skills
- AI recommendation display

## Tech Stack

- React.js with TypeScript
- Material-UI for components and styling
- React Router for navigation

## Getting Started

### Prerequisites

- Node.js 14+ and npm

### Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```
   The application will be available at http://localhost:3000

### Building for Production

To build the application for production:

```
npm run build
```

This will create a `build` directory with optimized production files.

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── layout/           # Layout components (Header, Layout)
│   ├── upload/           # PDF upload components
│   ├── resume/           # Resume display components
│   └── jdmatching/       # Job description matching components
├── pages/                # Page components
├── styles/               # Styling and theme configuration
├── types/                # TypeScript type definitions
└── App.tsx               # Main application component
```

## Integration with Backend

The frontend communicates with the FastAPI backend through RESTful API calls. The backend handles:

- PDF processing and text extraction
- Skills and information extraction using NLP
- Resume-job description matching
- Data storage and retrieval

Make sure the backend server is running at http://localhost:8000 for the frontend to function properly.
