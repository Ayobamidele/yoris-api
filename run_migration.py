"""
run_migration.py  —  Creates all SQLAlchemy tables on the configured DATABASE_URL.
Works with both SQLite (aiosqlite) and PostgreSQL (asyncpg).
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env")

# Normalise dialect so asyncpg is always used for Postgres
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

print(f"Connecting to: {DATABASE_URL[:40]}...")

from sqlalchemy.ext.asyncio import create_async_engine

# Import Base first so the declarative registry is built
from app.utils.database import Base

# Now import all models so they register themselves with Base
import app.models  # noqa: F401 — side effect: registers all ORM classes

async def run():
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        print("\nRunning create_all ...")
        await conn.run_sync(Base.metadata.create_all)
        print("\n✅ Done — all tables created (or already existed).")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run())
