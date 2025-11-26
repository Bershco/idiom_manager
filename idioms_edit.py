import argparse
import db
import settings
from util import normalize_text


def main():
    parser = argparse.ArgumentParser(description="Edit an idiom by ID.")
    parser.add_argument("--id", required=True, type=int, help="ID of idiom to edit")

    parser.add_argument("--idiom_en")
    parser.add_argument("--idiom_he")
    parser.add_argument("--translation_en")
    parser.add_argument("--translation_he")
    parser.add_argument("--half_en")
    parser.add_argument("--half_he")
    parser.add_argument("--off_en")
    parser.add_argument("--off_he")

    args = parser.parse_args()

    db_dir = settings.get_db_dir()
    if not db_dir:
        print("ERROR: DB path not set. Run GUI once to choose folder.")
        return

    db.set_db_path(db_dir)
    db.init_db()

    row = db.get_idiom(args.id)
    if not row:
        print("ERROR: Idiom not found.")
        return

    updated = db.update_idiom(
        args.id,
        idiom_en=normalize_text(args.idiom_en or row["idiom_en"]),
        idiom_he=normalize_text(args.idiom_he or row["idiom_he"]),
        translation_en=normalize_text(args.translation_en or row["translation_en"]),
        translation_he=normalize_text(args.translation_he or row["translation_he"]),
        half_en=normalize_text(args.half_en or row["half_en"]),
        half_he=normalize_text(args.half_he or row["half_he"]),
        off_en=normalize_text(args.off_en or row["off_en"]),
        off_he=normalize_text(args.off_he or row["off_he"]),
    )

    if updated:
        print(f"Updated idiom #{args.id}")
    else:
        print("No changes applied.")


if __name__ == "__main__":
    main()
