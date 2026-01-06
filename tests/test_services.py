import asyncio

import pytest

from app.core.exceptions import (
    EmailAlreadyExists,
    IncorrectPassword,
    UserNotFound,
)
from app.repositories.user import UserRepository
from app.services.user import UserService


def test_create_user_and_authenticate_success(
    user_factory, async_session_factory
):
    async def inner():
        await user_factory('alice', 'alice@example.com', 'secret')
        async with async_session_factory() as session:
            repo = UserRepository(session)
            svc = UserService(repo, session=session)
            user = await svc.authenticate_user('alice@example.com', 'secret')
            assert user is not None
            assert user.name == 'alice'

    asyncio.run(inner())


def test_create_user_duplicate_email_raises(user_factory):
    async def inner():
        await user_factory('alice', 'alice@example.com', 'password')
        try:
            await user_factory('bob', 'alice@example.com', 'password')
            raise AssertionError('Expected EmailAlreadyExists')
        except EmailAlreadyExists:
            pass

    asyncio.run(inner())


def test_authenticate_user_errors(user_factory, async_session_factory):
    async def inner():
        await user_factory('alice', 'alice@example.com', 'secret')
        async with async_session_factory() as session:
            repo = UserRepository(session)
            svc = UserService(repo, session=session)

            with pytest.raises(UserNotFound):
                await svc.authenticate_user('missing@example.com', 'secret')

            with pytest.raises(IncorrectPassword):
                await svc.authenticate_user('alice@example.com', 'wrong')

    asyncio.run(inner())
