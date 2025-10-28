from app.db import db, bcrypt
from datetime import datetime

class Mood(db.Model):
    __tablename__ = 'moods'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    emotion_label = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('moods', lazy=True))  
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'emotion_label': self.emotion_label,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
