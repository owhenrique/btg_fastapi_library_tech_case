from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_books(self) -> Sequence[Book]:
        stmt = select(Book)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_book(self, book: Book) -> Book:
        self.session.add(book)
        await self.session.flush()
        return book

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
