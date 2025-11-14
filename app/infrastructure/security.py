"""
Security Infrastructure

Provides security utilities including password hashing,
JWT token management, and other cryptographic operations.
"""

import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.infrastructure.config import settings


class PasswordHasher:
    """
    Password hashing utility using bcrypt.
    
    Provides secure password hashing and verification
    with configurable work factor.
    """
    
    @staticmethod
    def hash(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Hashed password string
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Previously hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False


class JWTManager:
    """
    JWT token management utility.
    
    Handles creation, validation, and decoding of JWT tokens
    for authentication and authorization.
    """
    
    @staticmethod
    def create_access_token(
        subject: str,
        expires_delta: Optional[int] = None,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            subject: Subject identifier (usually user ID)
            expires_delta: Token expiration time in minutes
            additional_claims: Optional additional claims to include
            
        Returns:
            Encoded JWT token string
        """
        if expires_delta is None:
            expires_delta = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        
        to_encode = {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access_token"
        }
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def create_refresh_token(subject: str) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            subject: Subject identifier (usually user ID)
            
        Returns:
            Encoded JWT refresh token string
        """
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh_token"
        }
        
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        
        Args:
            token: JWT token string to decode
            
        Returns:
            Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access_token") -> Optional[str]:
        """
        Verify a JWT token and return the subject.
        
        Args:
            token: JWT token string
            token_type: Expected token type
            
        Returns:
            Subject from token if valid, None otherwise
        """
        try:
            payload = JWTManager.decode_token(token)
            
            # Verify token type
            if payload.get("type") != token_type:
                return None
            
            return payload.get("sub")
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if a token is expired.
        
        Args:
            token: JWT token string
            
        Returns:
            True if token is expired, False otherwise
        """
        try:
            payload = JWTManager.decode_token(token)
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                return datetime.utcnow() > datetime.fromtimestamp(exp_timestamp)
            return True
        except jwt.InvalidTokenError:
            return True


class SecurityUtils:
    """Additional security utilities."""
    
    @staticmethod
    def generate_password_reset_token(user_id: str) -> str:
        """Generate a password reset token."""
        return JWTManager.create_access_token(
            subject=user_id,
            expires_delta=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
            additional_claims={"type": "password_reset"}
        )
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """Verify a password reset token and return user ID."""
        try:
            payload = JWTManager.decode_token(token)
            if payload.get("type") != "password_reset":
                return None
            return payload.get("sub")
        except jwt.InvalidTokenError:
            return None