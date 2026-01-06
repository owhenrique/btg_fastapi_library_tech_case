from __future__ import annotations

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.services import UserServiceDep
from app.api.v1.schemas.token import Token
from app.core.security import create_access_token
from app.services.user import UserService

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = UserServiceDep,
):
    user = await service.authenticate_user(
        form_data.username, form_data.password
    )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={'sub': str(user.id), 'role': user.role.value},
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
