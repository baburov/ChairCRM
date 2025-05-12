from __future__ import annotations

from src.core.interfaces.clients_list_former import IClientsListFormer
from src.core.models.client import Client
from src.data_access.repositories_interface import IClientRepo


class ClientsListFormerService(IClientsListFormer):
    def __init__(self, clients_repo: IClientRepo):
        self.clients_repo = clients_repo

    async def get_clients_list(self) -> list[Client]:
        try:
            return await self.clients_repo.get_all()
        except Exception as e:
            raise Exception(f"Clients list error: {e}")