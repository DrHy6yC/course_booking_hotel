from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройка среды
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = Field(default="LOCAL")

    # Настройки БД
    PG_VERSION: str = Field(default="")
    PG_HOST: str = Field(default="")
    PG_PORT: int = Field(default=0)
    PG_USER: str = Field(default="")
    PG_PASSWORD: str = Field(default="")
    PG_DB_NAME: str = Field(default="")
    PG_DATA: str = Field(default="")

    # Настройки токена авторизации
    JWT_SECRET_KEY: str = Field(default="")
    JWT_ALGORITHM: str = Field(default="")
    ACCESS_TOKEN_EXPIRE_MINUTE: int = Field(default=0)

    # Настройки Redis
    REDIS_PASSWORD: str = Field(default="")
    REDIS_USER: str = Field(default="")
    REDIS_USER_PASSWORD: str = Field(default="")
    REDIS_PORT: int = Field(default=0)
    REDIS_HOST: str = Field(default="")

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg:"
            f"//{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"
        )

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
