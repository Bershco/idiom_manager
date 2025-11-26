import argparse
import db
import settings


def main():
    parser = argparse.ArgumentParser(description="Delete an idiom by ID.")
    parser.add_argument("--id", required=True, type=int)
    args = parser.parse_args()

    db_dir = settings.get_db_dir()
    if not db_dir:
        print("ERROR: DB path not set. Run GUI first.")
        return

    db.set_db_path(db_dir)
    db.init_db()

    if db.delete_idiom(args.id):
        print(f"Deleted idiom #{args.id}")
    else:
        print("Idiom not found.")


if __name__ == "__main__":
    main()
