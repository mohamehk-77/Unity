from flask import Blueprint, request, jsonify
from Create import Users
from Create import add_user, edit_user_name, session, edit_user_email
from werkzeug.security import generate_password_hash

User_app_views = Blueprint('User_app_views', __name__)


@User_app_views.route('/users', methods=['POST'])
def CreateUser():
    Data = request.get_json()    
    add_user(Data['FirstName'], Data['LastName'],
             Data['Gender'], Data['ProfileName'],
             Data['Email'], Data['Password'])
    return jsonify({"message": "User Created Successfully"}), 201


@User_app_views.route("/users/<userID>", methods=["PUT"])
def UpdateUserName(userID):
    Data = request.get_json()
    edit_user_name(userID, Data.get('new_first_name'),
                   Data.get('new_last_name'))
    return jsonify({"message": "User Updated Successfully"}), 200


@User_app_views.route("/users/<userID>", methods=["GET"])
def GetUser(userID):
    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        return jsonify({"FirstName": User.FirstName,
                        "LastName": User.LastName,
                        "Gender": User.Gender,
                        "Email": User.Email}), 200
    else:
        return jsonify({"message": "User Not Found"}), 404


@User_app_views.route("/users/<userID>", methods=["DELETE"])
def DeleteUser(userID):
    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        session.delete(User)
        session.commit()
        return jsonify({"message": "User Deleted Successfully!"}), 200
    else:
        return jsonify({"message": "User Not Found!"}), 404


@User_app_views.route("/users/<userID>/password", methods=["PUT"])
def UpdateUserPassword(userID):
    Data = request.get_json()
    current_password = Data.get('current_password')
    new_password = Data.get('new_password')

    if current_password is None or new_password is None:
        return jsonify({"message": "Current and new passwords are required"}), 400

    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        if not User.check_password(current_password):
            return jsonify({"message": "Current password is incorrect"}), 401

        User.set_password(new_password)
        session.commit()
        return jsonify({"message": "Password Updated Successfully"}), 200
    else:
        return jsonify({"message": "User Not Found"}), 404


@User_app_views.route("/users/<userID>/info", methods=["PUT"])
def UpdateUserInfo(userID):
    Data = request.get_json()
    new_first_name = Data.get('new_first_name')
    new_last_name = Data.get('new_last_name')
    new_email = Data.get('new_email')

    if new_first_name is None or new_last_name is None or new_email is None:
        return jsonify({"message": "New first name, last name, and email are required"}), 400

    # Check if the new email already exists in the database
    existing_user = session.query(Users).filter_by(Email=new_email).first()
    if existing_user and existing_user.userID != userID:
        return jsonify({"message": "This email is already in use"}), 400

    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        User.FirstName = new_first_name
        User.LastName = new_last_name
        User.Email = new_email
        session.commit()
        return jsonify({"message": "User Info Updated Successfully"}), 200
    else:
        return jsonify({"message": "User Not Found"}), 404
