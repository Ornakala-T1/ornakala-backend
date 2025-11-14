from typing import Protocol
from app.domain.repository import UserRepository
from app.domain.models import User
from app.infrastructure.security import PasswordHasher
import re

class EmailAlreadyRegistered(Exception):
    pass

class WeakPassword(Exception):
    pass

class SignupService:
    """
    Domain use-case for user signup/registration.
    - Validates password strength.
    - Ensures email uniqueness via UserRepository.
    - Hashes password and persists new User.
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @staticmethod
    def _validate_password_strength(password: str) -> None:
        if len(password) < 8:
            raise WeakPassword("password-too-short")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise WeakPassword("password-must-contain-letters-and-numbers")

    async def register(self, email: str, password: str) -> User:
        email_norm = email.strip().lower()
        existing = await self.user_repo.get_by_email(email_norm)
        if existing:
            raise EmailAlreadyRegistered("email-already-registered")
        self._validate_password_strength(password)
        hashed = PasswordHasher.hash(password)
        user = User.create(email=email_norm, hashed_password=hashed)
        await self.user_repo.add(user)
        return user
