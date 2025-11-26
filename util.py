import re
import unicodedata


# ---------------------------------------------------------
#  LANGUAGE DETECTION
# ---------------------------------------------------------

HEBREW_RANGE = r"\u0590-\u05FF"

hebrew_re = re.compile(f"[{HEBREW_RANGE}]")
english_re = re.compile(r"[A-Za-z]")


def is_hebrew(text: str) -> bool:
    """Return True if the text contains any Hebrew characters."""
    if not text:
        return False
    return bool(hebrew_re.search(text))


def is_english(text: str) -> bool:
    """Return True if the text contains any English letters."""
    if not text:
        return False
    return bool(english_re.search(text))


# ---------------------------------------------------------
#  NORMALIZATION
# ---------------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize input: strip, normalize unicode, remove zero-width chars."""
    if text is None:
        return ""

    text = text.replace("\u200f", "").replace("\u200e", "")
    text = unicodedata.normalize("NFC", text)
    return text.strip()


# ---------------------------------------------------------
#  VALIDATION HELPERS
# ---------------------------------------------------------

def required_fields_present(*fields: str) -> bool:
    """Return True if all required fields are non-empty after normalization."""
    for f in fields:
        if normalize_text(f) == "":
            return False
    return True


def detect_language_pair(en_candidate: str, he_candidate: str) -> bool:
    """
    Validate that the left field is English and right is Hebrew.
    Used in CLI, but GUI has fixed orientation.
    """
    is_en_ok = is_english(en_candidate) and not is_hebrew(en_candidate)
    is_he_ok = is_hebrew(he_candidate) and not is_english(he_candidate)
    return is_en_ok and is_he_ok


# ---------------------------------------------------------
#  MISC
# ---------------------------------------------------------

def safe_int(s: str, default: int = -1) -> int:
    try:
        return int(s)
    except:
        return default
