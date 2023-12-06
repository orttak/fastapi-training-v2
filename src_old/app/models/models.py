from __future__ import annotations
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.config import Base


class Post(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    published: bool = Column(Boolean, server_default='TRUE')
    created_at: DateTime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    owner_id: int = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner: "User" = relationship("User")


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    created_at: DateTime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)


class Vote(Base):
    __tablename__ = "votes"
    user_id: int = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id: int = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
