from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    name: str
    artist: str


class SongTable(SongBase, table=True):
    id: int = Field(default=None, primary_key=True)


class SongCreate(SongBase):
    pass
