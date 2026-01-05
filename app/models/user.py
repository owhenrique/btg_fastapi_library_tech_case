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
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(Role, name='user_role', native_enum=False),
        nullable=False,
        default=Role.READER,
    )

    def set_password(self, password: str) -> None:
        self.password = hash_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(self.password, password)

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return (
            f'<User id={self.id!r} '
            f'email={self.email!r} '
            f'name={self.name!r} '
            f'role={self.role!r}>'
        )
