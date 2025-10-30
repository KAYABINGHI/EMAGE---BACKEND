from flask import Blueprint, request, jsonify
from app import db
from app.auth.models import User, Therapist
from datetime import datetime, timedelta
import secrets
from functools import wraps
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def admin_required(fn):
    """Decorator to require JWT auth and admin role in JWT claims."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        # Role should have been added to JWT during login
        if claims.get('role') != 'admin':
            return jsonify({'message': 'Admins only'}), 403
        return fn(*args, **kwargs)

    return wrapper

# =====================================
# REGISTER (User or Therapist)
# =====================================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')
    phone_number = data.get('phone_number')
    profile_image = data.get('profile_image')

    # Validation
    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400

    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({'message': 'Username or Email already exists'}), 400

    # Create base user
    user = User(
        username=username,
        email=email,
        phone_number=phone_number,
        role=role,
        profile_image=profile_image
    )
    user.set_password(password)

    db.session.add(user)
    db.session.flush()  # So we can get user.id before committing

    # If therapist, create therapist profile
    if role == 'therapist':
        specialty = data.get('specialty')
        contact_email = data.get('contact_email')

        if not specialty:
            return jsonify({'message': 'Specialty is required for therapists'}), 400

        therapist = Therapist(
            user_id=user.id,
            specialty=specialty,
            contact_email=contact_email,
            phone_number=phone_number,
            profile_image=profile_image
        )
        db.session.add(therapist)

    db.session.commit()

    return jsonify({
        'message': 'Registration successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at
        }
    }), 201


# =====================================
# LOGIN
# =====================================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Include therapist info if applicable
    therapist_data = None
    if user.role == 'therapist' and user.therapist_profile:
        therapist = user.therapist_profile
        therapist_data = {
            'id': therapist.id,
            'specialty': therapist.specialty,
            'bio': therapist.bio,
            'verified': therapist.verified
        }

    # Create a JWT access token that includes the user's role in claims.
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'therapist': therapist_data
        }
    }), 200


# =====================================
# FORGOT PASSWORD
# =====================================
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.reset_token = secrets.token_urlsafe(32)
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    # In production: email the reset token instead
    return jsonify({
        'message': 'Reset token generated successfully',
        'reset_token': user.reset_token
    }), 200


# =====================================
# RESET PASSWORD
# =====================================
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not token or not password or not confirm_password:
        return jsonify({'message': 'All fields are required'}), 400

    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match'}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user:
        return jsonify({'message': 'Invalid token'}), 400

    if user.reset_token_expires < datetime.utcnow():
        return jsonify({'message': 'Reset token has expired'}), 400

    user.set_password(password)
    user.reset_token = None
    user.reset_token_expires = None
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200


# ================================
# Admin-only endpoints
# ================================


@auth_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    """Return simple statistics for admin dashboard."""
    total_users = User.query.count()
    total_therapists = Therapist.query.count()
    pending_therapists = Therapist.query.filter_by(verified=False).count()

    # Simple system health metric placeholder (could be extended)
    system_health = '92%'

    return jsonify({
        'total_users': total_users,
        'total_therapists': total_therapists,
        'pending_therapists': pending_therapists,
        'system_health': system_health
    }), 200


@auth_bp.route('/admin/users', methods=['GET'])
@admin_required
def admin_list_users():
    """List users with optional pagination (admin only)."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    users = [
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'created_at': u.created_at
        }
        for u in pagination.items
    ]
    return jsonify({'users': users, 'total': pagination.total}), 200


@auth_bp.route('/admin/users/<int:user_id>/promote', methods=['PUT'])
@admin_required
def admin_promote_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.promote_to_admin()
    db.session.commit()
    return jsonify({'message': 'User promoted to admin', 'user_id': user.id}), 200


@auth_bp.route('/admin/users/<int:user_id>/demote', methods=['PUT'])
@admin_required
def admin_demote_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.demote_to_user()
    db.session.commit()
    return jsonify({'message': 'User demoted to user', 'user_id': user.id}), 200


@auth_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@auth_bp.route('/admin/therapists', methods=['GET'])
@admin_required
def admin_list_therapists():
    therapists = Therapist.query.order_by(Therapist.created_at.desc()).all()
    items = [
        {
            'id': t.id,
            'user_id': t.user_id,
            'specialty': t.specialty,
            'verified': t.verified,
            'created_at': t.created_at
        }
        for t in therapists
    ]
    return jsonify({'therapists': items}), 200


@auth_bp.route('/admin/therapists/<int:therapist_id>/verify', methods=['PUT'])
@admin_required
def admin_verify_therapist(therapist_id):
    t = Therapist.query.get(therapist_id)
    if not t:
        return jsonify({'message': 'Therapist not found'}), 404
    t.verified = True
    db.session.commit()
    return jsonify({'message': 'Therapist verified', 'therapist_id': t.id}), 200


@auth_bp.route('/admin/therapists/<int:therapist_id>', methods=['DELETE'])
@admin_required
def admin_delete_therapist(therapist_id):
    t = Therapist.query.get(therapist_id)
    if not t:
        return jsonify({'message': 'Therapist not found'}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Therapist deleted'}), 200
