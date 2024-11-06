import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL configuration
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_user: str = os.getenv("DB_USER", "user")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_name: str = os.getenv("DB_NAME", "task_db")

    # Redis configuration
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "secret_key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

    class Config:
        env_file = ".env"

settings = Settings()
