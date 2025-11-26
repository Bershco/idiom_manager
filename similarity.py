import difflib
from typing import Optional, Tuple, Dict
from util import normalize_text, is_hebrew, is_english


# ---------------------------------------------------------
#  INTERNAL HELPERS
# ---------------------------------------------------------

def _similarity(a: str, b: str) -> float:
    """
    Compute similarity ratio using difflib.SequenceMatcher.
    Returns a number between 0 and 1.
    """
    a = normalize_text(a)
    b = normalize_text(b)

    if not a or not b:
        return 0.0

    return difflib.SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------
#  PUBLIC API
# ---------------------------------------------------------

def find_best_match(
    idioms: Dict[int, Dict],
    new_en: str,
    new_he: str,
    threshold_en: float = 0.60,
    threshold_he: float = 0.60
) -> Optional[Tuple[int, float, str]]:
    """
    Compare the new idiom (English + Hebrew) against all existing idioms.
    Returns:
        (best_id, score, "en" or "he")
    OR:
        None if no match exceeds threshold.

    IMPORTANT:
    - English compared only with idiom_en
    - Hebrew compared only with idiom_he
    - Prevents cross-language false positives
    """

    best_id = None
    best_score = 0.0
    best_lang = None

    new_en_norm = normalize_text(new_en)
    new_he_norm = normalize_text(new_he)

    for idiom_id, row in idioms.items():

        # ----- English similarity -----
        existing_en = normalize_text(row["idiom_en"])
        if existing_en and new_en_norm and is_english(new_en_norm):
            score_en = _similarity(new_en_norm, existing_en)
            if score_en >= threshold_en and score_en > best_score:
                best_score = score_en
                best_id = row["id"]
                best_lang = "en"

        # ----- Hebrew similarity -----
        existing_he = normalize_text(row["idiom_he"])
        if existing_he and new_he_norm and is_hebrew(new_he_norm):
            score_he = _similarity(new_he_norm, existing_he)
            if score_he >= threshold_he and score_he > best_score:
                best_score = score_he
                best_id = row["id"]
                best_lang = "he"

    if best_id is None:
        return None

    return (best_id, best_score, best_lang)
