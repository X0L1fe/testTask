from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.auth.auth import create_access_token, create_refresh_token, get_password_hash, verify_password, store_refresh_token, verify_refresh_token
from app.models.user import User
from app.database import get_db
from datetime import timedelta

router = APIRouter()

# Регистрация
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_exists = await db.execute(select(User).where(User.username == user.username))
    if user_exists.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, password_hash=get_password_hash(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Вход и создание токенов
@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.username == user.username))
    db_user = db_user.scalars().first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.id})
    refresh_token = create_refresh_token(data={"sub": db_user.id})
    await store_refresh_token(str(db_user.id), refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}

# Обновление access-токена с помощью refresh-токена
@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = await decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload["sub"]
    if not await verify_refresh_token(user_id, refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    new_access_token = create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token}
