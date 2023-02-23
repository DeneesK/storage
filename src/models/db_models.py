import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String(length=255), unique=True)
    password = Column(Text, unique=False)
    file = relationship('File')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "User(id='%s', login='%s)" % (self.id, self.login)


class File(Base):
    __tablename__ = 'file'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, unique=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_downloadable = Column(Boolean, default=True)
    path = Column(Text, unique=False)
    size = Column(Integer, unique=False)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='file')
