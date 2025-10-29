# app/community/routes.py
from flask import Blueprint, request, jsonify
from app.db import db
from datetime import datetime
from app.community.models import (
    Community, CommunityMembership, CommunityMessage,
    DirectMessage, Connection
)
from app.auth.models import User

community_bp = Blueprint('community', __name__, url_prefix='/community')


# Helper: Convert model to dict
def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


# 1. List Communities
@community_bp.route('/', methods=['GET'])
def list_communities():
    communities = Community.query.order_by(Community.created_at.desc()).all()
    return jsonify([to_dict(c) for c in communities])


# 2. Create Community
@community_bp.route('/create', methods=['POST'])
def create_community():
    data = request.get_json() or {}
    name = data.get('name')
    owner_id = data.get('owner_id')
    description = data.get('description')
    is_private = data.get('is_private', False)

    if not name or not owner_id:
        return jsonify({'error': 'name and owner_id required'}), 400

    if not User.query.get(owner_id):
        return jsonify({'error': 'Owner not found'}), 404

    if Community.query.filter_by(name=name).first():
        return jsonify({'error': 'Community name already exists'}), 400

    community = Community(
        name=name,
        description=description,
        is_private=is_private,
        owner_id=owner_id
    )
    db.session.add(community)
    db.session.flush()  # Get ID before commit

    # Add owner as member
    membership = CommunityMembership(
        user_id=owner_id,
        community_id=community.id,
        role='owner'
    )
    db.session.add(membership)
    db.session.commit()

    return jsonify(to_dict(community)), 201


# 3. Join Community
@community_bp.route('/<int:community_id>/join', methods=['POST'])
def join_community(community_id):
    data = request.get_json() 
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    community = Community.query.get(community_id)
    if not community:
        return jsonify({'error': 'Community not found'}), 404

    if community.is_private:
        return jsonify({'error': 'Cannot join private community directly'}), 403

    if CommunityMembership.query.filter_by(user_id=user_id, community_id=community_id).first():
        return jsonify({'error': 'Already a member'}), 400

    membership = CommunityMembership(user_id=user_id, community_id=community_id)
    db.session.add(membership)
    db.session.commit()

    return jsonify({'message': 'Joined successfully'}), 201


# 4. Leave Community
@community_bp.route('/<int:community_id>/leave', methods=['POST'])
def leave_community(community_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    membership = CommunityMembership.query.filter_by(
        user_id=user_id, community_id=community_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member'}), 404

    if membership.role == 'owner':
        return jsonify({'error': 'Owner cannot leave. Transfer ownership first.'}), 403

    db.session.delete(membership)
    db.session.commit()

    return jsonify({'message': 'Left community'}), 200


# 5. Get Messages
@community_bp.route('/<int:community_id>/messages', methods=['GET'])
def get_messages(community_id):
    if not Community.query.get(community_id):
        return jsonify({'error': 'Community not found'}), 404

    messages = CommunityMessage.query.filter_by(community_id=community_id)\
        .order_by(CommunityMessage.created_at.asc()).all()

    return jsonify([to_dict(m) for m in messages])


# 6. Post Message
@community_bp.route('/<int:community_id>/message', methods=['POST'])
def post_message(community_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')
    content = data.get('content')

    if not user_id or not content:
        return jsonify({'error': 'user_id and content required'}), 400

    if not CommunityMembership.query.filter_by(user_id=user_id, community_id=community_id).first():
        return jsonify({'error': 'Not a member'}), 403

    message = CommunityMessage(
        community_id=community_id,
        user_id=user_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()

    return jsonify(to_dict(message)), 201


# 7. Send Direct Message
@community_bp.route('/message/direct', methods=['POST'])
def send_direct_message():
    data = request.get_json() or {}
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    content = data.get('content')

    if not all([sender_id, recipient_id, content]):
        return jsonify({'error': 'sender_id, recipient_id, content required'}), 400

    if sender_id == recipient_id:
        return jsonify({'error': 'Cannot send message to yourself'}), 400

    if not User.query.get(sender_id) or not User.query.get(recipient_id):
        return jsonify({'error': 'User not found'}), 404

    dm = DirectMessage(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content
    )
    db.session.add(dm)
    db.session.commit()

    return jsonify(to_dict(dm)), 201


# 8. Get Inbox
@community_bp.route('/messages/inbox/<int:user_id>', methods=['GET'])
def get_inbox(user_id):
    if not User.query.get(user_id):
        return jsonify({'error': 'User not found'}), 404

    messages = DirectMessage.query.filter_by(recipient_id=user_id)\
        .order_by(DirectMessage.created_at.desc()).all()

    return jsonify([to_dict(m) for m in messages])


# 9. Mark Message as Read
@community_bp.route('/message/<int:message_id>/read', methods=['POST'])
def mark_message_read(message_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')

    message = DirectMessage.query.get(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    if message.recipient_id != user_id:
        return jsonify({'error': 'Not your message'}), 403

    message.is_read = True
    db.session.commit()

    return jsonify({'message': 'Marked as read'}), 200


# 10. Connect Users
@community_bp.route('/connect', methods=['POST'])
def connect_users():
    data = request.get_json() or {}
    requester_id = data.get('requester_id')
    addressee_id = data.get('addressee_id')

    if not requester_id or not addressee_id:
        return jsonify({'error': 'Both IDs required'}), 400

    if requester_id == addressee_id:
        return jsonify({'error': 'Cannot connect to yourself'}), 400

    if not User.query.get(requester_id) or not User.query.get(addressee_id):
        return jsonify({'error': 'User not found'}), 404

    # Check existing connection
    existing = Connection.query.filter(
        ((Connection.requester_id == requester_id) & (Connection.addressee_id == addressee_id)) |
        ((Connection.requester_id == addressee_id) & (Connection.addressee_id == requester_id))
    ).first()

    if existing:
        if existing.status == 'pending' and existing.requester_id == addressee_id:
            existing.status = 'accepted'
            existing.accepted_at = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Connection accepted!', 'connection': to_dict(existing)})
        return jsonify({'message': 'Connection exists', 'status': existing.status}), 200

    conn = Connection(requester_id=requester_id, addressee_id=addressee_id, status='pending')
    db.session.add(conn)
    db.session.commit()

    return jsonify(to_dict(conn)), 201


# 11. List Connections
@community_bp.route('/connections/<int:user_id>', methods=['GET'])
def list_connections(user_id):
    if not User.query.get(user_id):
        return jsonify({'error': 'User not found'}), 404

    conns = Connection.query.filter(
        ((Connection.requester_id == user_id) | (Connection.addressee_id == user_id)) &
        (Connection.status == 'accepted')
    ).all()

    return jsonify([to_dict(c) for c in conns])