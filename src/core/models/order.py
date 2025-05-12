from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel

from src.core.models.client import Client
from src.core.models.item import Item


class Order(BaseModel):
    id: UUID = uuid4()
    content: list[Item] = []
    creation_date: str = ""
    status: str = ""
    owner: Client = Client()
    sum: float = 0.0