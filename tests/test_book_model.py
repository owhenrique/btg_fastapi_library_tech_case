from app.models.book import Book, BookCategoryEnum

PRAGMATIC_TITLE = 'The Pragmatic Programmer'
PRAGMATIC_AUTHOR = 'Andrew Hunt'
CLEAN_CODE_TITLE = 'Clean Code'
DEFAULT_COPY = 1
TOTAL_COPIES = 3
LENDING_ONE = 1
LENDING_TWO = 2
RETURN_EXCEED = 5
INITIAL_TOTAL = 2
INITIAL_AVAILABLE = 1
ADD_QTY = 3


def test_create_book_instance():
    b = Book()
    b.name = PRAGMATIC_TITLE
    b.author = PRAGMATIC_AUTHOR
    b.category = BookCategoryEnum.TECH

    assert 'Pragmatic' in repr(b)
    assert 'Andrew' in repr(b)
    assert b.category == BookCategoryEnum.TECH
    # By default there is 1 copy and it is available
    assert b.total_copies == DEFAULT_COPY
    assert b.available_copies == DEFAULT_COPY


def test_lending_and_return_flow():
    b = Book()
    b.name = CLEAN_CODE_TITLE
    b.total_copies = TOTAL_COPIES
    b.available_copies = TOTAL_COPIES

    b.lending()  # lending 1
    assert b.available_copies == TOTAL_COPIES - LENDING_ONE

    b.lending(LENDING_TWO)  # lending remaining 2
    assert b.available_copies == TOTAL_COPIES - LENDING_ONE - LENDING_TWO

    # cannot lend when none available
    try:
        b.lending()
    except ValueError:
        pass
    else:
        raise AssertionError('lending should fail when no copies available')

    # returning copies
    b.return_copy(LENDING_TWO)
    assert b.available_copies == (
        TOTAL_COPIES - LENDING_ONE - LENDING_TWO + LENDING_TWO
    )

    # cannot return more than total
    try:
        b.return_copy(RETURN_EXCEED)
    except ValueError:
        pass
    else:
        raise AssertionError('return should fail when exceeding total copies')


def test_add_copies_increases_both():
    b = Book()
    b.total_copies = INITIAL_TOTAL
    b.available_copies = INITIAL_AVAILABLE
    b.add_copies(ADD_QTY)
    assert b.total_copies == INITIAL_TOTAL + ADD_QTY
    assert b.available_copies == INITIAL_AVAILABLE + ADD_QTY
