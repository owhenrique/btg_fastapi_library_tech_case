from __future__ import annotations

from typing import Optional, Sequence

from email_validator import EmailNotValidError, validate_email
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lending import Lending
from app.models.user import Role, User
from app.repositories.user_repository import UserRepository
from app.services.exceptions import (
    EmailAlreadyExists,
    IncorrectPassword,
    InvalidEmail,
    UserNotFound,
)


class UserService:
    def __init__(
        self, repo: UserRepository, session: AsyncSession | None = None
    ) -> None:
        self.repo = repo
        self.session = session

    async def list_users(
        self, limit: int = 100, offset: int = 0
    ) -> Sequence[User]:
        return await self.repo.list_users(limit=limit, offset=offset)

    async def create_user(
        self, name: str, email: str, password: str, role: Role = Role.READER
    ) -> User:
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise InvalidEmail()

        existing = await self.repo.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyExists()

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role
        created = await self.repo.create_user(user)
        if self.session is not None:
            await self.session.commit()
        return created

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound()
        return user

    async def get_user_by_name(self, name: str) -> Optional[User]:
        return await self.repo.get_by_name(name)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repo.get_by_email(email)

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.get_user_by_email(email)
        if user is None:
            raise UserNotFound()
        if not user.check_password(password):
            raise IncorrectPassword()
        return user

    async def list_lendings(self, user_id: int) -> Sequence[Lending]:
        return await self.repo.list_lendings_for_user(user_id)
