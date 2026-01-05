from __future__ import annotations

from enum import StrEnum

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.security import hash_password, verify_password

from .base import Base, TimeStampMixin


class Role(StrEnum):
    ADMIN = 'admin'
    LIBRARIAN = 'librarian'
    READER = 'reader'


class User(Base, TimeStampMixin):
    """SQLAlchemy model for users."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(Role, name='user_role', native_enum=False),
        nullable=False,
        default=Role.READER,
    )

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password by delegating to the security module.
        """
        self.password = hash_password(password)

    def check_password(self, password: str) -> bool:
        """
        Verify the provided password by delegating to the security module.
        """
        return verify_password(self.password, password)

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return f'<User id={self.id!r} name={self.name!r} role={self.role!r}>'
