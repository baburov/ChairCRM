from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class Client(BaseModel):
    id: UUID = uuid4()
    number: str = ""
    fio: str = ""

