from __future__ import annotations

import asyncio
import os

from typing import Generator

import asyncpg
import pytest


# Default test database connection string - can be overridden with environment variables
DEFAULT_TEST_DB_URL = "postgresql://postgres:1234@localhost:5432/test_db"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncpg.Pool]:
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def pg_pool() -> asyncpg.Pool:
    """
    Create and return a connection pool for PostgreSQL.

    This fixture provides a connection pool for integration tests with
    the PostgreSQL database.
    """
    # Get connection string from environment variable or use default
    connection_string = os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DB_URL)

    # Create connection pool
    pool = await asyncpg.create_pool(connection_string)

    try:
        # Set up test database - clear existing tables and create new ones
        async with pool.acquire() as conn:
            # Drop existing tables if they exist
            await conn.execute("DROP TABLE IF EXISTS Manager CASCADE")
            await conn.execute("DROP TABLE IF EXISTS Client CASCADE")
            await conn.execute("DROP TABLE IF EXISTS Order_ CASCADE")
            await conn.execute("DROP TABLE IF EXISTS Product CASCADE")
            await conn.execute("DROP TABLE IF EXISTS InteractionHistory CASCADE")
            await conn.execute("DROP TABLE IF EXISTS Interaction CASCADE")

            # Create tables needed for tests
            await conn.execute("""
                CREATE TABLE Manager (
                    id SERIAL PRIMARY KEY,
                    fio TEXT NOT NULL,
                    contacts TEXT,
                    bonus NUMERIC DEFAULT 0,
                    role TEXT DEFAULT 'user'
                )
            """)

            await conn.execute("""
                CREATE TABLE Client (
                    id SERIAL PRIMARY KEY,
                    fio TEXT NOT NULL,
                    phone_number TEXT NOT NULL
                )
            """)

            await conn.execute("""
                CREATE TABLE Order_ (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES Client(id),
                    creation_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    total NUMERIC DEFAULT 0
                )
            """)

            await conn.execute("""
                CREATE TABLE Product (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price NUMERIC NOT NULL,
                    stock INTEGER DEFAULT 0
                )
            """)

            await conn.execute("""
                CREATE TABLE InteractionHistory (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES Client(id),
                    date TEXT NOT NULL,
                    type TEXT NOT NULL,
                    details TEXT
                )
            """)

            await conn.execute("""
                CREATE TABLE Interaction (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES Client(id),
                    manager_id INTEGER REFERENCES Manager(id)
                )
            """)

        yield pool  # Use yield instead of return
    except Exception as e:
        await pool.close()
        raise e

    # Note: We'll let pytest-asyncio handle the cleanup

