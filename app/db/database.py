from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.models.base import Base

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=settings.sqlalchemy_echo, future=True
)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_db_and_tables(
    engine_override: AsyncEngine | None = None,
) -> None:
    chosen_engine = engine_override or engine
    async with chosen_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
