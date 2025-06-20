from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_VERSION: str
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DB_NAME: str
    PG_DATA: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTE: int

    @property

    def DB_URL(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
