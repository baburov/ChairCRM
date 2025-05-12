from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.models.client import Client
from src.core.models.interaction import Interaction
from src.core.models.item import Item
from src.core.models.order import Order
from src.core.models.user import User


class IUserRepo(ABC):
    @abstractmethod
    async def get_by_login_pswd(self, login: str, password: str) -> User:
        pass

    @abstractmethod
    async def get_by_role(self, role_data: str) -> list[User]:
        pass

    @abstractmethod
    async def get_by_fio(self, fio_data: str) -> User:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def add_user(self, user: User) -> None:
        pass


class IOrderRepo(ABC):
    @abstractmethod
    async def insert(self, order_data: Order) -> None:
        pass

    @abstractmethod
    async def get_by_owner(self, user_data: Client) -> list[Order]:
        pass


class IItemRepo(ABC):
    @abstractmethod
    async def get_by_params(self, params: Item) -> list[Item]:
        pass


class IInteractionHistoryRepo(ABC):
    @abstractmethod
    async def get_by_user(self, user_data: User) -> list[Interaction]:
        pass

    @abstractmethod
    async def get_by_client(self, client_data: Client) -> list[Interaction]:
        pass


class IClientRepo(ABC):
    @abstractmethod
    async def get_by_order(self, order_data: Order) -> Client:
        pass

    @abstractmethod
    async def get_all(self) -> list[Client]:
        pass

    @abstractmethod
    async def get_by_params(self, params: Client) -> list[Client]:
        pass