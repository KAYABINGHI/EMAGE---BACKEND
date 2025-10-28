from app.db import db
from flask import Blueprint
from flask import request, jsonify
from app.mood.models import Mood
from app.mood.utilis import get_mood_message

mood_bp =Blueprint('mood', __name__,url_prefix="/mood")

@mood_bp.route('/add-mood', methods=['POST'])
def add_mood():
    data = request.get_json()
    
    new_mood = Mood(
        user_id=data['user_id'],
        emotion_label=data['emotion_label']
    )
    
    db.session.add(new_mood)
    db.session.commit()
    
    message = get_mood_message(new_mood.emotion_label)
    
    return jsonify({
        'id': new_mood.id,
        'user_id': new_mood.user_id,
        'emotion_label': new_mood.emotion_label,
        'created_at': new_mood.created_at,
        'message': message
    }), 201

#mood listings/mood logs
@mood_bp.route('/mood/<int:id>', methods=['GET'])
def get_mood(id):
    pass