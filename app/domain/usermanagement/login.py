# python
# File: app/domain/usermanagement/login.py
from app.domain.repository import UserRepository
from app.domain.models import User
from app.infrastructure.security import PasswordHasher, JWTManager

class InvalidCredentials(Exception):
    pass

class InactiveAccount(Exception):
    pass

class LoginService:
    """
    Domain use-case for authentication.
    - Verifies credentials.
    - Optionally produces access tokens (delegates to JWTManager).
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate(self, email: str, password: str) -> User:
        email_norm = email.strip().lower()
        user = await self.user_repo.get_by_email(email_norm)
        if not user or not PasswordHasher.verify(password, user.hashed_password):
            raise InvalidCredentials("invalid-credentials")
        if not user.is_active:
            raise InactiveAccount("account-inactive")
        return user

    def create_access_token(self, user: User, expires_minutes: int = None) -> str:
        # JWTManager.create_access_token expects minutes for expires_delta
        if expires_minutes is None:
            return JWTManager.create_access_token(str(user.id))
        return JWTManager.create_access_token(str(user.id), expires_delta=expires_minutes)
