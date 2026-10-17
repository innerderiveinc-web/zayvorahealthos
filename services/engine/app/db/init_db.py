"""
ZMIE Live Database Initialization & Migration Utility
Executes relational table creation in PostgreSQL and initial graph constraints in Neo4j.
"""

import os
import asyncio
import asyncpg
from neo4j import AsyncGraphDatabase


async def init_databases():
    print("=" * 80)
    print("  ZMIE LIVE DATABASE INITIALIZATION & MIGRATION RUNNER")
    print("=" * 80)

    # 1. PostgreSQL Schema Execution
    pg_dsn = os.getenv("DATABASE_URL", "postgresql://zmie_admin:zmie_secure_password@localhost:5432/zmie_knowledge_db")
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    print(f"\n[1/2] Connecting to PostgreSQL at {pg_dsn.split('@')[-1]}...")
    try:
        conn = await asyncpg.connect(pg_dsn)
        with open(schema_path, "r") as f:
            ddl_sql = f.read()
        await conn.execute(ddl_sql)
        await conn.close()
        print("  ✓ PostgreSQL tables & pgvector indexes successfully verified/created.")
    except Exception as e:
        print(f"  ⚠ PostgreSQL direct connection skipped (Ensure Docker container is running): {e}")

    # 2. Neo4j Constraints Execution
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_pwd = os.getenv("NEO4J_PASSWORD", "zmie_graph_password")

    print(f"\n[2/2] Connecting to Neo4j at {neo4j_uri}...")
    try:
        driver = AsyncGraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pwd))
        async with driver.session() as session:
            await session.run("CREATE CONSTRAINT unique_concept IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE")
            await session.run("CREATE CONSTRAINT unique_document IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE")
            await session.run("CREATE CONSTRAINT unique_claim IF NOT EXISTS FOR (cl:Claim) REQUIRE cl.id IS UNIQUE")
        await driver.close()
        print("  ✓ Neo4j graph uniqueness constraints successfully created.")
    except Exception as e:
        print(f"  ⚠ Neo4j direct connection skipped (Ensure Docker container is running): {e}")

    print("\n" + "=" * 80)
    print("  INITIALIZATION CYCLE FINISHED")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(init_databases())
