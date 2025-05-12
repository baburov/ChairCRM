from __future__ import annotations

import pytest

from asyncpg import Pool

from src.core.models.user import User
from src.data_access.repositories.postgre import UserRepo


@pytest.mark.asyncio
async def test_add_and_get_user(pg_pool: Pool) -> None:
    async for pool in pg_pool:
        repo = UserRepo(pool=pool)

        user = User(fio="Alice", bonus=1000)
        await repo.add_user(user)

        all_users = await repo.get_all_users()
        assert all_users[0].fio == "Alice"


@pytest.mark.asyncio
async def test_get_by_fio(pg_pool: Pool) -> None:
    async for pool in pg_pool:
        repo = UserRepo(pool=pool)

        user = User(fio="Bob Smirnov", bonus=500)
        await repo.add_user(user)

        result = await repo.get_by_fio("Bob Smirnov")
        assert result is not None
        assert result.fio == "Bob Smirnov"