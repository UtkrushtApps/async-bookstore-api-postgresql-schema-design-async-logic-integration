import asyncpg
import asyncio

class Database:
    def __init__(self):
        self._pool = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(
            database="bookstore_db",
            user="bookstore_user",
            password="bookstore_pass",
            host="postgres",
            port=5432,
            min_size=1,
            max_size=6
        )

    async def disconnect(self):
        await self._pool.close()

    @property
    def pool(self):
        return self._pool

db = Database()
