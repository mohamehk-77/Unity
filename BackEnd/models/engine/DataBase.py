#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users, Posts, Likes, Comments, Follows

# Database connection parameters
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the database engine
db = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(db)

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

# Database initialization


def init_db():
    from models import Base
    Base.metadata.create_all(engine)


# Define your CRUD functions


def add_user(FirstName, LastName, Gender, ProfileName, Email):
    Email_exist = session.query(Users).filter(Users.Email == Email).all()
    Profile_Name_Exist = session.query(Users).filter(Users.ProfileName == ProfileName).all()
    if len(Email_exist) > 0:
        print("Email Address already exists")
    elif len(Profile_Name_Exist) > 0:
        print("That ProfileName Was Taken Please Chose Another One!")
    else:
        user = Users(FirstName=FirstName, LastName=LastName, Gender=Gender, ProfileName=ProfileName, Email=Email)
        session.add(user)
        session.commit()


def add_post(UserID, PostContent):
    post = Posts(UserID=UserID, PostContent=PostContent)
    session.add(post)
    session.commit()
    print("Post Added")


def add_like(UserID, PostID):
    existing_like = session.query(Likes).filter_by(UserID=UserID, PostID=PostID).first()
    if existing_like:
        session.delete(existing_like)
        session.commit()
        print("Like removed")
    else:
        like = Likes(UserID=UserID, PostID=PostID)
        session.add(like)
        session.commit()
        print("Like added")


def add_comment(UserID, PostID, CommentContent):
    comment = Comments(UserID=UserID, PostID=PostID, CommentContent=CommentContent)
    session.add(comment)
    session.commit()


def add_follow(FollowerID, FolloweeID):
    existing_follow = session.query(Follows).filter_by(FollowerID=FollowerID, FolloweeID=FolloweeID).first()
    if existing_follow:
        session.delete(existing_follow)
        session.commit()
        print("Unfollowed")
    else:
        follow = Follows(FollowerID=FollowerID, FolloweeID=FolloweeID)
        session.add(follow)
        session.commit()
        print("Followed")
