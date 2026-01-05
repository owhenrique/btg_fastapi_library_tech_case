from datetime import datetime, timedelta

import pytest

from app.api.v1.schemas.lending import LendingCreate, LendingReturn
from app.core.exceptions import (
    LendingAlreadyExists,
    LendingLimitReached,
)
from app.repositories.book_repository import BookRepository
from app.repositories.lending_repository import LendingRepository
from app.services.lending_service import LendingService

FINE_PER_DAY = 2
FINE_DAYS_LATE = 6
FINE_TOTAL = FINE_PER_DAY * FINE_DAYS_LATE


@pytest.mark.asyncio
async def test_create_lending_success(
    async_session_factory, prepare_db, user_factory, book_factory
):
    async with async_session_factory() as session:
        user = await user_factory()
        book = await book_factory(total_copies=2)
        lending_repo = LendingRepository(session)
        book_repo = BookRepository(session)
        service = LendingService(
            lending_repo=lending_repo,
            book_repo=book_repo,
            session=session,
        )
        data = LendingCreate(user_id=user.id, book_id=book.id)
        lending = await service.create_lending(data)
        assert lending.user_id == user.id
        assert lending.book_id == book.id

        updated_book = await book_repo.get_by_id(book.id)
        assert updated_book.available_copies == 1


@pytest.mark.asyncio
async def test_lending_limit(
    async_session_factory, prepare_db, user_factory, book_factory
):
    async with async_session_factory() as session:
        user = await user_factory()
        books = [await book_factory() for _ in range(3)]
        lending_repo = LendingRepository(session)
        book_repo = BookRepository(session)
        service = LendingService(
            lending_repo=lending_repo,
            book_repo=book_repo,
            session=session,
        )
        for book in books:
            await service.create_lending(
                LendingCreate(user_id=user.id, book_id=book.id)
            )
        with pytest.raises(LendingLimitReached):
            await service.create_lending(
                LendingCreate(user_id=user.id, book_id=books[0].id)
            )


@pytest.mark.asyncio
async def test_lending_already_exists(
    async_session_factory, prepare_db, user_factory, book_factory
):
    async with async_session_factory() as session:
        user = await user_factory()
        book = await book_factory()
        lending_repo = LendingRepository(session)
        book_repo = BookRepository(session)
        service = LendingService(
            lending_repo=lending_repo,
            book_repo=book_repo,
            session=session,
        )
        await service.create_lending(
            LendingCreate(user_id=user.id, book_id=book.id)
        )
        with pytest.raises(LendingAlreadyExists):
            await service.create_lending(
                LendingCreate(user_id=user.id, book_id=book.id)
            )


@pytest.mark.asyncio
async def test_return_lending_success(
    async_session_factory, prepare_db, user_factory, book_factory
):
    async with async_session_factory() as session:
        user = await user_factory()
        book = await book_factory()
        lending_repo = LendingRepository(session)
        book_repo = BookRepository(session)
        service = LendingService(
            lending_repo=lending_repo,
            book_repo=book_repo,
            session=session,
        )
        lending = await service.create_lending(
            LendingCreate(user_id=user.id, book_id=book.id)
        )
        result = await service.return_lending(
            lending.id, LendingReturn(returned_at=datetime.now())
        )
        assert result.lending_id == lending.id
        assert result.fine == 0


@pytest.mark.asyncio
async def test_return_lending_with_fine(
    async_session_factory, prepare_db, user_factory, book_factory
):
    async with async_session_factory() as session:
        user = await user_factory()
        book = await book_factory()
        lending_repo = LendingRepository(session)
        book_repo = BookRepository(session)
        service = LendingService(
            lending_repo=lending_repo,
            book_repo=book_repo,
            session=session,
        )
        lending = await service.create_lending(
            LendingCreate(user_id=user.id, book_id=book.id)
        )
        late_date = lending.lending_date + timedelta(days=20)
        result = await service.return_lending(
            lending.id, LendingReturn(returned_at=late_date)
        )
        assert result.fine == FINE_TOTAL  # 6 dias de atraso x 2 reais
