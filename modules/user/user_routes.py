from flask import request
from .user_services import create_user, get_users, get_user_by_id, update_user, delete_user
from .user_exceptions import UserNotFoundError, BadRequestError
from blueprints.user_blueprint import user_bp


@user_bp.route('/user', methods=['POST'])
def create_user_route():
    try:
        return create_user(request.json)

    except BadRequestError as e:
        return {"error": str(e)}, 400

    except Exception as e:
        return {"error": str(e)}, 500


@user_bp.route('/users', methods=['GET'])
def get_users_route():
    return get_users()


@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    try:
        return get_user_by_id(user_id)

    except UserNotFoundError as e:
        return {"error": str(e)}, 404


@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    try:
        return update_user(user_id, request.json)

    except UserNotFoundError as e:
        return {"error": str(e)}, 404

    except BadRequestError as e:
        return {"error": str(e)}, 400


@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    try:
        return delete_user(user_id)

    except UserNotFoundError as e:
        return {"error": str(e)}, 404