from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import redis.asyncio as aioredis

# Создание асинхронного двигателя SQLAlchemy
DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий для базы данных
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Настройка подключения к Redis
redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")

# Получение сессии базы данных
async def get_db():
    async with async_session() as session:
        yield session
