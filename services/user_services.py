from schemas.user_schemas import UserSchema
from models.user_models import users
from pydantic import ValidationError

def create_user(data):
    try:
        user = UserSchema(**data)
        user_dict = user.dict()

        # Add ID
        user_dict["id"] = len(users) + 1

        users.append(user_dict)

        return {
            "message": "User created successfully",
            "data": user_dict
        }, 201

    except ValidationError as e:
        return {"errors": e.errors()}, 400
def get_users():
    return {
        "data": users
    }, 200

def get_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return {"data": user}, 200

    return {"message": "User not found"}, 404