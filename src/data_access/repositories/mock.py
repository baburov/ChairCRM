from __future__ import annotations

from uuid import uuid4

from src.core.models.client import Client
from src.core.models.interaction import Interaction
from src.core.models.item import Item
from src.core.models.order import Order
from src.core.models.user import User
from src.data_access.repositories_interface import IClientRepo
from src.data_access.repositories_interface import IInteractionHistoryRepo
from src.data_access.repositories_interface import IItemRepo
from src.data_access.repositories_interface import IOrderRepo
from src.data_access.repositories_interface import IUserRepo


class MockUserRepo(IUserRepo):
    @staticmethod
    async def get_by_login_pswd(login: str, password: str) -> User:
        return User(fio="user", login=login, password=password, role="user", bonus=0.0)

    @staticmethod
    async def get_by_fio(fio_data: str) -> User:
        return User(fio=fio_data, login="login123", password="password123", role="user", bonus=0.0)

    @staticmethod
    async def get_all_users() -> list[User]:
        return [
            User(fio="a", login="login123", password="password123", role="user", bonus=0.0),
            User(fio="b", login="login123", password="password123", role="user", bonus=0.0),
            User(fio="c", login="login123", password="password123", role="user", bonus=0.0),
            User(fio="d", login="login123", password="password123", role="user", bonus=0.0),
        ]

    @staticmethod
    async def get_by_role(role_data: str) -> list[User]:
        return [User(fio="user", login="login123", password="password123", role=role_data, bonus=0.0)]

    @staticmethod
    async def add_user(user: User) -> None:
        pass


class MockOrderRepo(IOrderRepo):
    @staticmethod
    async def insert(order_data: Order) -> None:
        if not order_data.content:
            raise ValueError("Content cannot be empty")

    @staticmethod
    async def get_by_owner(client_data: Client) -> list[Order]:
        return [
            Order(
                content=[
                    Item(
                        color="green",
                        name="Awesome Chair",
                        style="modern",
                        description="d",
                        weight=0.0,
                        article=1,
                        sizes={"l": 1},
                    )
                ],
                creation_date="01.01.1997",
                status="in process",
                owner=client_data,
                sum=0.0,
            )
        ]


class MockItemRepo(IItemRepo):
    @staticmethod
    async def get_by_params(params: Item) -> list[Item]:
        return [params]


class MockInteractionHistoryRepo(IInteractionHistoryRepo):
    @staticmethod
    async def get_by_user(user_data: User) -> list[Interaction]:
        return [
            Interaction(
                data="01.01.2001",
                type="sell",
                client=Client(id=uuid4(), fio="123", number="123"),
                user=user_data,
                comments="good",
            )
        ]

    @staticmethod
    async def get_by_client(client_data: Client) -> list[Interaction]:
        return [
            Interaction(
                data="01.01.2001",
                type="sell",
                client=client_data,
                user=User(fio="123", login="123", password="123", role="user", bonus=0.0),
                comments="good",
            )
        ]


class MockClientRepo(IClientRepo):
    @staticmethod
    async def get_by_order(order_data: Order) -> Client:
        return Client(id=uuid4(), fio="123", number="123")

    @staticmethod
    async def get_all() -> list[Client]:
        return [
            Client(id=uuid4(), fio="123", number="123"),
            Client(id=uuid4(), fio="123", number="123"),
            Client(id=uuid4(), fio="123", number="123"),
        ]

    @staticmethod
    async def get_by_params(params: Client) -> list[Client]:
        return [params]

