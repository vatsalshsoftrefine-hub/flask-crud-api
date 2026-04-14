from .user_schema import UserSchema
from .user_model import users_db
from pydantic import ValidationError
from .user_exceptions import UserNotFoundError , BadRequestError

# Temporary counter to assign unique IDs to users
current_id = 1


def create_user(data):
    """
    Creates a new user after validating input data.
    """
    global current_id
    try:
        # Step 1: Validate incoming data using Pydantic schema
        user = UserSchema(**data)

        # Step 2: Convert validated object into dictionary
        user_dict = user.dict()

        # Step 3: Assign a unique ID to the user
        user_dict["id"] = current_id

        # Step 4: Store user in dictionary (acting as in-memory database)
        users_db[current_id] = user_dict

        # Step 5: Increment ID for next user
        current_id += 1

        # Step 6: Return success response
        return {
            "message": "User created successfully",
            "data": user_dict
        }, 201

    except ValidationError as e:
        # Handles validation errors (invalid input data)
        return {"errors": e.errors()}, 400

    except Exception as e:
        # Handles unexpected errors
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