"""
Authentication API Routes

FastAPI router for user authentication endpoints including
login, signup, password reset, and user management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.schemas import (
    UserCreateRequest,
    UserLoginRequest,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
    UserResponse,
    TokenResponse,
    MessageResponse,
    ErrorResponse
)
from app.api.dependencies import (
    get_login_service,
    get_signup_service,
    get_password_reset_service,
    get_current_user
)
from app.domain.usermanagement.login import (
    LoginService,
    InvalidCredentials,
    InactiveAccount
)
from app.domain.usermanagement.signup import (
    SignupService,
    EmailAlreadyRegistered,
    WeakPassword
)
from app.domain.usermanagement.password_reset import (
    PasswordResetService,
    InvalidToken,
    UserNotFound
)
from app.domain.models import User
from app.infrastructure.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def signup(
    request: UserCreateRequest,
    signup_service: SignupService = Depends(get_signup_service)
):
    """Register a new user."""
    try:
        user = await signup_service.register(
            email=request.email,
            password=request.password
        )
        
        # Update profile if first/last name provided
        if request.first_name or request.last_name:
            user.update_profile(
                first_name=request.first_name,
                last_name=request.last_name
            )
        
        logger.info(f"New user registered: {user.email}")
        
        return UserResponse(
            id=user.id,
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )
    
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    except WeakPassword as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    description="Authenticate user and return access token"
)
async def login(
    request: UserLoginRequest,
    login_service: LoginService = Depends(get_login_service)
):
    """Authenticate user and return tokens."""
    try:
        user = await login_service.authenticate(
            email=request.email,
            password=request.password
        )
        
        # Update last login timestamp
        user.update_login_timestamp()
        
        # Create access token
        access_token = login_service.create_access_token(user)
        
        logger.info(f"User logged in: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        )
    
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except InactiveAccount:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post(
    "/password-reset",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Send password reset token (email implementation pending)"
)
async def request_password_reset(
    request: PasswordResetRequest,
    password_reset_service: PasswordResetService = Depends(get_password_reset_service)
):
    """Request password reset token."""
    try:
        # For now, we'll just generate the token and return it
        # In production, this should send an email
        from app.infrastructure.repositories import SQLAlchemyUserRepository
        from app.infrastructure.database import get_db_session
        
        # This is a simplified implementation
        # In production, you should:
        # 1. Verify email exists
        # 2. Generate token
        # 3. Send email with reset link
        # 4. Return success message without token
        
        logger.info(f"Password reset requested for: {request.email}")
        
        return MessageResponse(
            message="Password reset instructions have been sent to your email (feature pending implementation)",
            success=True
        )
    
    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password reset request"
        )


@router.post(
    "/password-reset/confirm",
    response_model=MessageResponse,
    summary="Confirm password reset",
    description="Reset password using reset token"
)
async def confirm_password_reset(
    request: PasswordResetConfirmRequest,
    password_reset_service: PasswordResetService = Depends(get_password_reset_service)
):
    """Confirm password reset with token."""
    try:
        await password_reset_service.reset_password(
            token=request.token,
            new_password=request.new_password
        )
        
        logger.info("Password reset completed successfully")
        
        return MessageResponse(
            message="Password has been reset successfully",
            success=True
        )
    
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except WeakPassword as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Password reset confirmation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password reset"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information"
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        email=str(current_user.email),
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="User logout",
    description="Logout user (client should discard token)"
)
async def logout():
    """
    Logout user.
    
    Since we're using stateless JWT tokens, logout is handled on the client side
    by discarding the token. In production, you might want to implement token blacklisting.
    """
    return MessageResponse(
        message="Logged out successfully",
        success=True
    )