"""
Repository Interfaces

Defines the contracts for data persistence following the Repository pattern.
These interfaces are implemented by the infrastructure layer.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.models import User


class UserRepository(ABC):
    """
    Repository interface for User aggregate.
    
    Defines all data access operations for users without
    specifying the implementation details.
    """
    
    @abstractmethod
    async def add(self, user: User) -> None:
        """Add a new user to the repository."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by their ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> None:
        """Update an existing user."""
        pass
    
    @abstractmethod
    async def update_password(self, user_id: UUID, hashed_password: str) -> None:
        """Update a user's password."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Delete a user (soft delete recommended)."""
        pass
    
    @abstractmethod
    async def list_users(
        self,
        limit: int = 100,
        offset: int = 0,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """List users with optional filtering."""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        pass


class UnitOfWork(ABC):
    """
    Unit of Work pattern interface for managing transactions.
    
    Ensures data consistency across multiple repository operations.
    """
    
    @abstractmethod
    async def __aenter__(self):
        """Enter the context manager and begin transaction."""
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager and handle transaction."""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        pass
    
    @property
    @abstractmethod
    def users(self) -> UserRepository:
        """Get the user repository instance."""
        pass