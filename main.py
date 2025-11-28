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
    redis = Redis(host="localhost", port=6379, db=0)
    await FastAPILimiter.init(redis)

Base.metadata.create_all(engine)