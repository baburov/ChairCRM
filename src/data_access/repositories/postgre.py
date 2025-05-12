from __future__ import annotations

from uuid import uuid4

import asyncpg

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
from src.data_access.utils.query_builder import client_queries
from src.data_access.utils.query_builder import interaction_queries
from src.data_access.utils.query_builder import item_queries
from src.data_access.utils.query_builder import order_queries
from src.data_access.utils.query_builder import user_queries


class UserRepo(IUserRepo):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_login_pswd(self, login: str, password: str) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(user_queries.get_by_login_pswd, login, password)
            return User(**dict(row)) if row else User()

    async def get_by_role(self, role_data: str) -> list[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(user_queries.get_by_role, role_data)
            return [User(**dict(row))] if row else [User()]

    async def get_by_fio(self, fio_data: str) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(user_queries.get_by_fio, fio_data)
            data = dict(row)
            del data["id"]
            user = User(**(data))
            user.id = uuid4()
            return user if row else User()

    async def get_all_users(self) -> list[User]:
        datas = []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(user_queries.get_all_users)
            for row in rows:
                data = dict(row)
                del data["id"]
                datas.append(data)
            users = [User(**data) for data in datas]
            for i in range(len(rows)):
                users[i].id = uuid4()
            return users

    async def add_user(self, user: User) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(user_queries.add_user, user.fio, user.contacts,
                               user.bonus, user.login, user.password, user.role)


class ClientRepo(IClientRepo):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_order(self, order_data: Order) -> Client:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(client_queries.get_by_order, order_data.id)
            return Client(**dict(row)) if row else Client()

    async def get_all(self) -> list[Client]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(client_queries.get_all)
            return [Client(**dict(row)) for row in rows]

    async def get_by_params(self, params: Client) -> list[Client]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(client_queries.get_by_params, params.fio)
            return [Client(**dict(row)) for row in rows]


class OrderRepo(IOrderRepo):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def insert(self, order_data: Order) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                order_queries.insert, 
                order_data.owner.id, 
                order_data.creation_date,
                order_data.status, 
                order_data.sum
            )

    async def get_by_owner(self, user_data: Client) -> list[Order]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(order_queries.get_by_owner, user_data.id)
            return [Order(**dict(row)) for row in rows]


class ItemRepo(IItemRepo):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_params(self, params: Item) -> list[Item]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(item_queries.get_by_params, params.name)
            return [Item(**dict(row)) for row in rows]


class InteractionHistoryRepo(IInteractionHistoryRepo):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_user(self, user_data: User) -> list[Interaction]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(interaction_queries.get_by_user, user_data.id)
            return [Interaction(**dict(row)) for row in rows]

    async def get_by_client(self, client_data: Client) -> list[Interaction]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(interaction_queries.get_by_client, client_data.id)
            return [Interaction(**dict(row)) for row in rows]