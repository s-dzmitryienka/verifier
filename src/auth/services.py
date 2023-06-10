from auth.models import User
from auth.schemas import UserCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db_session: AsyncSession, user: UserCreateSchema) -> User:
    fake_hashed_password = user.email + "notreallyhashed"
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=fake_hashed_password,
    )
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user
