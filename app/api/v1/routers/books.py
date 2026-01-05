from __future__ import annotations

from typing import List

from fastapi import APIRouter, status

from app.api.deps.auth import AdminOrStaffDep
from app.api.deps.services import BookServiceDep
from app.api.v1.schemas.book import BookAvailability, BookCreate, BookRead

router = APIRouter(prefix='/books', tags=['Books Routers'])


@router.get('/', response_model=List[BookRead])
async def list_books(service=BookServiceDep):
    return await service.list_books()


@router.post(
    '/',
    response_model=BookRead,
    dependencies=[AdminOrStaffDep],
    status_code=status.HTTP_201_CREATED,
)
async def create_book(data: BookCreate, service=BookServiceDep):
    return await service.create_book(data)


@router.get(
    '/{book_id}/availability',
    response_model=BookAvailability,
)
async def check_availability(book_id: int, service=BookServiceDep):
    return await service.check_availability(book_id)
