from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.models.client import Client
from src.core.models.item import Item


class IRecomendationFormer(ABC):
    @abstractmethod
    async def create_recomendation(self, client_data: Client) -> list[Item]:
        pass