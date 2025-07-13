from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    REDIS_HOST: str
    OPENAI_API_KEY: str
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str


_settings = _Settings()


class Settings:
    OPENAI_API_KEY: str = _settings.OPENAI_API_KEY
    NEO4J_URI: str = _settings.NEO4J_URI
    NEO4J_USER: str = _settings.NEO4J_USER
    NEO4J_PASSWORD: str = _settings.NEO4J_PASSWORD

    DATABASE_URL: str = (
        f"postgresql+psycopg://{_settings.DB_USER}:{_settings.DB_PASSWORD}@"
        f"{_settings.DB_HOST}:{_settings.DB_PORT}/{_settings.DB_NAME}"
    )
    CELERY_BROKER_URL: str = f"redis://{_settings.REDIS_HOST}:6379/0"


settings = Settings()
