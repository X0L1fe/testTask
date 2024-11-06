from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db, init_db, redis
from app.routers import auth, tasks
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/check-db")
async def check_db(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        return {"status": "Database connected"}

@app.get("/check-redis")
async def check_redis():
    try:
        await redis.ping()
        return {"status": "Redis connected"}
    except Exception:
        return {"status": "Redis connection failed"}
