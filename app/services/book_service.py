from __future__ import annotations

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.book import BookAvailability, BookCreate
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.services.exceptions import (
    BookAlreadyExists,
    BookNotFound,
    InvalidBookData,
)


class BookService:
    def __init__(
            self, repo: BookRepository, session: AsyncSession | None = None
        ) -> None:
        self.repo = repo
        self.session = session

    async def list_books(self) -> Sequence[Book]:
        return await self.repo.list_books()

    async def create_book(self, data: BookCreate) -> Book:
        if not data.name or not data.category:
            raise InvalidBookData(detail='Name and category are required')
        if data.total_copies < 1:
            raise InvalidBookData(detail='Total copies must be at least 1')

        books = await self.repo.list_books()
        for b in books:
            if b.name == data.name and b.author == data.author:
                raise BookAlreadyExists()
        book = Book(
            name=data.name,
            author=data.author,
            total_copies=data.total_copies,
            available_copies=data.total_copies,
            category=data.category,
        )
        book = await self.repo.create_book(book)
        if self.session is not None:
            await self.session.commit()
        return book

    async def check_availability(self, book_id: int) -> BookAvailability:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise BookNotFound()
        return BookAvailability(
            book_id=book.id,
            available_copies=book.available_copies,
            is_available=book.available_copies > 0,
        )
