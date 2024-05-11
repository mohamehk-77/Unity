#!/usr/bin/python3
from flask import request, Blueprint, jsonify
from Create import Users, Posts, Comments
from Create import add_comment, edit_comment, delete_comment, is_authorized_to_edit_comment, session

Comment_app_views = Blueprint("Comment_app_views", __name__)


@Comment_app_views.route('/users/<userID>/posts/<postID>/comments', methods=["POST"])
def CreateComment(userID, postID):
    Data = request.get_json()
    if 'CommentContent' not in Data:
        return jsonify({"error": "CommentContent is required"}), 400
    add_comment(userID, postID, Data['CommentContent'])
    return jsonify({"message": "Comment Was Created Successfully"}), 201


@Comment_app_views.route('/users/<userID>/posts/<postID>/comments', methods=["GET"])
def GetComments(userID, postID):
    comments = session.query(Comments).filter_by(UserID=userID, PostID=postID).all()
    comment_data = [{"CommentContent": comment.CommentContent} for comment in comments]
    Num = len(comments)
    return jsonify({"comments": comment_data, "Num": Num}), 200


@Comment_app_views.route('/users/<userID>/posts/<postID>/comments/<commentID>', methods=["PUT"])
def EditComment(userID, postID, commentID):
    Data = request.get_json()
    new_content = Data.get('new_content')
    if new_content is None:
        return jsonify({"error": "New content is required"}), 400
    if is_authorized_to_edit_comment(userID, postID, commentID):
        comment = session.query(Comments).filter_by(PostID=postID, CommentID=commentID).first()
        if comment:
            comment.CommentContent = new_content
            session.commit()
            return jsonify({"Message": "The comment has been edited successfully."}), 200
        else:
            return jsonify({"error": "Comment not found"}), 404
    else:
        return jsonify({"error": "You are not authorized to edit this comment"}), 403


@Comment_app_views.route('/users/<userID>/posts/<postID>/comments/<commentID>', methods=["DELETE"])
def DeleteComment(userID, postID, commentID):
    if is_authorized_to_edit_comment(userID, postID, commentID):
        delete_comment(userID, postID, commentID)
        return jsonify({"Message": "This comment was deleted successfully!"}), 200
    else:
        return jsonify({"error": "You are not authorized to delete this comment"}), 403
