import re
from sqlalchemy import select
from app.db import engine
from app.models import words

def analyze_text(text: str) -> dict:
    if not text or not text.strip():
        return {
            "happy_percentage": 0.0,
            "sad_percentage": 0.0,
            "neutral_percentage": 100.0,
            "user_state": "Neutral",
            "happy_count": 0,
            "sad_count": 0,
            "neutral_count": 0,
        }

    # Extract all lowercase words from sentence
    words_in_text = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    if not words_in_text:
        return {
            "happy_percentage": 0.0,
            "sad_percentage": 0.0,
            "neutral_percentage": 100.0,
            "user_state": "Neutral",
            "happy_count": 0,
            "sad_count": 0,
            "neutral_count": 0,
        }

    # Query Primary Key 'word' in PostgreSQL for matching categories
    with engine.connect() as conn:
        stmt = select(words.c.word, words.c.category).where(words.c.word.in_(words_in_text))
        matched_rows = conn.execute(stmt).fetchall()
        word_category_map = {row[0]: row[1] for row in matched_rows}

    happy_count = 0
    sad_count = 0
    neutral_count = 0

    for word in words_in_text:
        cat = word_category_map.get(word)
        if cat == "happy":
            happy_count += 1
        elif cat == "sad":
            sad_count += 1
        elif cat == "neutral":
            neutral_count += 1

    emotional_total = happy_count + sad_count

    if emotional_total == 0:
        happy_percentage = 0.0
        sad_percentage = 0.0
        neutral_percentage = 100.0
        user_state = "Neutral"
    else:
        happy_percentage = round((happy_count / emotional_total) * 100, 1)
        sad_percentage = round((sad_count / emotional_total) * 100, 1)
        neutral_percentage = 0.0

        if happy_percentage > sad_percentage:
            user_state = "Happy"
        elif sad_percentage > happy_percentage:
            user_state = "Sad"
        else:
            user_state = "Mixed"

    return {
        "happy_percentage": happy_percentage,
        "sad_percentage": sad_percentage,
        "neutral_percentage": neutral_percentage,
        "user_state": user_state,
        "happy_count": happy_count,
        "sad_count": sad_count,
        "neutral_count": neutral_count,
    }
