import db
import settings
import similarity
from util import normalize_text, required_fields_present
from models import IdiomData


def cli_prompt(prompt: str) -> str:
    s = input(prompt).strip()
    return normalize_text(s)


def main():
    # Ensure DB is ready
    db_dir = settings.get_db_dir()
    if not db_dir:
        print("ERROR: No DB folder chosen. Run the GUI once to set DB path.")
        return

    db.set_db_path(db_dir)
    db.init_db()

    print("=== Idiom Manager CLI ===")
    print("Enter 'q' or Ctrl+C to quit.\n")

    username = cli_prompt("Enter your username: ")
    if not username:
        print("Username required. Exiting.")
        return

    print("\nWelcome,", username)
    print("Start entering idioms.\n")

    while True:
        try:
            print("\n--- New Idiom ---")
            idiom_en = cli_prompt("Idiom (English): ")
            if idiom_en.lower() in ("q", "quit", "exit"):
                break

            idiom_he = cli_prompt("Idiom (Hebrew): ")
            if idiom_he.lower() in ("q", "quit", "exit"):
                break

            translation_en = cli_prompt("Translation (EN): ")
            translation_he = cli_prompt("Translation (HE): ")

            half_en = cli_prompt("Half (EN) [optional]: ")
            half_he = cli_prompt("Half (HE) [optional]: ")

            off_en = cli_prompt("Off (EN) [optional]: ")
            off_he = cli_prompt("Off (HE) [optional]: ")

            # Required fields check
            if not required_fields_present(idiom_en, idiom_he, translation_en, translation_he):
                print("❌ Missing required fields: idiom + translation in both languages.")
                continue

            data = IdiomData(
                created_by=username,
                idiom_en=idiom_en,
                idiom_he=idiom_he,
                translation_en=translation_en,
                translation_he=translation_he,
                half_en=half_en,
                half_he=half_he,
                off_en=off_en,
                off_he=off_he,
            )
            data.normalize()

            # Variant detection
            all_rows = {r["id"]: r for r in db.get_all_idioms()}
            match = similarity.find_best_match(all_rows, data.idiom_en, data.idiom_he)

            if match:
                idiom_id, score, lang = match
                row = db.get_idiom(idiom_id)

                print("\nPossible variant found:")
                print(f"  EN: {row['idiom_en']}")
                print(f"  HE: {row['idiom_he']}")
                print(f"  Similarity: {round(score,3)}")
                ans = cli_prompt("Is this a variant? (y/n): ").lower()

                if ans.startswith("y"):
                    new_id = db.add_idiom(
                        created_by=data.created_by,
                        idiom_en=data.idiom_en,
                        idiom_he=data.idiom_he,
                        translation_en=data.translation_en,
                        translation_he=data.translation_he,
                        half_en=data.half_en,
                        half_he=data.half_he,
                        off_en=data.off_en,
                        off_he=data.off_he,
                    )
                    db.add_variant_link(idiom_id, new_id)
                    print(f"✅ Added VARIANT #{new_id} linked to #{idiom_id}")
                    continue

            # Normal insert
            new_id = db.add_idiom(
                created_by=username,
                idiom_en=data.idiom_en,
                idiom_he=data.idiom_he,
                translation_en=data.translation_en,
                translation_he=data.translation_he,
                half_en=data.half_en,
                half_he=data.half_he,
                off_en=data.off_en,
                off_he=data.off_he,
            )
            print(f"✅ Added IDIOM #{new_id}")

            count = db.count_user_idioms(username)
            if count % 10 == 0:
                print(f"🎉 {username}, you’ve added {count} idioms so far!")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print("❌ ERROR:", e)


if __name__ == "__main__":
    main()
