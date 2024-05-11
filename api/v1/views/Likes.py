#!/usr/bin/python3
from flask import Blueprint, request, jsonify
from Create import Users, Posts, Likes
from Create import add_or_remove_like, count_likes, session

Like_app_views = Blueprint("Like_app_views", __name__)


@Like_app_views.route('/users/<userID>/posts/<postID>/likes', methods=["POST"])
def AddRemoveLike(userID, postID):
    Data = request.get_json()
    Act = Data.get("action")
    if Act != 'toggle':
        return jsonify({"error": "InvalidAction"}), 400

    existing_like = session.query(Likes).filter_by(UserID=userID, PostID=postID).first()

    if existing_like:
        session.delete(existing_like)
        session.commit()
        return jsonify({"message": "Like removed"}), 200
    else:
        add_or_remove_like(userID, postID)
        return jsonify({"message": "Like added"}), 200


@Like_app_views.route('/posts/<postID>/likes/count', methods=["GET"])
def CountLikes(postID):
    likes_count = count_likes(postID)
    return jsonify({"likes_count": likes_count}), 200
