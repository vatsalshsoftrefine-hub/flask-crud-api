from pydantic import ValidationError
from .user_exceptions import UserNotFoundError, BadRequestError
from .user_model import User
from extensions import db
import bcrypt

from .user_schema import RegisterSchema, LoginSchema
from .jwt_utils import generate_token


# REGISTER USER

def register_user(data):
    try:
        user = RegisterSchema(**data)

        existing_user = User.query.filter_by(email=user.email).first()
        if existing_user:
            raise BadRequestError("User already exists")

        hashed_password = bcrypt.hashpw(
            user.password.encode('utf-8'),
            bcrypt.gensalt(rounds=4)
        ).decode('utf-8')

        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            phone=user.phone,
            gender=user.gender,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

    except ValidationError as e:
        raise BadRequestError([err["msg"] for err in e.errors()])

# LOGIN USER

def login_user(data):
    try:
        user_data = LoginSchema(**data)

        user = User.query.filter_by(email=user_data.email).first()

        if not user:
            raise BadRequestError("Invalid credentials")

        if not bcrypt.checkpw(
            user_data.password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
            raise BadRequestError("Invalid credentials")

        token = generate_token(user)

        return {
            "message": "Login successful",
            "token": token
        }, 200

    except ValidationError as e:
        raise BadRequestError([err["msg"] for err in e.errors()])



# GET ALL USERS (ADMIN)

def get_users():
    users = User.query.all()

    return {
        "data": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "phone": u.phone,
                "gender": u.gender,
                "role": u.role
            } for u in users
        ]
    }, 200


# GET USER BY ID

def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")

    return {
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "gender": user.gender,
            "role": user.role
        }
    }, 200



# UPDATE USER

def update_user(user_id, data, current_user):
    user = User.query.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")


    if current_user["role"] != "admin" and current_user["user_id"] != user_id:
        raise BadRequestError("You can only update your own profile")

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)
    user.gender = data.get("gender", user.gender)

    db.session.commit()

    return {"message": "User updated successfully"}, 200


# DELETE USER

def delete_user(user_id, current_user):
    user = User.query.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")


    if current_user["role"] != "admin" and current_user["user_id"] != user_id:
        raise BadRequestError("You can only delete your own profile")

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted successfully"}, 200