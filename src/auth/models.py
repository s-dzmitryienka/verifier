from datetime import datetime

from sqlalchemy import Boolean, Column, String, DateTime

from core.models import ModelBase


class User(ModelBase):
    __tablename__ = "users"

    email = Column(String(length=64), unique=True, index=True)
    name = Column(String(length=64))
    hashed_password = Column(String(length=256))
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True), default=datetime.utcnow)
