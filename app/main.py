"""
Language Translation API - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Language Translation API",
    description="API for translating text between languages",
    version="1.0.0"
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        dict: Status of the API
    """
    return {"status": "ok"}


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Welcome message and API info
    """
    return {
        "message": "Welcome to Language Translation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
