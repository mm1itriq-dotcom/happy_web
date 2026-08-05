import datetime
from functools import wraps
import jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = "your-happiness-secret-key-change-in-production"


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, password)


def generate_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return (
                jsonify({"error": "Invalid token format. Use 'Bearer <token>'"}),
                401,
            )

        token = parts[1]
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated
