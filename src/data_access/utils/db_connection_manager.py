from __future__ import annotations

import asyncio

import asyncpg


class DatabaseConnectionManager:
    def __init__(self, connection_string: str, update_interval: int = 15):

        self.connection_string = connection_string
        self.pool: asyncpg.Pool | None = None
        self.update_interval = update_interval * 60 
        self.is_running = False
        self._initialized = False
    
    async def initialize(self, connection_string: str) -> None:
        self.connection_string = connection_string  # or self.connection_string or os.environ.get("DATABASE_URL")
        
        if not self.connection_string:
            raise ValueError("Connection string must be provided")
        
        await self._create_pool()
        self.is_running = True
        self._initialized = True
        asyncio.create_task(self._update_connection_loop())  
    
    async def _create_pool(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(
                self.connection_string, 
                min_size=5, 
                max_size=10
            )
            print("Database connection pool created.")
        except Exception as e:
            print(f"Error creating database connection pool: {e}")
            self.pool = None
            raise
    
    async def _close_pool(self) -> None:
        if self.pool:
            await self.pool.close()
            self.pool = None
            print("Database connection pool closed.")
    
    async def _update_connection_loop(self) -> None:
        while self.is_running:
            await asyncio.sleep(self.update_interval)
            await self._update_connection()
    
    async def _update_connection(self) -> None:
        print("Updating database connection...")
        try:
            new_pool = await asyncpg.create_pool(
                self.connection_string, 
                min_size=5, 
                max_size=10
            )
            old_pool = self.pool
            self.pool = new_pool
            if old_pool:
                asyncio.create_task(old_pool.close())  # Close old pool in the background
            print("Database connection updated successfully.")
        except Exception as e:
            print(f"Error updating database connection: {e}")
    
    def get_pool(self) -> asyncpg.Pool:
        if not self.pool:
            raise Exception("Database connection pool is not available.")
        return self.pool
    
    async def get_connection(self) -> asyncpg.Connection:
        if not self.pool:
            raise Exception("Database connection pool is not available.")
        return await self.pool.acquire()  # Important: Caller must release the connection!
    
    async def close(self) -> None:
        self.is_running = False
        await self._close_pool()
        self._initialized = False
        print("Database connection manager closed.")
    
    @property
    def initialized(self) -> bool:
        return self._initialized


db_manager = DatabaseConnectionManager("")