# python
# File: app/domain/usermanagement/password_reset.py
from uuid import UUID
from app.domain.repository import UserRepository
from app.infrastructure.security import PasswordHasher, JWTManager
from jose import JWTError
import re

class InvalidToken(Exception):
    pass

class UserNotFound(Exception):
    pass

class WeakPassword(Exception):
    pass

class PasswordResetService:
    """
    Domain use-case for password recovery:
    - Generates short-lived reset tokens.
    - Validates reset token and updates password via repository.
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @staticmethod
    def _validate_password_strength(password: str) -> None:
        if len(password) < 8:
            raise WeakPassword("password-too-short")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise WeakPassword("password-must-contain-letters-and-numbers")

    def generate_reset_token(self, user_id: UUID, ttl_minutes: int = 60) -> str:
        return JWTManager.create_access_token(str(user_id), expires_delta=ttl_minutes)

    async def reset_password(self, token: str, new_password: str) -> None:
        try:
            payload = JWTManager.decode_token(token)
            user_id = payload.get("sub")
            if not user_id:
                raise InvalidToken("invalid-token")
        except JWTError:
            raise InvalidToken("invalid-token")

        try:
            user_uuid = UUID(user_id)
        except Exception:
            raise InvalidToken("invalid-token")

        user = await self.user_repo.get_by_id(user_uuid)
        if not user:
            raise UserNotFound("user-not-found")

        self._validate_password_strength(new_password)
        hashed = PasswordHasher.hash(new_password)
        await self.user_repo.update_password(user_uuid, hashed)
