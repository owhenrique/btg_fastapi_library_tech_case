from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_books(
        self, limit: int = 10, offset: int = 0
    ) -> tuple[Sequence[Book], int]:
        stmt = select(Book).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count()).select_from(Book)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()
        return items, total

    async def create_book(self, book: Book) -> Book:
        self.session.add(book)
        await self.session.flush()
        return book

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
