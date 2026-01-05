from __future__ import annotations

from enum import StrEnum
from typing import Optional

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimeStampMixin


class BookCategoryEnum(StrEnum):
    FICTION = 'fiction'
    NONFICTION = 'nonfiction'
    TECH = 'tech'
    OTHER = 'other'


class Book(Base, TimeStampMixin):
    """SQLAlchemy model for books."""

    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    total_copies: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    available_copies: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    category: Mapped[BookCategoryEnum] = mapped_column(
        SAEnum(BookCategoryEnum, name='book_category', native_enum=False),
        nullable=False,
    )

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return (
            f'<Book id={self.id!r} name={self.name!r} author={self.author!r} '
            f'category={self.category!r} total_copies={self.total_copies!r} '
            f'available_copies={self.available_copies!r}>'
        )

    def __init__(self, *args, **kwargs):
        # Ensure sensible Python-level defaults before persistence
        super().__init__(*args, **kwargs)
        if getattr(self, 'total_copies', None) is None:
            self.total_copies = 1
        if getattr(self, 'available_copies', None) is None:
            self.available_copies = self.total_copies

    def lending(self, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError('qty must be positive')
        if self.available_copies < qty:
            raise ValueError('not enough copies available to lend')
        self.available_copies -= qty

    def return_copy(self, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError('qty must be positive')
        if self.available_copies + qty > self.total_copies:
            raise ValueError('return would exceed total copies')
        self.available_copies += qty

    def add_copies(self, qty: int = 1) -> None:
        """
        Add `qty` new copies to the library (increases total and available).
        """
        if qty <= 0:
            raise ValueError('qty must be positive')
        self.total_copies += qty
        self.available_copies += qty
