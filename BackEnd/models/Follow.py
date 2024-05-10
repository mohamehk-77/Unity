#!/usr/bin/python3
"""Follow Class"""
from sqlalchemy import create_engine, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
import uuid

from sqlalchemy.orm import declarative_base
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Follows(Base):
    __tablename__ = "follows"
    FollowID = Column("FollowID", CHAR(36), primary_key=True, default=generate_uuid)
    FollowerID = Column("FollowerID", CHAR(36), ForeignKey('users.userID'))
    FolloweeID = Column("FolloweeID", CHAR(36), ForeignKey('users.userID'))

    def __init__(self, FollowerID, FolloweeID):
        self.FollowerID = FollowerID
        self.FolloweeID = FolloweeID
