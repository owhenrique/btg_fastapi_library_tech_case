from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db import database


def test_settings_DATABASE_URL_is_sqlite():
    assert settings.DATABASE_URL.startswith('sqlite+aiosqlite://')


def test_engine_and_sessionmaker_present():
    assert database.engine is not None
    session = database.async_session()
    assert isinstance(session, AsyncSession)
