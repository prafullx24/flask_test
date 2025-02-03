from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
        'is_active': user.is_active
    })

@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    name = data.get('name', user.name)
    email = data.get('email', user.email)
    password = data.get('password')

    if password:
        user.set_password(password)

    user.name = name
    user.email = email
    user.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 200
