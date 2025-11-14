"""
API Routes Module

Centralized router configuration and registration.
"""

from app.api.auth import router as auth_router

__all__ = ["auth_router"]