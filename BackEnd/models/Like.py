#!/usr/bin/python3
"""Likes Class"""
from sqlalchemy import create_engine, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
import uuid

from sqlalchemy.orm import declarative_base
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Likes(Base):
    __tablename__ = "likes"
    LikeID = Column("LikeID", CHAR(36), primary_key=True,
                    default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostID = Column("PostID", CHAR(36), ForeignKey('posts.PostID'))

    def __init__(self, UserID, PostID):
        self.UserID = UserID
        self.PostID = PostID
