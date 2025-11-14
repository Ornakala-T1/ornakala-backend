"""
API Dependencies

FastAPI dependencies for authentication, database sessions, and other common functionality.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_session
from app.infrastructure.repositories import SQLAlchemyUserRepository
from app.infrastructure.security import JWTManager
from app.domain.usermanagement.login import LoginService
from app.domain.usermanagement.signup import SignupService
from app.domain.usermanagement.password_reset import PasswordResetService
from app.domain.repository import UserRepository
from app.domain.models import User
from typing import Optional

# Security
security = HTTPBearer(auto_error=False)


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    """Dependency for getting user repository."""
    return SQLAlchemyUserRepository(session)


async def get_login_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> LoginService:
    """Dependency for getting login service."""
    return LoginService(user_repo)


async def get_signup_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> SignupService:
    """Dependency for getting signup service."""
    return SignupService(user_repo)


async def get_password_reset_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> PasswordResetService:
    """Dependency for getting password reset service."""
    return PasswordResetService(user_repo)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    user_repo: UserRepository = Depends(get_user_repository)
) -> Optional[User]:
    """
    Get current user from JWT token (optional).
    Returns None if no token or invalid token.
    """
    if not credentials:
        return None
    
    try:
        user_id = JWTManager.verify_token(credentials.credentials)
        if not user_id:
            return None
        
        from uuid import UUID
        return await user_repo.get_by_id(UUID(user_id))
    except Exception:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    """
    Get current user from JWT token (required).
    Raises 401 if no token or invalid token.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = JWTManager.verify_token(credentials.credentials)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        from uuid import UUID
        user = await user_repo.get_by_id(UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is deactivated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )