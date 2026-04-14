from .user_schema import UserSchema
from .user_model import users_db, id_counter
from pydantic import ValidationError
from .user_exceptions import UserNotFoundError, BadRequestError


def create_user(data):
    """
    Create a new user after validating input.
    """
    try:
        # Validate input using Pydantic
        user = UserSchema(**data)

        # Convert to dictionary
        user_dict = user.dict()

        # Generate unique ID
        user_id = id_counter["value"]

        # Assign ID to user
        user_dict["id"] = user_id

        # Store user in dictionary (in-memory DB)
        users_db[user_id] = user_dict

        # Increment ID counter
        id_counter["value"] += 1

        return {
            "message": "User created successfully",
            "data": user_dict
        }, 201

    except ValidationError as e:
        # Extract only error messages (JSON safe)
        error_messages = [err["msg"] for err in e.errors()]

        # Raise custom error (handled in routes)
        raise BadRequestError(error_messages)


def get_users():
    """
    Return all users.
    """
    return {
        "data": list(users_db.values())
    }, 200


def get_user_by_id(user_id):
    """
    Fetch user by ID.
    """
    user = users_db.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")

    return {"data": user}, 200


def update_user(user_id, data):
    """
    Update existing user.
    """
    user = users_db.get(user_id)

    if not user:
        raise UserNotFoundError("User not found")

    try:
        # Validate updated data
        updated_user = UserSchema(**data)

        updated_dict = updated_user.dict()
        updated_dict["id"] = user_id

        # Update user in DB
        users_db[user_id] = updated_dict

        return {
            "message": "User updated successfully",
            "data": updated_dict
        }, 200

    except ValidationError as e:
        error_messages = [err["msg"] for err in e.errors()]
        raise BadRequestError(error_messages)


def delete_user(user_id):
    """
    Delete user by ID.
    """
    if user_id not in users_db:
        raise UserNotFoundError("User not found")

    del users_db[user_id]

    return {
        "message": "User deleted successfully"
    }, 200