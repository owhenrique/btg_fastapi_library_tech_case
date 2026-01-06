import pytest

from app.models.lending import Lending
from app.repositories.lending import LendingRepository

USER_ID_1 = 1
USER_ID_2 = 2
USER_ID_3 = 3
USER_ID_4 = 4
USER_ID_5 = 5
USER_ID_6 = 6
BOOK_ID_1 = 1
BOOK_ID_2 = 2
BOOK_ID_3 = 3
BOOK_ID_4 = 4
BOOK_ID_5 = 5
BOOK_ID_6 = 6


@pytest.mark.asyncio
async def test_create_lending(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = LendingRepository(session)
        lending = Lending(user_id=USER_ID_1, book_id=BOOK_ID_1, quantity=1)
        result = await repo.create_lending(lending)
        assert result.id is not None
        assert result.user_id == USER_ID_1
        assert result.book_id == BOOK_ID_1


@pytest.mark.asyncio
async def test_get_active_lendings_by_user(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = LendingRepository(session)
        lending = Lending(user_id=USER_ID_2, book_id=BOOK_ID_2, quantity=1)
        await repo.create_lending(lending)
        result = await repo.get_active_lendings_by_user(USER_ID_2)
        assert len(result) == 1
        assert result[0].user_id == USER_ID_2


@pytest.mark.asyncio
async def test_get_lending_by_user_and_book(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = LendingRepository(session)
        lending = Lending(user_id=USER_ID_3, book_id=BOOK_ID_3, quantity=1)
        await repo.create_lending(lending)
        result = await repo.get_lending_by_user_and_book(USER_ID_3, BOOK_ID_3)
        assert result is not None
        assert result.user_id == USER_ID_3
        assert result.book_id == BOOK_ID_3


@pytest.mark.asyncio
async def test_get_lending_by_id(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = LendingRepository(session)
        lending = Lending(user_id=USER_ID_4, book_id=BOOK_ID_4, quantity=1)
        created = await repo.create_lending(lending)
        result = await repo.get_lending_by_id(created.id)
        assert result is not None
        assert result.id == created.id


@pytest.mark.asyncio
async def test_list_active_lendings(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = LendingRepository(session)
        lending = Lending(user_id=USER_ID_5, book_id=BOOK_ID_5, quantity=1)
        await repo.create_lending(lending)
        result = await repo.list_active_lendings()
        assert any(
            lending_item.user_id == USER_ID_5 for lending_item in result
        )


@pytest.mark.asyncio
async def test_user_lending_history(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = LendingRepository(session)
        lending = Lending(user_id=USER_ID_6, book_id=BOOK_ID_6, quantity=1)
        await repo.create_lending(lending)
        result = await repo.user_lending_history(USER_ID_6)
        assert len(result) >= 1
        assert result[0].user_id == USER_ID_6
