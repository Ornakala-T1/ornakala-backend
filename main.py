"""
Ornakala Backend Application Entry Point

This module serves as the main entry point for the Ornakala Backend API.
It provides customer-facing services for jewelry discovery and personalization.
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import auth_router
from app.infrastructure.database import DatabaseManager
from app.infrastructure.config import Settings
import logging

__version__ = "1.0.0"
__author__ = "Ornakala Team"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Starting Ornakala Backend API...")
    await DatabaseManager.initialize()
    logger.info("Database initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down Ornakala Backend API...")
    await DatabaseManager.close()
    logger.info("Database connections closed")

def create_app() -> FastAPI:
    """Application factory function."""
    app = FastAPI(
        title="Ornakala Backend API",
        description="Backend service for Ornakala's customer platform",
        version=__version__,
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": __version__,
            "service": "Ornakala Backend"
        }

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "name": "Ornakala Backend",
            "version": __version__,
            "description": "Backend service for Ornakala's customer platform",
            "docs": "/docs",
            "health": "/health"
        }

    return app

app = create_app()

def main() -> None:
    """Main application entry point."""
    logger.info(f"Starting Ornakala Backend v{__version__}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()
