from flask import request, jsonify
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