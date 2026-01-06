from __future__ import annotations

from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.db.database import engine as default_engine
from app.models.user import Role
from app.repositories.user import UserRepository
from app.services.user import UserService


async def create_dev_admin(
    engine_override: Optional[AsyncEngine] = None,
) -> None:
    """Ensure a default admin user exists (Used in development only)."""
    chosen = engine_override or default_engine
    session_factory = async_sessionmaker(
        bind=chosen, expire_on_commit=False, class_=AsyncSession
    )
    async with session_factory() as session:
        repo = UserRepository(session)
        svc = UserService(repo, session=session)
        existing = await repo.get_by_name('admin')
        if existing is None:
            await svc.create_user(
                'admin', 'admin@example.com', '1234', role=Role.ADMIN
            )


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_dev_admin())
