"""
Ornakala Backend Application Entry Point

This module serves as the main entry point for the Ornakala Backend API.
It provides customer-facing services for jewelry discovery and personalization.
"""

from fastapi import FastAPI
import uvicorn
from typing import Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = "Ornakala Team"

# Initialize FastAPI app
app = FastAPI(
    title="Ornakala Backend",
    description="Backend service for Ornakala's customer platform",
    version=__version__
)

def get_app_info() -> Dict[str, str]:
    """
    Get basic application information.

    Returns:
        Dict[str, str]: Application information including name and version.
    """
    return {
        "name": "Ornakala Backend",
        "version": __version__,
        "description": "Backend service for Ornakala's customer platform",
        "status": "development",
    }

@app.get("/")
async def root():
    """Root endpoint returning application information."""
    logger.info("Root endpoint accessed")
    return get_app_info()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

@app.post("/message")
async def receive_message(message: Dict[str, str]):
    """Endpoint to receive messages."""
    logger.info(f"Received message: {message}")
    return {"status": "received", "message": message}

def main() -> None:
    """Main application entry point."""
    app_info = get_app_info()
    logger.info(f"Starting {app_info['name']} v{app_info['version']}")
    logger.info(f"Status: {app_info['status']}")
    
    # Run the FastAPI application with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()
