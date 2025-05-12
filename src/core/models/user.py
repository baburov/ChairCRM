from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class User(BaseModel):
    id: UUID = uuid4()
    fio: str = ""
    login: str = ""
    password: str = ""
    contacts: str = ""
    role: str = ""
    bonus: float = 0.0

