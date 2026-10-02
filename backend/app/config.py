from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./test.db",
        description="Default database connection URL (async driver preferred)",
    )
    SYNC_DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Explicit synchronous database URL. If omitted, derived from DATABASE_URL.",
    )
    
    # Connection pool configuration
    DB_POOL_SIZE: int = Field(default=5, description="Connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Max overflow connections")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Connection acquisition timeout in seconds")
    DB_POOL_RECYCLE: int = Field(default=1800, description="Recycle connections older than seconds")
    DB_ECHO: bool = Field(default=False, description="Echo SQL statements")
    
    # Application & Security configuration
    COOKIE_NAME: str = Field(default="sk_browser", description="Name of the session cookie")
    COOKIE_SECURE: bool = Field(default=False, description="Set Secure flag on cookies")
    SECRET_KEY: str = Field(
        default="insecure-dev-secret-key-change-in-production-min32bytes",
        description="Secret key for signing sessions and CSRF tokens",
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def sync_database_url(self) -> str:
        """Returns synchronous database URL suitable for standard SQLAlchemy engine."""
        if self.SYNC_DATABASE_URL:
            return self.SYNC_DATABASE_URL
        url = self.DATABASE_URL
        if url.startswith("sqlite+aiosqlite://"):
            return url.replace("sqlite+aiosqlite://", "sqlite://", 1)
        if url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
        return url

    @property
    def async_database_url(self) -> str:
        """Returns asynchronous database URL suitable for asyncpg / aiosqlite."""
        url = self.DATABASE_URL
        if url.startswith("sqlite://") and not url.startswith("sqlite+aiosqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if url.startswith("postgresql+psycopg2://"):
            return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
        return url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
