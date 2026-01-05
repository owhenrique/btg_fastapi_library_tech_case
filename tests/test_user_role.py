from app.models.user import Role, User


def test_default_role_is_user():
    u = User()
    u.name = 'joao'
    assert u.role in {None, Role.READER}


def test_set_role_admin():
    u = User()
    u.role = Role.ADMIN
    assert u.role == Role.ADMIN


def test_role_repr_includes_value():
    u = User()
    u.name = 'Ana'
    u.role = Role.LIBRARIAN
    assert 'librarian' in repr(u)
