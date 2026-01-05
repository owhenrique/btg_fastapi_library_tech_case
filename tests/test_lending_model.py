from app.models.book import Book
from app.models.lending import Lending


def test_apply_lending_reduces_available():
    book = Book()
    book.total_copies = 3
    book.available_copies = 3

    lending = Lending()
    lending.book = book
    lending.quantity = 2

    lending.apply()
    assert book.available_copies == 1
    assert lending.is_active


def test_mark_returned_increases_available():
    book = Book()
    book.total_copies = 2
    book.available_copies = 0

    lending = Lending()
    lending.book = book
    lending.quantity = 1

    lending.mark_returned()
    assert book.available_copies == 1
    assert not lending.is_active
    assert lending.returned_at is not None


def test_cannot_apply_if_insufficient():
    book = Book()
    book.total_copies = 1
    book.available_copies = 0

    lending = Lending()
    lending.book = book
    lending.quantity = 1

    try:
        lending.apply()
    except ValueError:
        pass
    else:
        raise AssertionError('apply should fail when insufficient copies')


def test_cannot_return_exceeding_total():
    book = Book()
    book.total_copies = 1
    book.available_copies = 1

    lending = Lending()
    lending.book = book
    lending.quantity = 1

    try:
        lending.mark_returned()
    except ValueError:
        pass
    else:
        raise AssertionError(
            'mark_returned should fail when exceeding total copies'
        )
