from sqlmodel import create_engine, SQLModel, Session
from config import DATABASE_URL

print(f"DB_URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
