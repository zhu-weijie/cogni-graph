from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    OPENAI_API_KEY: str

    NEO4J_URI: str = "neo4j://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    CELERY_BROKER_URL: str = "redis://redis:6379/0"


settings = Settings()
