import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the FastAPI application
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
