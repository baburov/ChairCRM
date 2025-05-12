from __future__ import annotations

from src.core.interfaces.order_former import IOrderFormer
from src.core.models.order import Order
from src.data_access.repositories_interface import IOrderRepo


class OrderFormerService(IOrderFormer):
    def __init__(self, order_repo: IOrderRepo):
        self.order_repo = order_repo

    async def form_order(self, order_data: Order) -> None:
        try:
            await self.order_repo.insert(order_data)
            return
        except Exception as e:
            raise Exception(f"Form order error: {e}")
