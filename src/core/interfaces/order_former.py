from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.models.order import Order


class IOrderFormer(ABC):
    @abstractmethod
    async def form_order(self, order_data: Order) -> None:
        pass

    