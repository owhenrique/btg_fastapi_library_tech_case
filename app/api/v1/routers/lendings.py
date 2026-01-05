from __future__ import annotations

from typing import List

from fastapi import APIRouter, status

from app.api.deps.auth import AdminOrStaffDep, AnyRoleDep
from app.api.deps.services import LendingServiceDep
from app.api.v1.schemas.lending import (
    LendingCreate,
    LendingRead,
    LendingReturn,
    LendingReturnResult,
)

router = APIRouter(prefix='/lendings', tags=['Lendings Routers'])


@router.post(
    '/',
    response_model=LendingRead,
    dependencies=[AdminOrStaffDep],
    status_code=status.HTTP_201_CREATED,
)
async def create_lending(data: LendingCreate, service=LendingServiceDep):
    return await service.create_lending(data)


@router.post(
    '/{lending_id}/return',
    response_model=LendingReturnResult,
    dependencies=[AdminOrStaffDep],
)
async def return_lending(
    lending_id: int,
    data: LendingReturn,
    service=LendingServiceDep,
):
    return await service.return_lending(lending_id, data)


@router.get(
    '/active',
    response_model=List[LendingRead],
    dependencies=[AdminOrStaffDep],
)
async def list_active_lendings(service=LendingServiceDep):
    return await service.list_active_lendings()


@router.get(
    '/user/{user_id}',
    response_model=List[LendingRead],
    dependencies=[AnyRoleDep],
)
async def user_lending_history(user_id: int, service=LendingServiceDep):
    return await service.user_lending_history(user_id)
