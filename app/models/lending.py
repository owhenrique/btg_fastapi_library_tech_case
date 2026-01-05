from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimeStampMixin
from .book import Book
from .user import User


class Lending(Base, TimeStampMixin):
    """SQLAlchemy model for lendings.

    A Lending records that a user borrowed a quantity of a given book.
    """

    __tablename__ = 'lendings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('books.id'), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    lending_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    returned_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped['User'] = relationship('User', lazy='joined')
    book: Mapped['Book'] = relationship('Book', lazy='joined')

    def apply(self) -> None:
        if self.quantity <= 0:
            raise ValueError('qty must be positive')
        if self.book is None:
            raise ValueError('lending has no associated book instance')
        if self.book.available_copies < self.quantity:
            raise ValueError('not enough copies available to lend')
        self.book.available_copies -= self.quantity

    def mark_returned(self) -> None:
        if self.returned_at is not None:
            raise ValueError('already returned')
        if self.book is None:
            raise ValueError('lending has no associated book instance')
        if self.book.available_copies + self.quantity > self.book.total_copies:
            raise ValueError('return would exceed total copies')
        self.book.available_copies += self.quantity
        self.returned_at = datetime.utcnow()

    @property
    def is_active(self) -> bool:
        return self.returned_at is None
