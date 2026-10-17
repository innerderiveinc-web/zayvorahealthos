"""
ZMIE Live Neo4j Graph Connection & Cypher Runner
"""

import os
from neo4j import AsyncGraphDatabase, AsyncDriver
from typing import Optional, List, Dict, Any


class Neo4jClient:
    _driver: Optional[AsyncDriver] = None

    @classmethod
    def get_driver(cls) -> AsyncDriver:
        if cls._driver is None:
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USER", "neo4j")
            password = os.getenv("NEO4J_PASSWORD", "zmie_graph_password")
            cls._driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        return cls._driver

    @classmethod
    async def run_query(cls, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        driver = cls.get_driver()
        async with driver.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    @classmethod
    async def close(cls):
        if cls._driver:
            await cls._driver.close()
            cls._driver = None
