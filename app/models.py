import uuid
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    func,
)

metadata = MetaData()

# Table: users
users = Table(
    "users",
    metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("name", String(100), nullable=False),
    Column("email", String(120), nullable=False, unique=True),
    Column("password_hash", String(255), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)

# Table: sentiments
sentiments = Table(
    "sentiments",
    metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("user_id", String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("input_text", Text, nullable=False),
    Column("sentiment_label", String(50), nullable=False),
    Column("happy_percentage", Float, nullable=False),
    Column("sad_percentage", Float, nullable=False),
    Column("neutral_percentage", Float, nullable=False, default=0.0),
    Column("created_at", DateTime, server_default=func.now()),
)

# Table: words (word is the PRIMARY KEY)
words = Table(
    "words",
    metadata,
    Column("word", String(100), primary_key=True),
    Column("category", String(50), nullable=False),  # 'happy', 'sad', or 'neutral'
)
