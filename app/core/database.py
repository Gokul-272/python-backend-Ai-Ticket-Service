from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import StaticPool
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

_engine = None
_session_maker = None

def init_db_connection() -> None:
    global _engine, _session_maker
    database_url = settings.DATABASE_URL
    engine_args = {"echo": True}
    
    if "sqlite" in database_url:
        engine_args.update({"poolclass": StaticPool,"connect_args": {"check_same_thread": False}})
    _engine = create_async_engine(database_url, **engine_args)
    _session_maker = async_sessionmaker(bind=_engine,class_=AsyncSession,expire_on_commit=False,)

init_db_connection()

def use_in_memory_fallback() -> None:
    global _engine, _session_maker
    logger.warning("PostgreSQL connection failed. Falling back to in-memory SQLite database.")
    fallback_url = "sqlite+aiosqlite:///:memory:"
    _engine = create_async_engine(fallback_url,poolclass=StaticPool,connect_args={"check_same_thread": False},echo=True)
    _session_maker = async_sessionmaker(bind=_engine,class_=AsyncSession,expire_on_commit=False)

class EngineProxy:
    def __getattr__(self, name):
        return getattr(_engine, name)
    
    def begin(self, *args, **kwargs):
        return _engine.begin(*args, **kwargs)

class SessionMakerProxy:
    def __call__(self, *args, **kwargs):
        return _session_maker(*args, **kwargs)

    def begin(self, *args, **kwargs):
        return _session_maker.begin(*args, **kwargs)

engine = EngineProxy()
AsyncSessionLocal = SessionMakerProxy()