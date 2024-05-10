#!/usr/bin/python3
"""User Class"""
from sqlalchemy import create_engine, String, Column, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
import uuid


from sqlalchemy.orm import declarative_base
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Users(Base):
    __tablename__ = "users"
    userID = Column("userID", CHAR(36), primary_key=True,
                    default=generate_uuid)
    FirstName = Column("FirstName", VARCHAR(255))
    LastName = Column("LastName", VARCHAR(255))
    Gender = Column("Gender", Enum("Male", "Female"))
    ProfileName = Column("ProfileName", VARCHAR(255))
    Email = Column("Email", VARCHAR(255))

    def __init__(self, FirstName, LastName, Gender, ProfileName, Email):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Gender = Gender
        self.ProfileName = ProfileName
        self.Email = Email
