#!/usr/bin/python3
from flask import request, jsonify, Blueprint
from Create import Users, Follows
from Create import add_follow, count_followers, count_follows, session

Follow_app_views = Blueprint("Follow_app_views", __name__)


@Follow_app_views.route('/users/<followerID>/follow/<followeeID>', methods=["POST"])
def AddRemoveFollow(followerID, followeeID):
    if followerID == followeeID:
        return jsonify({"error": "You cannot follow yourself"}), 400
    Data = request.get_json()
    Act = Data.get("action")
    if Act != 'toggle':
        return jsonify({"error": "InvalidAction"}), 400

    existing_follow = session.query(Follows).filter_by(FollowerID=followerID, FolloweeID=followeeID).first()

    if existing_follow:
        session.delete(existing_follow)
        session.commit()
        return jsonify({"message": "Unfollowed"}), 200
    else:
        follow = Follows(FollowerID=followerID, FolloweeID=followeeID)
        session.add(follow)
        session.commit()
        return jsonify({"message": "Followed"}), 200


@Follow_app_views.route('/users/<userID>/followers/count', methods=["GET"])
def CountFollowers(userID):
    followers_count = count_followers(userID)
    return jsonify({"followers_count": followers_count}), 200


@Follow_app_views.route('/users/<userID>/follows/count', methods=["GET"])
def CountFollows(userID):
    follows_count = count_follows(userID)
    return jsonify({"follows_count": follows_count}), 200
