from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lending import Lending


class LendingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_lending(self, lending: Lending) -> Lending:
        self.session.add(lending)
        await self.session.flush()
        return lending

    async def get_active_lendings_by_user(
        self, user_id: int
    ) -> Sequence[Lending]:
        stmt = select(Lending).where(
            and_(
                Lending.user_id == user_id,
                Lending.returned_at == None,  # noqa: E711
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_lending_by_user_and_book(
        self, user_id: int, book_id: int
    ) -> Optional[Lending]:
        stmt = select(Lending).where(
            and_(
                Lending.user_id == user_id,
                Lending.book_id == book_id,
                Lending.returned_at == None,  # noqa: E711
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_lending_by_id(self, lending_id: int) -> Optional[Lending]:
        stmt = select(Lending).where(Lending.id == lending_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_active_lendings(self) -> Sequence[Lending]:
        stmt = select(Lending).where(Lending.returned_at == None)  # noqa: E711
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def user_lending_history(self, user_id: int) -> Sequence[Lending]:
        stmt = select(Lending).where(Lending.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
