from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.models.client import Client


class IClientsListFormer(ABC):
    @abstractmethod
    async def get_clients_list(self) -> list[Client]:
        pass