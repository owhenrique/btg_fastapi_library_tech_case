import asyncio

from app.models.book import BookCategoryEnum

TOTAL_COPIES = 3


def test_book_factory_and_lending(book_factory, user_factory, lending_factory):
    async def inner():
        book = await book_factory(
            'My Book',
            author='Auth',
            category=BookCategoryEnum.TECH,
            total_copies=TOTAL_COPIES,
        )
        assert book.id is not None
        user = await user_factory('bob', 'bob@example.com', 'pw')
        lending = await lending_factory(user=user, book=book, qty=1)
        assert lending.id is not None
        assert lending.book.available_copies == TOTAL_COPIES - 1

    asyncio.run(inner())
