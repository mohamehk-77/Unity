#!/usr/bin/python3
"""SocialMedia"""
from sqlalchemy import create_engine, String, Column, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
import uuid
import os

from sqlalchemy.orm import declarative_base
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Users(Base):
    __tablename__ = "users"
    userID = Column("userID", CHAR(36), primary_key=True, default=generate_uuid)
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


class Posts(Base):
    __tablename__ = "posts"
    PostID = Column("PostID", CHAR(36), primary_key=True, default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))  # Corrected
    PostContent = Column("PostContent", VARCHAR(1024))

    def __init__(self, UserID, PostContent):
        self.UserID = UserID
        self.PostContent = PostContent


class Likes(Base):
    __tablename__ = "likes"
    LikeID = Column("LikeID", CHAR(36), primary_key=True,
                    default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostID = Column("PostID", CHAR(36), ForeignKey('posts.PostID'))

    def __init__(self, UserID, PostID):
        self.UserID = UserID
        self.PostID = PostID


class Comments(Base):
    __tablename__ = "comments"
    CommentID = Column("CommentID", CHAR(36), primary_key=True,
                       default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    PostID = Column("PostID", CHAR(36), ForeignKey('posts.PostID'))
    CommentContent = Column("CommentContent", VARCHAR(1024))

    def __init__(self, UserID, PostID, CommentContent):
        self.UserID = UserID
        self.PostID = PostID
        self.CommentContent = CommentContent


class Follows(Base):
    __tablename__ = "follows"
    FollowID = Column("FollowID", CHAR(36), primary_key=True, default=generate_uuid)
    FollowerID = Column("FollowerID", CHAR(36), ForeignKey('users.userID'))
    FolloweeID = Column("FolloweeID", CHAR(36), ForeignKey('users.userID'))

    def __init__(self, FollowerID, FolloweeID):
        self.FollowerID = FollowerID
        self.FolloweeID = FolloweeID


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


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(db)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)
session = session()

FirstName = "Ahmed"
LastName = "Reyad"
Gender = "Male"
ProfileName = "efdsaReyad24"
Email = "asdsadsadnigga56847@gmail.com"
add_user(FirstName, LastName, Gender, ProfileName, Email)

UserID = "cb51bf77-2f05-4bba-b572-70300e7e1b40"
PostContent = "ta3zem salam l3mo 7ossam gably badla :)"
# addPost(UserID, PostContent,  session)
# allPosts = session.query(Posts).filter(Posts.UserID == UserID).all()
# postFilterByUserID = [p.PostContent for p in allPosts]
# print(postFilterByUserID)

UserID = "789efd69-30c1-4706-b74d-36455d9b3bbe"
PostContent = "3ayz Tagme3a ya Shabab"
# addPost(UserID, PostContent,  session)
allPosts = session.query(Posts).filter(Posts.UserID == UserID).all()
# print(allPosts)
# postFilterByUserID = [p.PostContent for p in allPosts]
# print(postFilterByUserID)
# userPosts = []
# for p in allPosts:
#     userPosts.append(p.PostContent)
# print(userPosts)

# UserID = "a78d8519-929b-4f38-9f92-abc00d7b18a4"
# PostID = "5e54f127-3166-40ab-ba6a-96284dbf7971"
# # addLike(UserID, PostID)
# PostLikes = session.query(Likes).filter(Likes.PostID == PostID).all()
# # print(len(PostLikes))
# UserLikesPosts = session.query(Users, Likes).filter(Likes.PostID == PostID).filter(Likes.UserID == UserID).all()
# for user, like in UserLikesPosts:
#     print(user.FirstName, user.LastName, user.Email)  # Accessing user attributes

FollowerID = "01bef9a2-23a0-4d30-9e37-587eefe0012b"
FolloweeID = "789efd69-30c1-4706-b74d-36455d9b3bbe"
add_follow(FollowerID, FolloweeID)
