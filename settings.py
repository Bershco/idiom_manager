import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")


def load_settings() -> dict:
    """Load settings.json if exists, else return empty dict."""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_settings(settings: dict):
    """Write settings.json."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


def get_db_dir() -> str:
    """Return DB directory string or empty string if not set."""
    settings = load_settings()
    return settings.get("db_dir", "")


def set_db_dir(path: str):
    """Save new DB directory into settings.json."""
    settings = load_settings()
    settings["db_dir"] = path
    save_settings(settings)
