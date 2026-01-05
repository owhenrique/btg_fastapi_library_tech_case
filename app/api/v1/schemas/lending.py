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
