import os
import json
from sqlalchemy import select, insert
from app.db import engine
from app.models import words

def seed_words():
    json_path = os.path.join(os.path.dirname(__file__), "words.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = {
        "happy": data.get("happy_words", []),
        "sad": data.get("sad_words", []),
        "neutral": data.get("neutral_words", []),
    }

    with engine.connect() as conn:
        for category, word_list in categories.items():
            for word_str in word_list:
                word_clean = word_str.strip().lower()
                existing = conn.execute(
                    select(words.c.word).where(words.c.word == word_clean)
                ).fetchone()
                if not existing:
                    conn.execute(
                        insert(words).values(word=word_clean, category=category)
                    )

        conn.commit()
        print("Words seeded into database using 'word' as Primary Key!")

if __name__ == "__main__":
    seed_words()
