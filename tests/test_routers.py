from fastapi import status
from fastapi.testclient import TestClient

import app.api.v1.routers.users as users_router
from app import main
from app.core.security import create_access_token
from app.services.exceptions import IncorrectPassword, UserNotFound


def test_get_user_by_id_not_found(monkeypatch):
    async def raise_not_found(*args, **kwargs):
        raise UserNotFound()

    monkeypatch.setattr(
        users_router.UserService,
        'get_user',
        raise_not_found,
    )

    client = TestClient(main.app)

    token = create_access_token({'sub': '1', 'role': 'admin'})
    headers = {'Authorization': f'Bearer {token}'}

    resp = client.get('/users/1', headers=headers)
    assert resp.status_code == UserNotFound().code
    assert resp.json().get('detail') == UserNotFound().detail


def test_auth_token_failure(monkeypatch):
    async def raise_incorrect(*args, **kwargs):
        raise IncorrectPassword()

    monkeypatch.setattr(
        'app.api.v1.routers.auth.UserService.authenticate_user',
        raise_incorrect,
    )

    client = TestClient(main.app)

    resp = client.post('/auth/token', data={'username': 'x', 'password': 'y'})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert resp.json().get('detail') == 'Incorrect email or password'
