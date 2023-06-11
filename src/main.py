from fastapi import FastAPI

from database import Base, engine
from router import api_router

app = FastAPI()
app.include_router(api_router)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/heath")
async def health_check():
    return {"status": "ok"}
