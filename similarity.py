# similarity.py

from rapidfuzz import fuzz
import db


SIMILARITY_THRESHOLD = 80


def find_similar(hebrew: str, english: str):
    idioms = db.fetch_all_idioms()
    similar = []

    for row in idioms:
        score_he = fuzz.ratio(hebrew, row["hebrew"])
        score_en = fuzz.ratio(english, row["english"])

        if score_he > SIMILARITY_THRESHOLD or score_en > SIMILARITY_THRESHOLD:
            similar.append({
                "row": row,
                "score_he": score_he,
                "score_en": score_en
            })

    return similar

