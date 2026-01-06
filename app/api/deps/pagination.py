from typing import Annotated

from fastapi import Depends, Query


class PaginationParams:
    def __init__(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset


def _pagination_params(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PaginationParams:
    return PaginationParams(limit, offset)


PaginationDep = Annotated[PaginationParams, Depends(_pagination_params)]
