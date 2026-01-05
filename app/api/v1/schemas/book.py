from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.book import BookCategoryEnum


class BookCreate(BaseModel):
    name: str
    author: Optional[str] = None
    total_copies: int = 1
    category: BookCategoryEnum


class BookRead(BaseModel):
    id: int
    name: str
    author: Optional[str]
    total_copies: int
    available_copies: int
    category: BookCategoryEnum
    created_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True


class BookAvailability(BaseModel):
    book_id: int
    available_copies: int
    is_available: bool
