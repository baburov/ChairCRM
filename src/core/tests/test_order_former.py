from __future__ import annotations

import pytest

from src.core.models.client import Client
from src.core.models.item import Item
from src.core.models.order import Order
from src.core.services.order_form_service import OrderFormerService
from src.data_access.repositories.mock import MockOrderRepo


@pytest.mark.asyncio
async def test_order_former() -> None:
    order_repo = MockOrderRepo()
    order_former_service = OrderFormerService(order_repo)
    content = [
        Item(
            article=1,
            name="chair",
            style="modern",
            color="green",
            description="123",
            weight=12.0,
            sizes={"lenth": 1.0, "depth": 1.0, "width": 1.0},
        ),
        Item(
            article=1,
            name="table",
            style="modern",
            color="green",
            description="321",
            weight=22.0,
            sizes={"lenth": 2.0, "depth": 2.0, "width": 2.0},
        ),
        Item(
            article=1,
            name="table2",
            style="modern",
            color="green",
            description="321",
            weight=22.0,
            sizes={"lenth": 3.0, "depth": 3.0, "width": 3.0},
        ),
    ]
    await order_former_service.form_order(
        order_data=Order(
            content=content,
            creation_date="",
            status="",
            owner=Client(),
            sum=0.0,
        )
    )
