import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple, Dict

# ---------------------------------------------------------
#  DB PATH IS SET EXTERNALLY BY settings.py
#  Every file importing db.py must call: set_db_path(directory)
# ---------------------------------------------------------

DB_PATH: Optional[Path] = None


# ---------------------------------------------------------
#  PUBLIC SETTER
# ---------------------------------------------------------
def set_db_path(db_dir: str):
    """
    Call this once at startup to tell the DB module
    where idioms.db is located.
    """
    global DB_PATH
    p = Path(db_dir)
    p.mkdir(parents=True, exist_ok=True)
    DB_PATH = p / "idioms.db"


# ---------------------------------------------------------
#  INTERNAL HELPERS
# ---------------------------------------------------------
def _get_conn() -> sqlite3.Connection:
    if DB_PATH is None:
        raise RuntimeError("DB_PATH not set. Call set_db_path() before using db.py")

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Improve reliability on Google Drive sync
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


# ---------------------------------------------------------
#  SCHEMA INIT
# ---------------------------------------------------------
def init_db():
    conn = _get_conn()
    cur = conn.cursor()

    # Main idioms table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS idioms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            idiom_en TEXT NOT NULL,
            idiom_he TEXT NOT NULL,

            translation_en TEXT NOT NULL,
            translation_he TEXT NOT NULL,

            half_en TEXT,
            half_he TEXT,

            off_en TEXT,
            off_he TEXT
        );
    """)

    # Variants linking table (bidirectional)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS variants_link (
            idiom_id INTEGER NOT NULL,
            variant_id INTEGER NOT NULL,

            PRIMARY KEY (idiom_id, variant_id),

            FOREIGN KEY (idiom_id) REFERENCES idioms(id) ON DELETE CASCADE,
            FOREIGN KEY (variant_id) REFERENCES idioms(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------
#  INSERT IDIOM
# ---------------------------------------------------------
def add_idiom(
    *,
    created_by: str,
    idiom_en: str,
    idiom_he: str,
    translation_en: str,
    translation_he: str,
    half_en: Optional[str],
    half_he: Optional[str],
    off_en: Optional[str],
    off_he: Optional[str],
) -> int:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO idioms (
            created_by,
            idiom_en, idiom_he,
            translation_en, translation_he,
            half_en, half_he,
            off_en, off_he
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        created_by,
        idiom_en, idiom_he,
        translation_en, translation_he,
        half_en, half_he,
        off_en, off_he
    ))

    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


# ---------------------------------------------------------
#  VARIANT LINKING
# ---------------------------------------------------------
def add_variant_link(id1: int, id2: int):
    """
    Bidirectional linking:
      (id1, id2) and (id2, id1)
    """
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO variants_link (idiom_id, variant_id)
        VALUES (?, ?);
    """, (id1, id2))

    cur.execute("""
        INSERT OR IGNORE INTO variants_link (idiom_id, variant_id)
        VALUES (?, ?);
    """, (id2, id1))

    conn.commit()
    conn.close()


def get_variants(idiom_id: int) -> List[int]:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT variant_id
        FROM variants_link
        WHERE idiom_id = ?;
    """, (idiom_id,))

    rows = cur.fetchall()
    conn.close()

    return [r["variant_id"] for r in rows]


# ---------------------------------------------------------
#  GET IDIOM
# ---------------------------------------------------------
def get_idiom(idiom_id: int) -> Optional[Dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM idioms WHERE id = ?;", (idiom_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


# ---------------------------------------------------------
#  GET ALL IDIOMS
# ---------------------------------------------------------
def get_all_idioms() -> List[Dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM idioms ORDER BY id;")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------
#  USER COUNT
# ---------------------------------------------------------
def count_user_idioms(username: str) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) AS c
        FROM idioms
        WHERE created_by = ?;
    """, (username,))
    result = cur.fetchone()["c"]
    conn.close()
    return result


# ---------------------------------------------------------
#  DELETE IDIOM
# ---------------------------------------------------------
def delete_idiom(idiom_id: int) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM idioms WHERE id = ?;", (idiom_id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    return affected > 0


# ---------------------------------------------------------
#  EDIT IDIOM
# ---------------------------------------------------------
def update_idiom(
    idiom_id: int,
    *,
    idiom_en: str,
    idiom_he: str,
    translation_en: str,
    translation_he: str,
    half_en: Optional[str],
    half_he: Optional[str],
    off_en: Optional[str],
    off_he: Optional[str]
) -> bool:
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE idioms
        SET
            idiom_en = ?,
            idiom_he = ?,
            translation_en = ?,
            translation_he = ?,
            half_en = ?,
            half_he = ?,
            off_en = ?,
            off_he = ?
        WHERE id = ?;
    """, (
        idiom_en, idiom_he,
        translation_en, translation_he,
        half_en, half_he,
        off_en, off_he,
        idiom_id
    ))

    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected > 0
