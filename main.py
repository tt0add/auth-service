from fastapi import FastAPI
import database.modules
from database.db import Base, engine
from routers.auth_router import router as auth_router

app = FastAPI(title='Auth Service API')
app.include_router(auth_router)


Base.metadata.create_all(engine)