from __future__ import annotations

from fastapi import APIRouter, status

from app.api.deps.auth import AdminOrStaffDep
from app.api.deps.pagination import PaginationDep
from app.api.deps.services import BookServiceDep
from app.api.v1.schemas.book import BookAvailability, BookCreate, BookRead
from app.api.v1.schemas.paginated_response import PaginatedResponse

router = APIRouter(prefix='/books', tags=['Books Routers'])


@router.get('/', response_model=PaginatedResponse[BookRead])
async def list_books(
    pagination: PaginationDep,
    service=BookServiceDep,
):
    books, total = await service.list_books(
        limit=pagination.limit, offset=pagination.offset
    )
    return {
        'items': books,
        'total': total,
        'page': (pagination.offset // pagination.limit) + 1,
        'size': len(books),
    }


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
