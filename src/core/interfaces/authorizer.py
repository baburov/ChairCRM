from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.models.user import User


class IAuthorizer(ABC):
    @abstractmethod
    async def auth(self, login: str, password: str) -> User:
        pass

    @abstractmethod
    async def register(self, user_data: User) -> User:
        pass
    