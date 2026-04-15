from functools import wraps
from flask import request
from .jwt_utils import verify_token


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"error": "Token is missing"}, 401

        try:
            token = auth_header.split(" ")[1]
        except:
            return {"error": "Invalid token format"}, 401

        decoded = verify_token(token)

        if not decoded:
            return {"error": "Invalid or expired token"}, 401

        # Attach user info
        request.user = decoded

        return f(*args, **kwargs)

    return wrapper

def admin_required(f):
    from functools import wraps
    from flask import request

    @wraps(f)
    def wrapper(*args, **kwargs):

        if request.user.get("role") != "admin":
            return {"error": "Admin access required"}, 403

        return f(*args, **kwargs)

    return wrapper