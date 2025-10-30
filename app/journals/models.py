# app/models/journal.py
from app.db import db
from datetime import datetime


class Journal(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref=db.backref('journals', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'is_private': self.is_private,
            'created_at': self.created_at.strftime("%a, %b %d, %Y"),
            'updated_at': self.updated_at.strftime("%a, %b %d, %Y") if self.updated_at else None
        }