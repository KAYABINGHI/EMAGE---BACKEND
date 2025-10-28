# app/models/journal.py
from app.db import db
from datetime import datetime


class Journal(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'), nullable=True)
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('journals', lazy=True))
    mood = db.relationship('Mood', backref=db.backref('journals', lazy=True))

    