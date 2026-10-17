import os
import logging
from typing import Optional

logger = logging.getLogger("zmie.db.postgres")


class PostgresClient:
    _pool = None
    _connection_attempted: bool = False

    @classmethod
    async def get_pool(cls):
        if cls._pool is None and not cls._connection_attempted:
            cls._connection_attempted = True
            dsn = os.getenv(
                "DATABASE_URL",
                "postgresql://zmie_admin:zmie_secure_password@localhost:5432/zmie_knowledge_db"
            )
            try:
                import asyncpg
                cls._pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5, timeout=2.0)
                logger.info("Connected to PostgreSQL enterprise cluster.")
            except Exception as e:
                logger.info("PostgreSQL cluster offline (%s); utilizing crash-resilient SQLite local store.", str(e))
                cls._pool = None
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool:
            try:
                await cls._pool.close()
            except Exception:
                pass
            cls._pool = None
        cls._connection_attempted = False
