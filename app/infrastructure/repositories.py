"""
SQLAlchemy User Repository Implementation

Concrete implementation of the UserRepository interface
using SQLAlchemy for data persistence.
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repository import UserRepository
from app.domain.models import User, Email
from app.infrastructure.database import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of UserRepository.
    
    Handles the mapping between domain models and database models.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, user: User) -> None:
        """Add a new user to the database."""
        db_user = self._to_db_model(user)
        self.session.add(db_user)
        await self.session.flush()  # Ensure the user is persisted
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by their ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        return self._to_domain_model(db_user) if db_user else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        stmt = select(UserModel).where(UserModel.email == email.lower())
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        return self._to_domain_model(db_user) if db_user else None
    
    async def update(self, user: User) -> None:
        """Update an existing user."""
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                email=str(user.email),
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                is_verified=user.is_verified,
                first_name=user.first_name,
                last_name=user.last_name,
                updated_at=user.updated_at,
                last_login=user.last_login
            )
        )
        await self.session.execute(stmt)
    
    async def update_password(self, user_id: UUID, hashed_password: str) -> None:
        """Update a user's password."""
        from datetime import datetime
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(hashed_password=hashed_password, updated_at=datetime.utcnow())
        )
        await self.session.execute(stmt)
    
    async def delete(self, user_id: UUID) -> None:
        """Delete a user (hard delete - consider soft delete in production)."""
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(stmt)
    
    async def list_users(
        self,
        limit: int = 100,
        offset: int = 0,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """List users with optional filtering."""
        stmt = select(UserModel)
        
        if is_active is not None:
            stmt = stmt.where(UserModel.is_active == is_active)
        
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        
        return [self._to_domain_model(db_user) for db_user in db_users]
    
    async def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        stmt = select(UserModel.id).where(UserModel.email == email.lower())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    def _to_db_model(self, user: User) -> UserModel:
        """Convert domain model to database model."""
        return UserModel(
            id=user.id,
            email=str(user.email),
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_verified=user.is_verified,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )
    
    def _to_domain_model(self, db_user: UserModel) -> User:
        """Convert database model to domain model."""
        return User(
            id=db_user.id,
            email=Email(db_user.email),
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login
        )

class SQLAlchemyUserKYCRepository(UserKYCRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, kyc: UserKYC) -> None:
        db = self._to_db_model(kyc)
        self.session.add(db)
        await self.session.flush()

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserKYC]:
        stmt = select(UserKYCModel).where(UserKYCModel.user_id == user_id)
        res = await self.session.execute(stmt)
        db = res.scalar_one_or_none()
        return self._to_domain_model(db) if db else None

    async def update(self, kyc: UserKYC) -> None:
        stmt = (
            update(UserKYCModel)
            .where(UserKYCModel.user_id == kyc.user_id)
            .values(
                legal_name=kyc.legal_name,
                document_type=kyc.document_type,
                document_number=kyc.document_number,
                dob=kyc.dob,
                address=kyc.address,
                country=kyc.country,
                status=kyc.status,
                updated_at=datetime.utcnow(),
            )
        )
        await self.session.execute(stmt)

    async def delete_by_user_id(self, user_id: UUID) -> None:
        stmt = delete(UserKYCModel).where(UserKYCModel.user_id == user_id)
        await self.session.execute(stmt)

    async def exists_by_user_id(self, user_id: UUID) -> bool:
        stmt = select(UserKYCModel.id).where(UserKYCModel.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    def _to_db_model(self, kyc: UserKYC) -> UserKYCModel:
        return UserKYCModel(
            id=kyc.id,
            user_id=kyc.user_id,
            legal_name=kyc.legal_name,
            document_type=kyc.document_type,
            document_number=kyc.document_number,
            dob=kyc.dob,
            address=kyc.address,
            country=kyc.country,
            status=kyc.status,
            created_at=kyc.created_at,
            updated_at=kyc.updated_at,
        )

    def _to_domain_model(self, db: UserKYCModel) -> UserKYC:
        return UserKYC(
            id=db.id,
            user_id=db.user_id,
            legal_name=db.legal_name,
            document_type=db.document_type,
            document_number=db.document_number,
            dob=db.dob,
            address=db.address,
            country=db.country,
            status=db.status,
            created_at=db.created_at,
            updated_at=db.updated_at,
        )
