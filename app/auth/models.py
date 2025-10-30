from app.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)  # 'user' | 'therapist'
    is_verified = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(255), nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship (one-to-one)
    therapist_profile = db.relationship("Therapist", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """Return True if the user has the 'admin' role."""
        return (self.role or '').lower() == 'admin'

    def promote_to_admin(self):
        """Promote this user to admin role."""
        self.role = 'admin'

    def demote_to_user(self):
        """Demote this user to a normal 'user' role."""
        self.role = 'user'



class Therapist(db.Model):
    __tablename__ = 'therapists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    contact_email = db.Column(db.String(150), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.Text, nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
