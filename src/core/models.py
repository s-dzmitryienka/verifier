import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime

from database import Base


class ModelBase(Base):
    """
    Base DB model
    """
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid_pkg.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow, default=datetime.utcnow)

    @classmethod
    def pk_name(cls):
        return cls.__mapper__.primary_key[0].name
