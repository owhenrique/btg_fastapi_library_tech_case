from datetime import timedelta

from app.core.security import create_access_token, decode_access_token


def test_create_and_decode_token():
    payload = {'sub': '42', 'role': 'reader'}
    token = create_access_token(payload, expires_delta=timedelta(minutes=1))
    data = decode_access_token(token)
    assert data['sub'] == '42'
    assert data['role'] == 'reader'
