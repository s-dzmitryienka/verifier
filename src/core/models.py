from datetime import datetime
import uuid as uuid_pkg
from sqlalchemy import DateTime, Column, UUID

from database import Base


class ModelBase(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid_pkg.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow, default=datetime.utcnow)
