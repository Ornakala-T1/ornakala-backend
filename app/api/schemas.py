"""
API Request and Response Models

Pydantic models for API request/response validation and serialization.
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserCreateRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


class PasswordResetRequest(BaseModel):
    """Request model for password reset initiation."""
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    """Request model for password reset confirmation."""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(BaseModel):
    """Response model for user data."""
    id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Response model for authentication tokens."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class MessageResponse(BaseModel):
    """Generic message response model."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    success: bool = False