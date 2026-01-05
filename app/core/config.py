from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration."""

    DATABASE_NAME: str = 'library'
    sqlalchemy_echo: bool = False
    SECRET_KEY: str = 'change-me'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_ENV: str = 'development'
    CREATE_DEV_ADMIN: bool = True

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @property
    def DATABASE_URL(self) -> str:
        return f'sqlite+aiosqlite:///./{self.DATABASE_NAME}.db'


settings = Config()
