from fastapi import FastAPI

from db import init_db
from models import SongTable

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}