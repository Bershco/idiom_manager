# db.py

import sqlite3
import os
from pathlib import Path
from datetime import datetime


def detect_default_drive_path():
    """
    Detect Google Drive Desktop folder on Windows or macOS.

    Your setup:
    Google Drive is mounted as G:\My Drive\

    So we check for:
        G:\My Drive
    """

    # Your actual confirmed Google Drive Desktop folder
    my_drive = Path("G:/My Drive")
    if my_drive.exists():
        return my_drive / "shared_idioms" / "idioms.db"

    # Fallbacks (optional, in case you or teammates have different setups)
    google_drive_old = Path("G:/Google Drive")
    if google_drive_old.exists():
        return google_drive_old / "shared_idioms" / "idioms.db"

    root_drive = Path("G:/")
    if root_drive.exists():
        return root_drive / "shared_idioms" / "idioms.db"

    home_google = Path.home() / "Google Drive"
    if home_google.exists():
        return home_google / "shared_idioms" / "idioms.db"

    home_my_drive = Path.home() / "My Drive"
    if home_my_drive.exists():
        return home_my_drive / "shared_idioms" / "idioms.db"

    # Final fallback
    return Path.home() / "shared_idioms" / "idioms.db"



CUSTOM_DB_DIR = os.getenv("IDIOM_DB_DIR")
if CUSTOM_DB_DIR:
    DB_PATH = Path(CUSTOM_DB_DIR) / "idioms.db"
else:
    DB_PATH = detect_default_drive_path()


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS idioms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hebrew TEXT NOT NULL,
        english TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS variants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idiom_id INTEGER NOT NULL,
        lang TEXT NOT NULL CHECK(lang IN ('he', 'en')),
        variant TEXT NOT NULL,
        FOREIGN KEY(idiom_id) REFERENCES idioms(id)
    )
    """)

    conn.commit()
    conn.close()


def insert_idiom(hebrew: str, english: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO idioms (hebrew, english, created_at) VALUES (?, ?, ?)",
        (hebrew, english, datetime.utcnow())
    )
    conn.commit()
    conn.close()


def insert_variant(idiom_id: int, variant_text: str, lang: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO variants (idiom_id, lang, variant) VALUES (?, ?, ?)",
        (idiom_id, lang, variant_text)
    )
    conn.commit()
    conn.close()


def fetch_all_idioms():
    """
    Returns idioms with TWO grouped columns:
    - hebrew_variants
    - english_variants
    """

    conn = get_conn()
    c = conn.cursor()

    query = """
        SELECT 
            idioms.id,
            idioms.hebrew,
            idioms.english,
            idioms.created_at,
            GROUP_CONCAT(CASE WHEN variants.lang='he' THEN variants.variant END, ', ') AS hebrew_variants,
            GROUP_CONCAT(CASE WHEN variants.lang='en' THEN variants.variant END, ', ') AS english_variants
        FROM idioms
        LEFT JOIN variants ON idioms.id = variants.idiom_id
        GROUP BY idioms.id
        ORDER BY idioms.id
    """

    rows = c.execute(query).fetchall()
    conn.close()
    return rows


def find_exact_match(h: str, e: str):
    conn = get_conn()
    c = conn.cursor()
    row = c.execute("SELECT * FROM idioms WHERE hebrew=? AND english=?", (h, e)).fetchone()
    conn.close()
    return row


def find_by_hebrew(h: str):
    conn = get_conn()
    c = conn.cursor()
    row = c.execute("SELECT * FROM idioms WHERE hebrew=?", (h,)).fetchone()
    conn.close()
    return row


def find_by_english(e: str):
    conn = get_conn()
    c = conn.cursor()
    row = c.execute("SELECT * FROM idioms WHERE english=?", (e,)).fetchone()
    conn.close()
    return row


def count_idioms():
    conn = get_conn()
    c = conn.cursor()
    (count,) = c.execute("SELECT COUNT(*) FROM idioms").fetchone()
    conn.close()
    return count
