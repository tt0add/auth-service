from fastapi import FastAPI
import database.modules
from database.db import Base, engine


app = FastAPI(title='Auth Service API')

Base.metadata.create_all(engine)