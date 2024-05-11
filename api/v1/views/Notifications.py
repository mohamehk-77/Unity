from flask import Blueprint, jsonify, request
from sqlalchemy import func
from Create import session, Notifications, Users, Posts, Comments

Notifications_app_views = Blueprint("notifications_app_views", __name__)


def create_notification(user_id, interaction_type, post_id=None, comment_id=None):
    user = session.query(Users).filter_by(id=user_id).first()
    if interaction_type == 'like':
        post = session.query(Posts).filter_by(PostID=post_id).first()
        message = f'<b>{user.username}</b> liked your post: {post.PostContent}'
    elif interaction_type == 'comment':
        comment = session.query(Comments).filter_by(CommentID=comment_id).first()
        message = f'<b>{user.username}</b> commented on your post: {comment.CommentContent}'
    elif interaction_type == 'follow':
        message = f'<b>{user.username}</b> started following you'
    else:
        return "Invalid interaction type"

    notification = Notifications(user_id=user_id, message=message)
    session.add(notification)
    session.commit()


@Notifications_app_views.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = session.query(Notifications).filter_by(user_id=user_id).all()
    notifications_data = [{"id": notification.id, "message": notification.message, "created_at": notification.created_at} for notification in notifications]
    return jsonify({"notifications": notifications_data}), 200


@Notifications_app_views.route('/notifications/count/<user_id>', methods=['GET'])
def count_notifications(user_id):
    notifications_count = session.query(func.count(Notifications.id)).filter_by(user_id=user_id).scalar()
    return jsonify({"notifications_count": notifications_count}), 200


@Notifications_app_views.route('/notifications/reset/<user_id>', methods=['POST'])
def reset_notifications(user_id):
    session.query(Notifications).filter_by(user_id=user_id).delete()
    session.commit()
    return jsonify({"message": "Notifications reset successfully"}), 200
