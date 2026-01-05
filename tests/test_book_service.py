import pytest

from app.api.v1.schemas.book import BookCreate
from app.models.book import BookCategoryEnum
from app.services.book_service import BookService
from app.services.exceptions import (
    BookAlreadyExists,
    BookNotFound,
    InvalidBookData,
)

TOTAL_COPIES = 2


@pytest.mark.asyncio
async def test_create_book_success(book_service: BookService):
    data = BookCreate(
        name='Livro Teste',
        author='Autor',
        total_copies=TOTAL_COPIES,
        category=BookCategoryEnum.FICTION
    )
    book = await book_service.create_book(data)
    assert book.id is not None
    assert book.name == 'Livro Teste'
    assert book.author == 'Autor'
    assert book.total_copies == TOTAL_COPIES
    assert book.available_copies == TOTAL_COPIES
    assert book.category == BookCategoryEnum.FICTION


@pytest.mark.asyncio
async def test_create_book_duplicate(book_service: BookService):
    data = BookCreate(
        name='Duplicado',
        author='Autor',
        total_copies=1,
        category=BookCategoryEnum.TECH
    )
    await book_service.create_book(data)
    with pytest.raises(BookAlreadyExists):
        await book_service.create_book(data)


@pytest.mark.asyncio
async def test_create_book_invalid_data(book_service: BookService):
    data = BookCreate(
        name='',
        author='Autor',
        total_copies=0,
        category=BookCategoryEnum.OTHER
    )
    with pytest.raises(InvalidBookData):
        await book_service.create_book(data)


@pytest.mark.asyncio
async def test_check_availability_success(book_service: BookService):
    data = BookCreate(
        name='Disponível',
        author='Autor',
        total_copies=TOTAL_COPIES,
        category=BookCategoryEnum.FICTION
    )
    book = await book_service.create_book(data)
    availability = await book_service.check_availability(book.id)
    assert availability.book_id == book.id
    assert availability.available_copies == TOTAL_COPIES
    assert availability.is_available is True


@pytest.mark.asyncio
async def test_check_availability_not_found(book_service: BookService):
    with pytest.raises(BookNotFound):
        await book_service.check_availability(9999)
