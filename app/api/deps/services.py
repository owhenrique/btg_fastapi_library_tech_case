from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    repo = UserRepository(session)
    svc = UserService(repo, session=session)
    return svc


UserServiceDep = Depends(get_user_service)
