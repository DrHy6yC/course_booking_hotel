from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PG_VERSION: str
    PG_HOST: str
    PG_PORT: str
    PG_USER: str
    PG_PASSWORD: str
    PG_DB_NAME: str
    PG_DATA: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
