from .user_schema import UserSchema
from .user_model import users_db, id_counter
from pydantic import ValidationError
from .user_exceptions import UserNotFoundError , BadRequestError


def create_user(data):
    try:
        # Validate input
        user = UserSchema(**data)
        user_dict = user.dict()

        # Get current ID
        user_id = id_counter["value"]

        # Assign ID
        user_dict["id"] = user_id

        # Store user
        users_db[user_id] = user_dict

        # Increment ID
        id_counter["value"] += 1

        return {
            "message": "User created successfully",
            "data": user_dict
        }, 201

    except ValidationError as e:
        return {"errors": e.errors()}, 400

    except Exception as e:
        return {"error": str(e)}, 500

def get_users():
    """
    Returns all users stored in the in-memory database.
    """
    try:
        return {
            "data": list(users_db.values())
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500

def get_user_by_id(user_id):
    user = users_db.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")

    return {"data": user}, 200

def update_user(user_id, data):
    user = users_db.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")

    try:
        updated_user = UserSchema(**data)
        updated_dict = updated_user.dict()
        updated_dict["id"] = user_id

        users_db[user_id] = updated_dict

        return {
            "message": "User updated successfully",
            "data": updated_dict
        }, 200

    except ValidationError as e:
        raise BadRequestError(e.errors())


def delete_user(user_id):
    if user_id not in users_db:
        raise UserNotFoundError("User not found")

    del users_db[user_id]

    return {"message": "User deleted successfully"}, 200