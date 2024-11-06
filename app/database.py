import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import settings
import redis.asyncio as aioredis
from app.models import Base

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

async def init_db():
    retries = 5
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break  # Успешное подключение
        except OperationalError:
            if i < retries - 1:
                await asyncio.sleep(2)  # Ожидание перед повторной попыткой
            else:
                raise