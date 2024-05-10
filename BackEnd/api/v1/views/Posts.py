#!/usr/bin/python3
from flask import Blueprint, request, jsonify
from Create import Users, Posts
from Create import add_post, edit_post, delete_post, is_authorized_to_edit_post, session

Post_app_views = Blueprint('Post_app_views', __name__)


@Post_app_views.route('/users/<userID>/posts', methods=['POST'])
def CreatePost(userID):
    Data = request.get_json()
    if 'PostContent' not in Data:
        return jsonify({"error": "PostContent is required"}), 400
    post_content = Data['PostContent']
    
    add_post(userID, post_content)
    return jsonify({"message": "Post Created Successfully!"}), 201


@Post_app_views.route('/users/<userID>/posts/<postID>', methods=['PUT'])
def Update_Post(userID, postID):
    Data = request.get_json()
    if is_authorized_to_edit_post(userID, postID):
        edit_post(postID, Data['PostContent'])
        return jsonify({"message": "Post Updated Successfully!"}), 200
    else:
        return jsonify({"error": "You are not authorized to edit this post"}), 403


@Post_app_views.route('/users/<userID>/posts/<postID>', methods=['DELETE'])
def Delete_Post(userID, postID):
    if is_authorized_to_edit_post(userID, postID):
        delete_post(postID)
        return jsonify({"message": "Post Was Deleted Successfully!"}), 200
    else:
        return jsonify({"error": "You are not authorized to delete this post"}), 403
