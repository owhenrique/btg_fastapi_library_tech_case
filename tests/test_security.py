from app.core.security import hash_password, verify_password


def test_hash_and_verify():
    hashed = hash_password('secret123')
    assert hashed != 'secret123'
    assert verify_password(hashed, 'secret123')
    assert not verify_password(hashed, 'wrong')


def test_uniqueness_due_to_salt():
    h1 = hash_password('same')
    h2 = hash_password('same')
    assert h1 != h2
    assert verify_password(h1, 'same')
    assert verify_password(h2, 'same')


def test_invalid_hash_returns_false():
    assert not verify_password('not-a-valid-hash', 'anything')
