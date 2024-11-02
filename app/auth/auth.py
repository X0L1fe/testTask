from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
import redis.asyncio as aioredis

# Настройки для Redis
redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")

# Настройки для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создание JWT токенов
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.refresh_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

# Проверка пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Хеширование пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Проверка токена и получение данных пользователя
async def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload.get("sub")
    except JWTError:
        return None

# Сохранение refresh-токена в Redis
async def store_refresh_token(user_id: str, token: str):
    await redis.set(f"refresh_token:{user_id}", token, ex=settings.refresh_token_expire_minutes * 60)

# Проверка refresh-токена в Redis
async def verify_refresh_token(user_id: str, token: str):
    stored_token = await redis.get(f"refresh_token:{user_id}")
    return stored_token and stored_token.decode("utf-8") == token
