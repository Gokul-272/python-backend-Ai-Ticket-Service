import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

import app.core.database

app.core.database.engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)
app.core.database.AsyncSessionLocal = async_sessionmaker(
    bind=app.core.database.engine,
    class_=AsyncSession,
    expire_on_commit=False
)

from app.main import app

@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as c:
        yield c

@pytest.fixture(name="db_session")
async def db_session_fixture():
    async with app.core.database.AsyncSessionLocal() as session:
        yield session
