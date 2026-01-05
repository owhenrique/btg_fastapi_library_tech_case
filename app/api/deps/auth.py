from __future__ import annotations

from typing import Iterable, Set

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.deps.services import UserServiceDep
from app.core.security import decode_access_token
from app.models.user import Role, User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def get_current_user(
    token: str = Depends(oauth2_scheme), service: UserService = UserServiceDep
) -> User:
    try:
        payload = decode_access_token(token)
        sub = payload.get('sub')
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
            )
        user = await service.get_user(int(sub))
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
        )


def require_roles(allowed: Iterable[Role]):
    allowed_set: Set[Role] = set(allowed)

    async def verifier(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Insufficient role',
            )
        return current_user

    return verifier


AdminOnlyDep = Depends(require_roles([Role.ADMIN]))
AdminOrStaffDep = Depends(require_roles([Role.ADMIN, Role.LIBRARIAN]))
AnyRoleDep = Depends(require_roles([Role.ADMIN, Role.LIBRARIAN, Role.READER]))
