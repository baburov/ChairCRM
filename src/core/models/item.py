from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class Item(BaseModel):
    id: UUID = uuid4()
    article: int = 0
    style: str = ""
    color: str = ""
    description: str = ""
    weight: float = 0.0
    sizes: dict[str, float] = {}
    name: str = ""