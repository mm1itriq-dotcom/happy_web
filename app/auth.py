import datetime
import re
from functools import wraps
import jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = "your-happiness-secret-key-change-in-production"

# Regex for validating email format
def is_valid_email(email: str) -> bool:
    email_regex = r"^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$"
    return bool(re.match(email_regex, email))

# Regex for validating strong password (min 8 chars, 1 lower, 1 upper, 1 number, 1 symbol)
def is_valid_password(password: str) -> bool:
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_#\^\-])[A-Za-z\d@$!%*?&_#\^\-]{8,}$"
    return bool(re.match(password_regex, password))

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, password)

def generate_token(user_id: str) -> str:
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

        # Use Regex for robust Bearer token extraction
        match = re.match(r"^Bearer\s+(.+)$", auth_header, re.IGNORECASE)
        if not match:
            return (
                jsonify({"error": "Invalid token format. Use 'Bearer <token>'"}),
                401,
            )

        token = match.group(1)
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated