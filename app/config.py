from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_host: str

    class Config:
        env_file = ".env"

settings = Settings()