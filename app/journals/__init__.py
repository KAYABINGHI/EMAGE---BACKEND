from flask import Blueprint, request, jsonify
from app.db import db
from app.journals.models import Journal
from app.journals.utils import validate_journal_data, format_tags
from datetime import datetime


journal_bp = Blueprint('journal', __name__, url_prefix='/journals')

@journal_bp.route('/create', methods=['POST'])
def create_journal():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'title', 'content']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Additional validation
        validation_errors = validate_journal_data(data)
        if validation_errors:
            return jsonify({'errors': validation_errors}), 400
        
        # Create new journal entry
        new_journal = Journal(
            user_id=data['user_id'],
            title=data['title'].strip(),
            content=data['content'].strip(),
            mood=data.get('mood'),
            tags=format_tags(data.get('tags', [])),
            is_public=data.get('is_public', False)
        )
        
        db.session.add(new_journal)
        db.session.commit()
        
        return jsonify({
            'message': 'Journal entry created successfully',
            'journal': new_journal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_journals(user_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get journals with pagination
        journals_query = Journal.query.filter_by(user_id=user_id)
        
        # Optional filters
        if request.args.get('mood'):
            journals_query = journals_query.filter_by(mood=request.args['mood'])
        
        if request.args.get('public_only'):
            journals_query = journals_query.filter_by(is_public=True)
        
        # Order by latest first
        journals = journals_query.order_by(Journal.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'journals': [journal.to_dict() for journal in journals.items],
            'pagination': {
                'page': journals.page,
                'per_page': journals.per_page,
                'total': journals.total,
                'pages': journals.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/<int:journal_id>', methods=['GET'])
def get_journal(journal_id):
    try:
        journal = Journal.query.get_or_404(journal_id)
        
        # Check if user can access this journal
        # You might want to add proper authorization here
        return jsonify({
            'journal': journal.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@journal_bp.route('/<int:journal_id>', methods=['PUT'])
def update_journal(journal_id):
    try:
        data = request.get_json()
        journal = Journal.query.get_or_404(journal_id)
        
        # Update fields if provided
        if 'title' in data:
            journal.title = data['title'].strip()
        
        if 'content' in data:
            journal.content = data['content'].strip()
        
        if 'mood' in data:
            journal.mood = data['mood']
        
        if 'tags' in data:
            journal.tags = format_tags(data['tags'])
        
        if 'is_public' in data:
            journal.is_public = data['is_public']
        
        journal.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Journal updated successfully',
            'journal': journal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/<int:journal_id>', methods=['DELETE'])
def delete_journal(journal_id):
    try:
        journal = Journal.query.get_or_404(journal_id)
        
        db.session.delete(journal)
        db.session.commit()
        
        return jsonify({
            'message': 'Journal deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/public', methods=['GET'])
def get_public_journals():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        journals = Journal.query.filter_by(is_public=True)\
            .order_by(Journal.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'journals': [journal.to_dict() for journal in journals.items],
            'pagination': {
                'page': journals.page,
                'per_page': journals.per_page,
                'total': journals.total,
                'pages': journals.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

        from app.db import db
from datetime import datetime

class Journal(db.Model):
    __tablename__ = 'journals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'), nullable=True)  

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500))  # Comma-separated tags
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('journals', lazy=True))
    mood = db.relationship('Mood', backref=db.backref('journals', lazy=True))  # Link to Mood model

    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'mood': self.mood.emotion_label if self.mood else None,  
            'tags': self.tags.split(',') if self.tags else [],
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
from flask import Blueprint

journals_bp = Blueprint('journals', __name__, url_prefix="/journals")

from app.journals import routes  # Import routes after blueprint creation
