import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.database import create_db_and_tables
from app.db.fixtures import create_dev_admin
from app.models.user import Role
from app.repositories.user import UserRepository


def test_create_dev_admin_creates_admin():
    async def inner():
        engine = create_async_engine(
            'sqlite+aiosqlite:///:memory:', future=True
        )
        await create_db_and_tables(engine_override=engine)
        await create_dev_admin(engine_override=engine)
        async_session = async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            repo = UserRepository(session)
            admin = await repo.get_by_name('admin')
            assert admin is not None
            assert admin.role == Role.ADMIN
            assert admin.check_password('1234')
        await engine.dispose()

    asyncio.run(inner())
