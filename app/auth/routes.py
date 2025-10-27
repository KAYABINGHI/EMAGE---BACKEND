from flask import request, jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth.models import User
from datetime import timedelta
from app.db import bcrypt,db
from flask import Blueprint

bp = Blueprint('auth', __name__,url_prefix="/auth")


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    # Validate required fields
    required_fields = [
        'username',
        'email',
        'phone_number',
        'password',
        'confirm_password'
    ]
    
    # Check if all required fields are present
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'message': 'Username already exists'
        }), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'message': 'Email already exists'
        }), 400

    if User.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({
            'message': 'Phone number already exists'
        }), 400

    # Check password confirmation
    if data.get('password') != data.get('confirm_password'):
        return jsonify({'message': 'Password and confirm_password do not match'}), 400

    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            phone_number=data['phone_number']
        )

        # Set password using bcrypt hashing
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': f'Error creating user: {str(e)}'
        }), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    required_fields = ['email', 'password']
    missing_fields = [f for f in required_fields if f not in data or not data[f]]

    if missing_fields:
        return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Email does not exist'}), 404

    # Check password (using your model method)
    if not user.check_password(data['password']):
        return jsonify({'message': 'Invalid password'}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}

    # Check if email is provided
    if 'email' not in data or not data['email']:
        return jsonify({'message': 'Email is required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Email does not exist'}), 404

    # Create short-lived reset token (valid for 15 minutes)
    reset_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=15)
    )

    # Normally, you'd send this link via email
    reset_link = f"http://127.0.0.1:5000/reset-password?token={reset_token}"

    # For testing, we’ll return the link in the response
    return jsonify({
        'message': 'Password reset link generated successfully',
        'reset_link': reset_link,
        'token': reset_token
    }), 200

@bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    data = request.get_json() or {}

    if 'new_password' not in data or not data['new_password']:
        return jsonify({'message': 'New password is required'}), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Use your model’s password setter
    user.set_password(data['password'])
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200