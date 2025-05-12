from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel

from src.core.models.client import Client
from src.core.models.user import User


class Interaction(BaseModel):
    id: UUID = uuid4()
    data: str = ""
    type: str = ""
    client: Client
    user: User
    comments: str = ""