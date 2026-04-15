from flask import request
from blueprints.user_blueprint import user_bp

# Services
from .user_services import (
    register_user,
    login_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user
)

# Exceptions
from .user_exceptions import UserNotFoundError, BadRequestError

# Decorators
from .decorators import token_required, admin_required

# PUBLIC ROUTES (No Auth)

@user_bp.route('/register', methods=['POST'])
def register_user_route():
    try:
        return register_user(request.json)
    except BadRequestError as e:
        return {"error": str(e)}, 400


@user_bp.route('/login', methods=['POST'])
def login_user_route():
    try:
        return login_user(request.json)
    except BadRequestError as e:
        return {"error": str(e)}, 400

# USER ROUTES (Self Access)

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_my_profile():
    user_id = request.user["user_id"]
    return get_user_by_id(user_id)


@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_my_profile():
    user_id = request.user["user_id"]
    return update_user(user_id, request.json, request.user)

@user_bp.route('/profile', methods=['DELETE'])
@token_required
def delete_my_profile():
    user_id = request.user["user_id"]
    return delete_user(user_id, request.user)


# ADMIN ROUTES 

@user_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users_route():
    return get_users()
