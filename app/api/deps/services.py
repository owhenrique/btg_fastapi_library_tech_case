from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.repositories.book import BookRepository
from app.repositories.lending import LendingRepository
from app.repositories.user import UserRepository
from app.services.book import BookService
from app.services.lending import LendingService
from app.services.user import UserService


async def get_lending_service(
    session: AsyncSession = Depends(get_session),
) -> LendingService:
    lending_repo = LendingRepository(session)
    book_repo = BookRepository(session)
    svc = LendingService(lending_repo, book_repo, session)
    return svc


LendingServiceDep = Depends(get_lending_service)


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    repo = UserRepository(session)
    svc = UserService(repo, session=session)
    return svc


UserServiceDep = Depends(get_user_service)


async def get_book_service(
    session: AsyncSession = Depends(get_session),
) -> BookService:
    repo = BookRepository(session)
    svc = BookService(repo, session=session)
    return svc


BookServiceDep = Depends(get_book_service)
