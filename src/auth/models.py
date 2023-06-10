from sqlalchemy import Column, String, Boolean
from core.models import ModelBase


class User(ModelBase):
    __tablename__ = "users"

    email = Column(String(length=64), unique=True, index=True)
    name = Column(String(length=64))
    hashed_password = Column(String(length=256))
    is_active = Column(Boolean, default=True)
