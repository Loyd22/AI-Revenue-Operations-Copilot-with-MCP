# This file reads environment variables for backend settings.
# It keeps all important app configuration in one place.

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "AI Revenue Operations Copilot API"
    app_env: str = "development"
    app_debug: bool = True

    api_v1_prefix: str = "/api/v1"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    postgres_user: str = "revops_user"
    postgres_password: str = "revops_pass"
    postgres_db: str = "revops_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    database_url: str = "postgresql://revops_user:revops_pass@localhost:5433/revops_db"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change_this_to_a_long_random_secret"
    jwt_refresh_secret_key: str = "change_this_to_another_long_random_secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    openai_api_key: str = "your_openai_api_key_here"
    openai_model: str = "gpt-5"

    storage_backend: str = "local"
    local_storage_path: str = "storage"

    cors_origins: str = "http://localhost:3000"


settings = Settings()