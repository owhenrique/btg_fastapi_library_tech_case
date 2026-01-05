from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import Role


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[Role] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    created_at: Optional[datetime]

    class ConfigDict:
        from_attributes = True
