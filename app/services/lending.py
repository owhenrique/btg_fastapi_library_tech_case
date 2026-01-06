from __future__ import annotations

from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.lending import (
    LendingCreate,
    LendingReturn,
    LendingReturnResult,
)
from app.core.exceptions import (
    BookNotAvailable,
    LendingAlreadyExists,
    LendingLimitReached,
    LendingNotFound,
)
from app.models.lending import Lending
from app.repositories.book import BookRepository
from app.repositories.lending import LendingRepository

LENDING_DAYS = 14
FINE_PER_DAY = 2.0
MAX_LENDINGS = 3


class LendingService:
    def __init__(
        self,
        lending_repo: LendingRepository,
        book_repo: BookRepository,
        session: AsyncSession,
    ) -> None:
        self.lending_repo = lending_repo
        self.book_repo = book_repo
        self.session = session

    async def create_lending(self, data: LendingCreate) -> Lending:
        active = await self.lending_repo.get_active_lendings_by_user(
            data.user_id
        )

        if len(active) >= MAX_LENDINGS:
            raise LendingLimitReached()

        if await self.lending_repo.get_lending_by_user_and_book(
            data.user_id, data.book_id
        ):
            raise LendingAlreadyExists()

        book = await self.book_repo.get_by_id(data.book_id)

        if not book or book.available_copies < 1:
            raise BookNotAvailable()

        lending = Lending(
            user_id=data.user_id,
            book_id=data.book_id,
            quantity=1,
            lending_date=datetime.now(),
        )
        book.available_copies -= 1
        self.session.add(lending)
        await self.session.flush()
        await self.session.commit()
        return lending

    async def return_lending(
        self, lending_id: int, data: LendingReturn
    ) -> LendingReturnResult:
        lending = await self.lending_repo.get_lending_by_id(lending_id)

        if not lending or lending.returned_at:
            raise LendingNotFound()

        now = data.returned_at or datetime.now()
        lending.returned_at = now

        due_date = lending.lending_date + timedelta(days=LENDING_DAYS)
        days_late = (now.date() - due_date.date()).days
        fine = FINE_PER_DAY * max(0, days_late)

        book = await self.book_repo.get_by_id(lending.book_id)
        if book:
            book.available_copies += 1
        await self.session.commit()
        return LendingReturnResult(
            lending_id=lending.id, returned_at=now, fine=fine
        )

    async def list_active_lendings(
        self, limit: int = 10, offset: int = 0
    ) -> tuple[Sequence[Lending], int]:
        return await self.lending_repo.list_active_lendings(
            limit=limit, offset=offset
        )

    async def user_lending_history(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> Sequence[Lending]:
        return await self.lending_repo.user_lending_history(
            user_id, limit=limit, offset=offset
        )
