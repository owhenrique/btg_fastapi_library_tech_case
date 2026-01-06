import asyncio
from datetime import datetime, timedelta

from fastapi import status

from app.core.security import create_access_token

FINE_PER_DAY = 2
FINE_DAYS_LATE = 6
FINE_TOTAL = FINE_PER_DAY * FINE_DAYS_LATE


def test_create_lending_endpoint(client, user_factory, book_factory):
    user = asyncio.run(user_factory(role='admin'))
    book = asyncio.run(book_factory(total_copies=2))
    token = create_access_token({'sub': str(user.id)})
    data = {'user_id': user.id, 'book_id': book.id}
    response = client.post(
        '/api/v1/lendings/',
        json=data,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    resp = response.json()
    assert resp['user_id'] == user.id
    assert resp['book_id'] == book.id


def test_lending_limit_endpoint(client, user_factory, book_factory):
    user = asyncio.run(user_factory(role='admin'))
    books = [asyncio.run(book_factory()) for _ in range(3)]
    token = create_access_token({'sub': str(user.id)})
    for book in books:
        client.post(
            '/api/v1/lendings/',
            json={'user_id': user.id, 'book_id': book.id},
            headers={'Authorization': f'Bearer {token}'},
        )
    response = client.post(
        '/api/v1/lendings/',
        json={'user_id': user.id, 'book_id': books[0].id},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Lending limit reached' in response.text


def test_return_lending_endpoint(client, user_factory, book_factory):
    user = asyncio.run(user_factory(role='admin'))
    book = asyncio.run(book_factory())
    token = create_access_token({'sub': str(user.id)})
    resp = client.post(
        '/api/v1/lendings/',
        json={'user_id': user.id, 'book_id': book.id},
        headers={'Authorization': f'Bearer {token}'},
    )
    lending_id = resp.json()['id']
    response = client.post(
        f'/api/v1/lendings/{lending_id}/return',
        json={'returned_at': datetime.now().isoformat()},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['fine'] == 0


def test_return_lending_with_fine_endpoint(client, user_factory, book_factory):
    user = asyncio.run(user_factory(role='admin'))
    book = asyncio.run(book_factory())
    token = create_access_token({'sub': str(user.id)})
    resp = client.post(
        '/api/v1/lendings/',
        json={'user_id': user.id, 'book_id': book.id},
        headers={'Authorization': f'Bearer {token}'},
    )
    lending = resp.json()
    late_date = datetime.fromisoformat(lending['lending_date']) + timedelta(
        days=20
    )
    response = client.post(
        f'/api/v1/lendings/{lending["id"]}/return',
        json={'returned_at': late_date.isoformat()},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['fine'] == FINE_TOTAL
