from fastapi import FastAPI
import database.models
from database.db import Base, engine
from routers.auth_router import router as auth_router
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis

app = FastAPI(title='Auth Service API')
app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    redis_conn = Redis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)

Base.metadata.create_all(engine)