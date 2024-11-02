from fastapi import FastAPI, Depends
from app.database import get_db, redis
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

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
    
@app.get("/ping")
async def ping():
    return {"message": "pong"}
