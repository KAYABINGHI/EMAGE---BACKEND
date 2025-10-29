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

# Get mood logs for a user
@mood_bp.route('/<int:user_id>', methods=['GET'])
def get_mood(user_id):
    moods = Mood.query.filter_by(user_id=user_id).order_by(Mood.created_at.desc()).all()
    
    if not moods:
        return jsonify({'message': 'No mood entries found', 'moods': []}), 200
    
    mood_list = [{
        'id': mood.id,
        'user_id': mood.user_id,
        'emotion_label': mood.emotion_label,
        'created_at': mood.created_at.isoformat() if mood.created_at else None
    } for mood in moods]
    
    return jsonify({'moods': mood_list, 'count': len(mood_list)}), 200