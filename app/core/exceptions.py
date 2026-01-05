from __future__ import annotations

from fastapi import status


class BaseServiceException(Exception):
    """Base class for service-layer errors.

    Subclasses should set class attributes `code` and `detail`. Instances will
    pick those defaults when constructed without arguments.
    """

    code: int = status.HTTP_400_BAD_REQUEST
    detail: str | None = None

    def __init__(self, code: int | None = None, detail: str | None = None):
        self.code = (
            code
            if code is not None
            else getattr(self.__class__, 'code', status.HTTP_400_BAD_REQUEST)
        )
        self.detail = (
            detail
            if detail is not None
            else getattr(self.__class__, 'detail', None)
        )
        super().__init__(self.detail)


class EmailAlreadyExists(BaseServiceException):
    code = status.HTTP_409_CONFLICT
    detail = 'Email already registered'


class IncorrectPassword(BaseServiceException):
    code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect email or password'


class UserNotFound(BaseServiceException):
    code = status.HTTP_404_NOT_FOUND
    detail = 'User not found'


class InvalidEmail(BaseServiceException):
    code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = 'Invalid email address'


class BookNotFound(BaseServiceException):
    code = status.HTTP_404_NOT_FOUND
    detail = 'Book not found'


class BookAlreadyExists(BaseServiceException):
    code = status.HTTP_409_CONFLICT
    detail = 'Book already exists'


class InvalidBookData(BaseServiceException):
    code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = 'Invalid book data'


class LendingLimitReached(BaseServiceException):
    code = status.HTTP_409_CONFLICT
    detail = 'User has reached the maximum number of active lendings'


class LendingAlreadyExists(BaseServiceException):
    code = status.HTTP_409_CONFLICT
    detail = 'User already has an active lending for this book'


class LendingNotFound(BaseServiceException):
    code = status.HTTP_404_NOT_FOUND
    detail = 'Lending not found'


class BookNotAvailable(BaseServiceException):
    code = status.HTTP_409_CONFLICT
    detail = 'Book is not available for lending'
