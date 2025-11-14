"""
Domain Models

Contains core business entities and value objects following DDD principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import re


@dataclass
class Email:
    """Value object for email addresses with validation."""
    value: str
    
    def __post_init__(self):
        self.value = self.value.strip().lower()
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __str__(self) -> str:
        return self.value


@dataclass
class User:
    """
    User aggregate root representing a platform user.
    
    This is the main entity for user management with complete
    business logic and invariants.
    """
    id: UUID = field(default_factory=uuid4)
    email: Email = None
    hashed_password: str = ""
    is_active: bool = True
    is_verified: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    @classmethod
    def create(
        cls,
        email: str,
        hashed_password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> "User":
        """Factory method to create a new user with proper validation."""
        return cls(
            email=Email(email),
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )
    
    def update_login_timestamp(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.updated_at = datetime.utcnow()
    
    def update_password(self, new_hashed_password: str) -> None:
        """Update user password."""
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()
    
    def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> None:
        """Update user profile information."""
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.updated_at = datetime.utcnow()
    
    @property
    def full_name(self) -> str:
        """Get full name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return ""
    
    def __str__(self) -> str:
        return f"User(id={self.id}, email={self.email})"


@dataclass
class PasswordResetToken:
    """Domain model for password reset tokens."""
    token: str
    user_id: UUID
    expires_at: datetime
    is_used: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def is_expired(self) -> bool:
        """Check if the token is expired."""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if the token is valid (not used and not expired)."""
        return not self.is_used and not self.is_expired()
    
    def mark_as_used(self) -> None:
        """Mark the token as used."""
        self.is_used = True