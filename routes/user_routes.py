from flask import Blueprint, request
from services.user_services import create_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['POST'])
def create_user_route():
    data = request.json
    return create_user(data)