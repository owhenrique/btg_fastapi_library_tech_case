from __future__ import annotations

from typing import List

from fastapi import APIRouter, status

from app.api.deps.auth import AdminOnlyDep, AdminOrStaffDep, AnyRoleDep
from app.api.deps.pagination import PaginationDep
from app.api.deps.services import UserServiceDep
from app.api.v1.schemas.lending import LendingRead
from app.api.v1.schemas.paginated_response import PaginatedResponse
from app.api.v1.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.user import UserService

router = APIRouter(prefix='/users', tags=['Users Routers'])


@router.get(
    '/',
    response_model=PaginatedResponse[UserRead],
    dependencies=[AdminOnlyDep],
)
async def list_users(
    pagination: PaginationDep,
    service: UserService = UserServiceDep,
):
    users, total = await service.list_users(
        limit=pagination.limit, offset=pagination.offset
    )
    return {
        'items': users,
        'total': total,
        'page': (pagination.offset // pagination.limit) + 1,
        'size': len(users),
    }


@router.post(
    '/',
    response_model=UserRead,
    dependencies=[AdminOrStaffDep],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(data: UserCreate, service: UserService = UserServiceDep):
    role = data.role or User().role
    user = await service.create_user(
        name=data.name, email=data.email, password=data.password, role=role
    )
    return user


@router.get(
    '/{user_id}',
    response_model=UserRead,
    dependencies=[AdminOrStaffDep],
)
async def get_user_by_id(user_id: int, service: UserService = UserServiceDep):
    user = await service.get_user(user_id)
    return user


@router.get(
    '/{user_id}/lendings',
    response_model=List[LendingRead],
    dependencies=[AnyRoleDep],
)
async def list_user_lendings(
    user_id: int, service: UserService = UserServiceDep
):
    return await service.list_lendings(user_id)
