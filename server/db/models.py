from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func

from .database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    subscribed_at = Column(DateTime(timezone=True), default=func.now())


class NewsLetter(Base):
    __tablename__ = "newsletters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    published_at = Column(DateTime(timezone=True), default=func.now())
    published_by = Column(String)
    include_unsubscribe_link = Column(Boolean, default=True)
