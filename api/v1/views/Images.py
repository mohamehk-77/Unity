from flask import Blueprint, request, flash, redirect, url_for
from Create import Images, db, session, session as db_session
from werkzeug.utils import secure_filename

import os

Image_app_views = Blueprint('Image_app_views', __name__)




@Image_app_views.route('/upload_image', methods=['POST'])
def upload_avatar():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            new_image = Images(session['user_id'], file_path)
            db_session.add(new_image)
            db_session.commit()
            return redirect(url_for('uploaded_file', filename=filename))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@Image_app_views.route('/delete_image/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = db.query(Images).get(image_id)
    if image and image.user_id == session['user_id']:
        db.delete(image)
        db.commit()
        return 'Image deleted successfully'
    else:
        return 'Image not found or unauthorized'


@Image_app_views.route('/count_images', methods=['GET'])
def count_images():
    image_count = db.query(Images).filter_by(user_id=session['user_id']).count()
    return f'You have uploaded {image_count} images'
