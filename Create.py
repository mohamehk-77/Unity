#!/usr/bin/python3
import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Enum, ForeignKey, Date, TIMESTAMP, LargeBinary
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
from sqlalchemy import String
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# Create the base class using the declarative_base factory function
Base = declarative_base()

flask_secret_key = os.getenv("FLASK_SECRET_KEY")


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
    PasswordHash = Column("PasswordHash", VARCHAR(256))
    Birthday = Column("Birthday", Date)
    avatar_image_id = Column("avatar_image_id", CHAR(36), ForeignKey('images.image_id'), nullable=True)

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

    def __init__(self, FirstName, LastName, Gender, ProfileName, Email, Password, Birthday, avatar_image_id):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Gender = Gender
        self.ProfileName = ProfileName
        self.Email = Email
        self.set_password(Password)
        self.Birthday = Birthday
        self.avatar_image_id = avatar_image_id


class Posts(Base):
    __tablename__ = "posts"
    PostID = Column("PostID", CHAR(36), primary_key=True, default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))  # Corrected
    PostContent = Column("PostContent", VARCHAR(1024))
    image = Column("image", VARCHAR(255), nullable=True)

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


class Notifications(Base):
    __tablename__ = "notifications"
    id = Column("id", CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column("user_id", CHAR(36), ForeignKey('users.userID'))
    message = Column("message", VARCHAR(255))
    created_at = Column("created_at", TIMESTAMP, default=datetime.utcnow)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message


def create_notification(user_id, message):
    notification = Notifications(user_id=user_id, message=message)
    session.add(notification)
    session.commit()


class Images(Base):
    __tablename__ = "images"
    image_id = Column("image_id", CHAR(36), primary_key=True, default=generate_uuid)
    user_id = Column("user_id", CHAR(36), ForeignKey('users.userID'))
    image_path = Column("image_path", VARCHAR(255))  # New column to store image file path
    upload_time = Column("upload_time", TIMESTAMP, default=datetime.utcnow)
    image_url = Column("image_url", String(255))  # Adjusted to specify length

    def __init__(self, user_id, image_path, image_url=None):
        self.user_id = user_id
        self.image_path = image_path
        self.image_url = image_url


class Stories(Base):
    __tablename__ = "stories"
    StoryID = Column("StoryID", CHAR(36), primary_key=True, default=generate_uuid)
    UserID = Column("UserID", CHAR(36), ForeignKey('users.userID'))
    StoryContent = Column("StoryContent", VARCHAR(1024))
    ImagePath = Column("ImagePath", VARCHAR(255), nullable=True)

    def __init__(self, UserID, StoryContent, ImagePath=None):
        self.UserID = UserID
        self.StoryContent = StoryContent
        self.ImagePath = ImagePath


def add_story(UserID, StoryContent, ImagePath=None):
    story = Stories(UserID=UserID, StoryContent=StoryContent, ImagePath=ImagePath)
    session.add(story)
    session.commit()
    print("Story Added")


def delete_story(story_id):
    story_to_delete = session.query(Stories).filter(Stories.StoryID == story_id).one()
    session.delete(story_to_delete)
    session.commit()
    print("Story Deleted")


def add_user(FirstName, LastName, Gender, ProfileName, Email, Password, Birthday, session, avatar_image_id=None):
    Email_exist = session.query(Users).filter(Users.Email == Email).all()
    Profile_Name_Exist = session.query(Users).filter(Users.ProfileName == ProfileName).all()
    if len(Email_exist) > 0:
        print("Email Address already exists")
    elif len(Profile_Name_Exist) > 0:
        print("That ProfileName Was Taken Please Choose Another One!")
    else:
        new_user = Users(FirstName=FirstName, LastName=LastName, Gender=Gender, ProfileName=ProfileName, Email=Email, Password=Password, Birthday=Birthday, avatar_image_id=avatar_image_id)
        session.add(new_user)
        session.commit()
        return new_user




def edit_user_email(userID, new_email):
    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        User.set_email(new_email)
        session.commit()


def add_post(UserID, PostContent):
    post = Posts(UserID=UserID, PostContent=PostContent)
    session.add(post)
    session.commit()
    print("Post Added")


def add_or_remove_like(UserID, PostID):
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


def edit_user_info(user_id, new_first_name, new_last_name, new_email):
    user = session.query(Users).filter_by(userID=user_id).first()
    if user:
        if new_first_name:
            user.FirstName = new_first_name
        if new_last_name:
            user.LastName = new_last_name
        if new_email:
            user.Email = new_email
        session.commit()
        return user
    else:
        return None


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
        return jsonify({"message": "Unfollowed"}), 200
    else:
        follow = Follows(FollowerID=FollowerID, FolloweeID=FolloweeID)
        session.add(follow)
        session.commit()
        print("Followed")
        return jsonify({"message": "Followed"}), 200


def is_authorized_to_edit_post(userID, postID):
    post = session.query(Posts).filter_by(UserID=userID, PostID=postID).first()
    if post and post.UserID == userID:
        return True
    return False


def edit_post(PostID, new_content):
    post = session.query(Posts).filter_by(PostID=PostID).first()
    if post:
        post.PostContent = new_content
        session.commit()
        print("Post updated")
    else:
        print("Post not found")


def delete_post(PostID):
    post = session.query(Posts).filter_by(PostID=PostID).first()
    if post:
        session.delete(post)
        session.commit()
        print("Post deleted")
    else:
        print("Post not found")


def is_authorized_to_edit_comment(userID, postID, commentID):
    comment = session.query(Comments).filter_by(PostID=postID, CommentID=commentID).first()
    if comment:
        if comment.UserID == userID:
            return True
    return False


def edit_comment(userID, postID, commentID, new_content):
    comment = session.query(Comments).filter_by(UserID=userID, PostID=postID, CommentID=commentID).first()
    if comment:
        comment.CommentContent = new_content
        session.commit()
        print("Comment updated")
    else:
        print("Comment not found")


def delete_comment(userID, postID, CommentID):
    comment = session.query(Comments).filter_by(UserID=userID, PostID=postID, CommentID=CommentID).first()
    if comment:
        session.delete(comment)
        session.commit()
        print("Comment deleted")
    else:
        print("Comment not found")


def count_likes(PostID):
    likes_count = session.query(Likes).filter_by(PostID=PostID).count()
    return likes_count


def edit_user_name(userID, new_first_name, new_last_name):
    user = session.query(Users).filter_by(userID=userID).first()
    if user:
        user.FirstName = new_first_name
        user.LastName = new_last_name
        session.commit()
        print("User name updated")
    else:
        print("User not found")


def login(email, password):
    user = session.query(Users).filter_by(Email=email).first()
    if user and user.check_password(password):
        print("Login successful")
        return user
    else:
        print("Invalid email or password")
        return None


def count_followers(userID):
    followers_count = session.query(Follows).filter_by(FolloweeID=userID).count()
    return followers_count


def count_follows(userID):
    follows_count = session.query(Follows).filter_by(FollowerID=userID).count()
    return follows_count


def delete_story(story_id):
    """
    Delete a story from the database by its ID.
    """
    story = session.query(Stories).filter_by(StoryID=story_id).first()
    if story:
        session.delete(story)
        session.commit()
        return True
    return False


def fetch_stories_for_user(user_id):
    """
    Fetch stories for a user from the database.
    """
    stories = session.query(Stories).filter_by(UserID=user_id).all()
    return stories


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Create the database engine
db = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(db)

# Create all tables known to Base
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()
