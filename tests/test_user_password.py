from app.models.user import User


def test_set_and_check_password():
    user = User()
    user.set_password('secret123')

    # Should not store plain text
    assert user.password != 'secret123'

    # Correct password passes
    assert user.check_password('secret123')

    # Wrong password fails
    assert not user.check_password('wrongpassword')


def test_hash_format_and_uniqueness():
    u1 = User()
    u2 = User()

    u1.set_password('samepass')
    u2.set_password('samepass')

    # With salt, two hashes for same plain password should differ
    assert u1.password != u2.password

    # Format should start with algorithm name
    assert u1.password.startswith('pbkdf2_sha256$')

    assert u1.check_password('samepass')
    assert u2.check_password('samepass')


def test_invalid_stored_hash():
    u = User()
    u.password = 'not-a-valid-hash'
    assert not u.check_password('anything')
