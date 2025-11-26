import csv
from pathlib import Path
import db
from settings import get_db_dir


def export_csv():
    """
    Export idioms into <db_dir>/idioms.csv with UTF-8 BOM.
    Includes variants (comma-separated list).
    """

    db_dir = get_db_dir()
    if not db_dir:
        raise RuntimeError("DB directory is not set. Please choose folder in the GUI first.")

    csv_path = Path(db_dir) / "idioms.csv"

    # Fetch idioms
    idioms = db.get_all_idioms()

    # Prepare CSV
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "id",
            "created_by",
            "created_at",
            "idiom_en",
            "idiom_he",
            "translation_en",
            "translation_he",
            "half_en",
            "half_he",
            "off_en",
            "off_he",
            "variants"
        ])

        # Rows
        for row in idioms:
            vid_list = db.get_variants(row["id"])
            vid_csv = ",".join(str(v) for v in vid_list)

            writer.writerow([
                row["id"],
                row["created_by"],
                row["created_at"],
                row["idiom_en"],
                row["idiom_he"],
                row["translation_en"],
                row["translation_he"],
                row.get("half_en", "") or "",
                row.get("half_he", "") or "",
                row.get("off_en", "") or "",
                row.get("off_he", "") or "",
                vid_csv
            ])

    return str(csv_path)
