from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth import bp
from app.auth.models import User
from app import db
from datetime import timedelta


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
    if not all(field in data for field in required_fields):
        return jsonify({
            'message': 'Username, email,phone_number and password are required'
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

    # Create new user
    user = User(username=data['username'], email=data['email'],phone_number=data['phone_number'], password=data['password'],confirm_password=data['confirm_password'])
    db.session.add(user)
    db.session.commit()

    # Create access token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

