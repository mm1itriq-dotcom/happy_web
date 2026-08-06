import logging
import uuid
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import insert, select, desc
from app.db import engine
from app.models import users, sentiments
from app.auth import hash_password, verify_password, generate_token, token_required, is_valid_email, is_valid_password
from app.sentiment import analyze_text
from app.exceptions import register_error_handlers, ValidationError, AuthenticationError, ResourceExistsError

app = Flask(__name__)
# Enable CORS for all routes so the frontend can connect
CORS(app)

# Register custom exception handlers
register_error_handlers(app)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Happiness API is running!"}), 200

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        raise ValidationError("Missing required fields")

    if not is_valid_email(email):
        raise ValidationError("Invalid email format")

    if not is_valid_password(password):
        raise ValidationError("Password must be at least 8 characters and contain an uppercase letter, a lowercase letter, a number, and a symbol")

    hashed_pw = hash_password(password)
    new_user_id = str(uuid.uuid4())

    with engine.begin() as conn:
        # Check if user already exists
        existing_user = conn.execute(select(users).where(users.c.email == email)).fetchone()
        if existing_user:
            raise ResourceExistsError("Email already registered")

        # Insert new user into the database
        conn.execute(
            insert(users).values(
                id=new_user_id,
                name=name,
                email=email,
                password_hash=hashed_pw,
                created_at=datetime.datetime.utcnow()
            )
        )

    return jsonify({"message": "User registered successfully", "user_id": new_user_id}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise ValidationError("Missing required fields")

    with engine.connect() as conn:
        user = conn.execute(select(users).where(users.c.email == email)).fetchone()

    # Check if user exists and password is correct
    if not user or not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid email or password")

    # Generate an auth token for future requests
    token = generate_token(user.id)
    return jsonify({"message": "Login successful", "token": token, "name": user.name}), 200


@app.route("/analyze", methods=["POST"])
@token_required
def analyze(current_user_id):
    data = request.get_json()
    text = data.get("text")

    if not text:
        raise ValidationError("Text is required")

    # Run the sentiment analysis logic you wrote
    analysis_result = analyze_text(text)
    new_sentiment_id = str(uuid.uuid4())

    # Save the analysis result to the database linked to this user
    with engine.begin() as conn:
        conn.execute(
            insert(sentiments).values(
                id=new_sentiment_id,
                user_id=current_user_id,
                input_text=text,
                sentiment_label=analysis_result["user_state"],
                happy_percentage=analysis_result["happy_percentage"],
                sad_percentage=analysis_result["sad_percentage"],
                neutral_percentage=analysis_result["neutral_percentage"],
                created_at=datetime.datetime.utcnow()
            )
        )

    return jsonify(analysis_result), 200


@app.route("/history", methods=["GET"])
@token_required
def get_history(current_user_id):
    with engine.connect() as conn:
        # Fetch sentiments for this user, newest first
        stmt = select(sentiments).where(sentiments.c.user_id == current_user_id).order_by(desc(sentiments.c.created_at))
        rows = conn.execute(stmt).fetchall()

    history = []
    for row in rows:
        history.append({
            "id": row.id,
            "text": row.input_text,
            "sentiment_label": row.sentiment_label,
            "happy_percentage": row.happy_percentage,
            "sad_percentage": row.sad_percentage,
            "neutral_percentage": row.neutral_percentage,
            "created_at": row.created_at.isoformat() if row.created_at else None
        })

    return jsonify({"history": history}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)