from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.config import get_settings


class Base(DeclarativeBase):
    pass


# SQLite Foreign Keys pragma listener
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Only execute pragma on sqlite engines
    if hasattr(dbapi_connection, "cursor"):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        except Exception:
            pass
        finally:
            cursor.close()


settings = get_settings()

# Engine creation helpers
def create_sync_db_engine(url: str, echo: bool = False) -> Engine:
    connect_args = {}
    kwargs = {"echo": echo}
    if "sqlite" in url:
        connect_args["check_same_thread"] = False
        kwargs["connect_args"] = connect_args
        if ":memory:" in url:
            kwargs["poolclass"] = StaticPool
    else:
        kwargs["pool_size"] = settings.DB_POOL_SIZE
        kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
        kwargs["pool_timeout"] = settings.DB_POOL_TIMEOUT
        kwargs["pool_recycle"] = settings.DB_POOL_RECYCLE
    return create_engine(url, **kwargs)


def create_async_db_engine(url: str, echo: bool = False) -> AsyncEngine:
    connect_args = {}
    kwargs = {"echo": echo}
    if "sqlite" in url:
        connect_args["check_same_thread"] = False
        kwargs["connect_args"] = connect_args
        if ":memory:" in url:
            kwargs["poolclass"] = StaticPool
    else:
        kwargs["pool_size"] = settings.DB_POOL_SIZE
        kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
        kwargs["pool_timeout"] = settings.DB_POOL_TIMEOUT
        kwargs["pool_recycle"] = settings.DB_POOL_RECYCLE
    return create_async_engine(url, **kwargs)


# Default engines and sessionmakers
sync_engine: Engine = create_sync_db_engine(settings.sync_database_url, echo=settings.DB_ECHO)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async_engine: AsyncEngine = create_async_db_engine(settings.async_database_url, echo=settings.DB_ECHO)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


def get_db() -> Generator[Session, None, None]:
    """Dependency / generator providing synchronous database session."""
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency / generator providing asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Context manager for synchronous database sessions."""
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@asynccontextmanager
async def async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for asynchronous database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
