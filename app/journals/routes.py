from flask import request, jsonify
from app.db import db
from app.journals.models import Journal
from flask import Blueprint

journals_bp = Blueprint('journals', __name__, url_prefix="/journals")


# Get all journal entries
@journals_bp.route('/', methods=['GET'])
def get_entries():
    entries = Journal.query.order_by(Journal.created_at.desc()).all()
    return jsonify([entry.to_dict() for entry in entries]), 200


# Get single journal entry by ID
@journals_bp.route('/<int:id>', methods=['GET'])
def get_entry(id):
    entry = Journal.query.get(id)
    if not entry:
        return jsonify({'message': 'Journal entry not found'}), 404
    return jsonify(entry.to_dict()), 200


# Create a new journal entry
@journals_bp.route('/', methods=['POST'])
def create_entry():
    data = request.get_json() or {}

    # Basic validation
    if not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Title and content are required'}), 400

    try:
        new_entry = Journal(
            user_id=data.get('user_id', 1),  # 👈 replace with auth later
            title=data['title'],
            content=data['content'],
            mood_id=data.get('mood_id'),
            is_private=data.get('is_private', False)
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(new_entry.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating journal entry', 'error': str(e)}), 500



# Update a journal entry
@journals_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_entry(id):
    entry = Journal.query.get(id)
    if not entry:
        return jsonify({'message': 'Journal entry not found'}), 404

    data = request.get_json() or {}

    # Update only provided fields
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.mood_id = data.get('mood_id', entry.mood_id)
    entry.is_private = data.get('is_private', entry.is_private)

    try:
        db.session.commit()
        return jsonify(entry.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating journal entry', 'error': str(e)}), 500



# Delete a journal entry
@journals_bp.route('/<int:id>', methods=['DELETE'])
def delete_entry(id):
    entry = Journal.query.get(id)
    if not entry:
        return jsonify({'message': 'Journal entry not found'}), 404

    try:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Journal entry deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting journal entry', 'error': str(e)}), 500