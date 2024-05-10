#!/usr/bin/python3
from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from api.v1.views import *
from Create import add_user, check_password_hash, Users, Posts, Comments, Follows, Likes, Notifications, session as db_session, Stories
import os
from Create import db, Session, Images, edit_user_email, edit_user_name, edit_user_info
from werkzeug.utils import secure_filename
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
import errno
import re


def save_image_file(image_file):
    # Define the correct path for saving images
    image_path = os.path.join('static', 'uploaded_images', secure_filename(image_file.filename))
    
    # Save the image file to the filesystem
    image_file.save(image_path)
    
    return image_path




db = Session()

app = Flask(__name__)

app.register_blueprint(User_app_views, url_prefix='/api/v1')
app.register_blueprint(Post_app_views, url_prefix='/api/v1')
app.register_blueprint(Comment_app_views, url_prefix='/api/v1')
app.register_blueprint(Like_app_views, url_prefix='/api/v1')
app.register_blueprint(Follow_app_views, url_prefix='/api/v1')
app.register_blueprint(Notifications_app_views, url_prefix='/api/v1')
app.register_blueprint(Image_app_views, url_prefix='/api/v1')
app.register_blueprint(Story_app_views, url_prefix='/api/v1')


UPLOAD_FOLDER = 'static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
flask_secret_key = os.getenv("FLASK_SECRET_KEY")
app.secret_key = flask_secret_key
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


# app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# These are the extension that we are accepting to be uploaded

# For a given file, return whether it's an allowed type or not


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    # Save the file to the filesystem
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Save only the relative path in the database
    relative_filepath = os.path.join('uploaded_images', filename)
    new_image = Images(user_id=session['user_id'], image_path=relative_filepath)
    db_session.add(new_image)
    db_session.commit()
    return 'File uploaded successfully'


def is_filename_safe(filename):
    # This regular expression checks for any character that is not a letter, number, underscore, or hyphen
    safe_pattern = re.compile('[^a-zA-Z0-9._-]')
    return not bool(safe_pattern.search(filename))


@app.route('/submit_story', methods=['POST'])
def submit_story():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    story_content = request.form.get('story_content')
    image_file = request.files.get('image_file')

    # Check if required data is present
    if not story_content or not image_file:
        return jsonify({'error': 'Story content or image file missing'}), 400

    # Check if the file is allowed
    if not allowed_file(image_file.filename):
        return jsonify({'error': 'File type not allowed. Please upload a file with one of the following extensions: png, jpg, jpeg, gif'}), 400
    
    if not is_filename_safe(image_file.filename):
        return jsonify({'error': 'Filename is not safe. Please rename the file and try again. Filenames should only contain letters, numbers, underscores, and hyphens.'}), 400
    # Check the file size
    max_file_size = 1024 * 1024 * 5  # 5 MB
    if image_file.content_length > max_file_size:
        return jsonify({'error': 'File size exceeds the limit of 5 MB. Please upload a smaller file.'}), 400

    try:
        # Save the image file and get the path
        image_path = save_image_file(image_file)
        
        # Calculate the image URL
        image_url = url_for('static', filename=os.path.join('uploaded_images', image_file.filename))
        
        # Create a new image record in the database
        new_image = Images(user_id=session['user_id'], image_path=image_path, image_url=image_url)
        db_session.add(new_image)
        db_session.commit()
        
        # Create a new story with the ImagePath of the new image
        new_story = Stories(UserID=session['user_id'], StoryContent=story_content, ImagePath=new_image.image_id)
        db_session.add(new_story)
        db_session.commit()
        
        return jsonify({'message': 'Story submitted successfully', 'story_id': new_story.StoryID}), 200
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file
    file = request.files.get('file')
    
    if not file:
        return "No file uploaded", 400

    # Check if the file is allowed
    if not allowed_file(file.filename):
        return "File type not allowed. Please upload a file with one of the following extensions: png, jpg, jpeg, gif", 400
    
    # Check the file size
    max_file_size = 1024 * 1024 * 5  # 5 MB
    if file.content_length > max_file_size:
        return "File size exceeds the limit of 5 MB. Please upload a smaller file.", 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    except IOError as e:
        return f"IOError: {str(e)}", 500
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500
    
    # Insert metadata into the database
    with Session() as db:
        image_metadata = Images(
            user_id=request.form.get('user_id'),  # Assuming you pass user ID in the form data
            image_path=file_path,
        )
        db.add(image_metadata)
        db.commit()

    return "File uploaded successfully", 200


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        profile_name = request.form['profile_name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']        
        user = add_user(first_name, last_name, gender, profile_name, email, password, birthday, session=db_session)
        if user is not None:
            flash('Signup successful!')
            session['profile_name'] = profile_name
            session['user_id'] = user.userID
            return redirect(url_for('home', profile_name=profile_name))
        else:
            flash('Signup failed. Please try again.')
    return render_template('signin_Page.html')


@app.route('/update_user_info', methods=['PUT'])
def update_user_info():
    # Retrieve user_id from session
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'error': 'User not authenticated'}), 401

    new_first_name = request.json.get('new_first_name')
    new_last_name = request.json.get('new_last_name')
    new_email = request.json.get('new_email')
    # You'll need to modify the edit_user_info function to handle the additional fields
    new_user = edit_user_info(user_id, new_first_name, new_last_name, new_email)
    if new_user is not None:
        return jsonify({'message': 'User information updated successfully'})
    else:
        return jsonify({'error': 'Failed to update user information'}), 500


@app.route('/change_password', methods=['POST'])
def change_password():
    # Retrieve user_id from session
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'error': 'User not authenticated'}), 401

    # Retrieve current and new passwords from the request
    current_password = request.json.get('currentPassword')
    new_password = request.json.get('newPassword')

    # Retrieve user from database
    user = db_session.query(Users).filter_by(userID=user_id).first()
    if user:
        # Check if the current password matches the user's password
        if not check_password_hash(user.PasswordHash, current_password):
            return jsonify({'error': 'Incorrect current password'}), 400

        # Update the user's password with the new password
        user.set_password(new_password)
        db_session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Retrieve user_id from the authenticated session
    user_id = session.get('user_id')

    # Retrieve confirmPassword from the request JSON payload
    confirm_password = request.form.get('confirmPassword', '')

    # Check if confirmPassword is empty
    if not confirm_password:
        flash('Please enter your current password')
        # Redirect to login if profile_name is not available yet
        return redirect(url_for('login'))

    # Retrieve the user from the database based on the user_id
    user = db_session.query(Users).filter_by(userID=user_id).first()
    if not user:
        flash('User not found')
        # Redirect to login if user is not found
        return redirect(url_for('login'))

    # Retrieve the profile_name from the user object
    profile_name = user.ProfileName

    # Check if the entered password matches the user's current password
    if not check_password_hash(user.PasswordHash, confirm_password):
        flash('Incorrect password')
        return jsonify({'error': 'Incorrect password'}), 400


    # If password matches, proceed with account deletion
    # Delete the user account and any associated data
    db_session.delete(user)
    db_session.commit()

    # Clear the user's session data
    session.clear()

    flash('Account successfully deleted')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db_session.query(Users).filter_by(Email=email).first()
        if user:
            if check_password_hash(user.PasswordHash, password):
                session['user_id'] = user.userID
                session['profile_name'] = user.ProfileName
                flash('You were successfully logged in')
                return redirect(url_for('home', profile_name=user.ProfileName))
            else:
                error = 'Incorrect password'
                return render_template('login_Page.html', error=error)
        else:
            error = 'Email not found'
            return render_template('login_Page.html', error=error)
    return render_template('login_Page.html')


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    image_file = request.files.get('file')
    if not image_file:
        return jsonify({'error': 'Image file missing'}), 400

    # ...same checks as before...

    try:
        image_path = save_image_file(image_file)
        new_image = Images(user_id=session['user_id'], image_path=image_path)
        db_session.add(new_image)
        db_session.commit()

        user = db_session.query(Users).filter_by(userID=session['user_id']).first()
        user.avatar_image_id = new_image.image_id
        db_session.commit()

        return jsonify({'message': 'Avatar image uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@app.route('/change_avatar', methods=['POST'])
def change_avatar():
    if 'user_id' not in session:
        return jsonify({'error': 'User not authenticated'}), 401

    image_file = request.files.get('file')

    # Check if required data is present
    if not image_file:
        return jsonify({'error': 'Image file missing'}), 400

    # Check if the file is allowed
    if not allowed_file(image_file.filename):
        return jsonify({'error': 'File type not allowed. Please upload a file with one of the following extensions: png, jpg, jpeg, gif'}), 400

    # Check the file size
    max_file_size = 1024 * 1024 * 5  # 5 MB
    if image_file.content_length > max_file_size:
        return jsonify({'error': 'File size exceeds the limit of 5 MB. Please upload a smaller file.'}), 400

    try:
        # Save the image file and get the path
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        
        # Create a new image record in the database
        new_image = Images(user_id=session['user_id'], image_path=image_path)
        db_session.add(new_image)
        db_session.commit()

        # Calculate the image URL without the UUID subdirectory
        image_url = url_for('static', filename='uploaded_images/' + filename)
        new_image.image_url = image_url
        db_session.commit()
        
        # Update the user's record with the new avatar image ID
        user = db_session.query(Users).filter_by(userID=session['user_id']).first()
        user.avatar_image_id = new_image.image_id
        db_session.commit()

        # Update the session with the new avatar image URL
        session['avatar_image_url'] = image_url
        
        return jsonify({'message': 'Avatar image changed successfully', 'image_url': image_url}), 200
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@app.route('/update_avatar_image_url', methods=['POST'])
def update_avatar_image_url():
    data = request.get_json()
    user_id = data.get('user_id')
    avatar_image_url = data.get('avatar_image_url')

    # Get the image record with the given URL
    avatar_image = db_session.query(Images).filter_by(image_url=avatar_image_url).first()
    if not avatar_image:
        return 'Image not found', 404

    # Update the user's avatar image ID in the database
    user = db_session.query(Users).filter_by(userID=user_id).first()
    if user:
        user.avatar_image_id = avatar_image.image_id
        db_session.commit()
        return 'Avatar image ID updated successfully', 200
    else:
        return 'User not found', 404


@app.route('/<profile_name>/home')
def home(profile_name):
    # Check if user is logged in
    current_page = 0
    if 'user_id' not in session:
        flash('Please log in to view this page')
        return redirect(url_for('login'))

    # Check if the logged-in user matches the requested profile
    if session.get('profile_name') != profile_name:
        flash('Unauthorized access')
        return redirect(url_for('login'))

    # Query the database for the user by profile name
    user = db_session.query(Users).filter_by(ProfileName=profile_name).first()
    if not user:
        flash('User not found')
        return redirect(url_for('login'))

    # Get the user's avatar image URL or use a default one
    avatar_image_url = url_for('static', filename='image/images.png')  # Default avatar image
    if user.avatar_image_id:
        avatar_image = db_session.query(Images).filter_by(image_id=user.avatar_image_id).first()
        if avatar_image:
            avatar_image_url = avatar_image.image_url
    # Get all stories and their images for the user
    stories_with_images = db_session.query(Stories, Images.image_url).outerjoin(Images, Stories.ImagePath == Images.image_id).filter(Stories.UserID == user.userID).all()
    
    # Construct a list of dictionaries with story content and image URLs
    stories_data = [{'content': story.StoryContent, 'image_url': image_url if image_url else avatar_image_url} for story, image_url in stories_with_images]
    total_stories_count = db_session.query(Stories).filter(Stories.UserID == user.userID).count()
    # Render the home page template with the user's information
    total_pages = (total_stories_count + 4) // 5
    return render_template('HomePage.html', user=user, avatar_image_url=avatar_image_url, stories_data=stories_data, current_page=current_page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)
