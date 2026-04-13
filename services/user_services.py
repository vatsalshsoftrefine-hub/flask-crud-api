from schemas.user_schemas import UserSchema
from models.user_models import users
from pydantic import ValidationError

def create_user(data):
    try:
        # Validate data
        user = UserSchema(**data)

        # Convert to dictionary
        user_dict = user.dict()

        # Store in list (acting as DB)
        users.append(user_dict)

        return {
            "message": "User created successfully",
            "data": user_dict
        }, 201

    except ValidationError as e:
        return {
            "errors": e.errors()
        }, 400
def get_users():
    return {
        "data": users
    }, 200