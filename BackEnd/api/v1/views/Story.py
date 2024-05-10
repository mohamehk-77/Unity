from flask import Blueprint, request, jsonify
from Create import add_story, delete_story, session, Stories  # Import the Stories class

Story_app_views = Blueprint('Story_app_views', __name__)


@Story_app_views.route('/stories', methods=['POST'])
def create_story():
    data = request.get_json()
    UserID = data.get('UserID')
    StoryContent = data.get('StoryContent')
    ImagePath = data.get('ImagePath')
    # Validate required fields
    if not UserID or not StoryContent:
        return jsonify({"error": "UserID and StoryContent are required"}), 400
    # Add the story to the database
    story = add_story(UserID, StoryContent, ImagePath)
    return jsonify({"message": "Story created successfully", "story_id": story.StoryID}), 201


@Story_app_views.route('/stories/<story_id>', methods=['DELETE'])
def delete_story_api(story_id):
    # Check if the story exists
    story = session.query(Stories).filter_by(StoryID=story_id).first()
    if not story:
        return jsonify({"error": "Story not found"}), 404
    # Delete the story
    delete_story(story_id)
    return jsonify({"message": "Story deleted successfully"}), 200
