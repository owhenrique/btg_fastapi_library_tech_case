import pytest_asyncio as pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app import main as app_main
from app.api.deps.services import get_user_service
from app.core.config import settings as app_settings
from app.db.database import create_db_and_tables
from app.models.book import Book, BookCategoryEnum
from app.models.lending import Lending
from app.models.user import Role
from app.repositories.book import BookRepository
from app.repositories.user import UserRepository
from app.services.book import BookService
from app.services.user import UserService


@pytest.fixture
async def engine():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_session_factory(engine):
    return async_sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )


@pytest.fixture
async def prepare_db(engine):
    await create_db_and_tables(engine_override=engine)


@pytest.fixture
async def user_factory(async_session_factory, prepare_db):
    async def _create(
        name='alice',
        email='alice@example.com',
        password='secret',
        role=Role.READER,
    ):
        async with async_session_factory() as session:
            repo = UserRepository(session)
            svc = UserService(repo, session=session)
            user = await svc.create_user(name, email, password, role=role)
            return user

    return _create


@pytest.fixture
async def book_factory(async_session_factory, prepare_db):
    async def _create(
        name='The Book',
        author='Author',
        category=BookCategoryEnum.FICTION,
        total_copies=1,
    ):
        async with async_session_factory() as session:
            book = Book(
                name=name,
                author=author,
                category=category,
                total_copies=total_copies,
            )
            session.add(book)
            await session.flush()
            await session.commit()
            return book

    return _create


@pytest.fixture
async def lending_factory(async_session_factory, user_factory, book_factory):
    async def _create(user=None, book=None, qty=1):
        if user is None:
            user = await user_factory()
        if book is None:
            book = await book_factory()
        async with async_session_factory() as session:
            lending = Lending(user_id=user.id, book_id=book.id, quantity=qty)
            session.add(lending)
            await session.flush()
            lending.book = book
            lending.apply()
            await session.commit()
            return lending

    return _create


@pytest.fixture
async def client(async_session_factory, prepare_db):
    orig_create = app_settings.CREATE_DEV_ADMIN
    app_settings.CREATE_DEV_ADMIN = False

    async def _override_get_user_service(*args, **kwargs):
        async with async_session_factory() as session:
            repo = UserRepository(session)
            svc = UserService(repo, session=session)
            return svc

    app_main.app.dependency_overrides[get_user_service] = (
        _override_get_user_service
    )

    client = TestClient(app_main.app)

    yield client

    app_main.app.dependency_overrides.pop(get_user_service, None)
    app_settings.CREATE_DEV_ADMIN = orig_create


@pytest.fixture
async def book_service(async_session_factory, prepare_db):
    async with async_session_factory() as session:
        repo = BookRepository(session)
        svc = BookService(repo, session=session)
        yield svc
