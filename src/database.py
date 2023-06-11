from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
