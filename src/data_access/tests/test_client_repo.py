from __future__ import annotations

import pytest

from asyncpg import Pool

from src.data_access.repositories.postgre import ClientRepo


@pytest.mark.asyncio
async def test_add_and_get_client(pg_pool: Pool) -> None:
    async for pool in pg_pool:
        repo = ClientRepo(pool=pool)
        all_clients = await repo.get_all()
        assert len(all_clients) == 0