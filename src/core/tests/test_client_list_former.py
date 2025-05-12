from __future__ import annotations

import pytest

from src.core.services.clients_list_former_service import ClientsListFormerService
from src.data_access.repositories.mock import MockClientRepo


@pytest.mark.asyncio
async def test_client_list_former() -> None:
    clients_repo = MockClientRepo()
    service = ClientsListFormerService(clients_repo=clients_repo)
    assert len(await service.get_clients_list()) != 0


@pytest.mark.asyncio
async def test_client_list_former_1() -> None:
    clients_repo = MockClientRepo()
    service = ClientsListFormerService(clients_repo=clients_repo)
    assert len(await service.get_clients_list()) != 0
