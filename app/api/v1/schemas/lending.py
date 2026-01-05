from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LendingRead(BaseModel):
    id: int
    book_id: int
    quantity: int
    lending_date: datetime
    returned_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True


class LendingCreate(BaseModel):
    user_id: int
    book_id: int


class LendingReturn(BaseModel):
    returned_at: datetime | None = None


class LendingReturnResult(BaseModel):
    lending_id: int
    returned_at: datetime
    fine: float
