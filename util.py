
# util.py

import re

HEBREW_RANGE = re.compile(r'[\u0590-\u05FF]')

def is_hebrew(text: str) -> bool:
    return bool(HEBREW_RANGE.search(text))

def detect_languages(a: str, b: str):
    a_is_he = is_hebrew(a)
    b_is_he = is_hebrew(b)

    if a_is_he and not b_is_he:
        return a, b
    elif b_is_he and not a_is_he:
        return b, a
    else:
        raise ValueError("One must be Hebrew and the other English.")
