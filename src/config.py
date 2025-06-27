from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройки БД
    PG_VERSION: str
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB_NAME: str
    PG_DATA: str

    # Настройки токена авторизации
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int

    # Настройки Redis
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    REDIS_PORT: int
    REDIS_HOST: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_USER}:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
