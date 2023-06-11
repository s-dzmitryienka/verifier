from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import UserCreateSchema, UserSchema
from database import Base, engine, get_session
from auth.services import create_user as srv_create_user
app = FastAPI()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/heath")
async def health_check():
    return {"status": "ok"}


@app.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    return await srv_create_user(db_session=session, user=user)
