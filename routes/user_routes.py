from flask import Blueprint, request
from services.user_services import create_user, get_users, get_user_by_id, update_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['POST'])
def create_user_route():
    data = request.json
    return create_user(data)

@user_bp.route('/users', methods=['GET'])
def get_users_route():
    return get_users()

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user_by_id(user_id)

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.json
    return update_user(user_id, data)