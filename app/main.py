"""
Language Translation API - Main FastAPI Application

Initializes the FastAPI application, sets up database, and registers routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import create_db_and_tables, settings
from app.api.v1.routes import router as v1_router

# Initialize FastAPI application
app = FastAPI(
    title="Language Translation API",
    description="Professional REST API for translating text between multiple languages with authentication, rate limiting, and history tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    
    Creates database tables on application start.
    """
    create_db_and_tables()


@app.get("/health", tags=["system"])
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        dict: Status of the API and system info
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": settings.environment
    }


@app.get("/", tags=["system"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Welcome message and API info
    """
    return {
        "message": "Welcome to Language Translation API",
        "version": "1.0.0",
        "environment": settings.environment,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "translate": "/api/v1/translate",
            "detect": "/api/v1/detect",
            "history": "/api/v1/history"
        },
        "authentication": "API-Key required in X-API-Key header",
        "rate_limit": f"{settings.rate_limit_per_minute} requests per minute"
    }


# Include API v1 routes
app.include_router(v1_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
