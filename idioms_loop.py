import typer
import db
from util import detect_languages, is_hebrew
from similarity import find_similar

EXIT_WORDS = {"q", "quit", "exit", "out"}


def start_loop():
    db.init_db()  # Ensure DB schema exists
    typer.echo("=== Idiom Manager (Interactive Mode) ===")
    typer.echo("Enter idioms using the format:")
    typer.echo("    Hebrew | English")
    typer.echo("Type 'quit' or press Ctrl+C to exit.")
    typer.echo("")

    while True:
        try:
            line = input(">>> ").strip()

        except (KeyboardInterrupt, EOFError):
            typer.echo("\nExiting.")
            break

        # Exit words
        if line.lower() in EXIT_WORDS:
            typer.echo("Goodbye!")
            break

        # Must contain delimiter
        if "|" not in line:
            typer.echo("[ERROR] Use format: hebrew | english")
            continue

        left, right = (s.strip() for s in line.split("|", 1))

        # Language detection
        try:
            hebrew, english = detect_languages(left, right)
        except ValueError as e:
            typer.echo(f"[ERROR] {e}")
            continue

        # Duplicate exact match?
        if db.find_exact_match(hebrew, english):
            typer.echo("[ERROR] This exact Hebrew-English pair already exists.")
            continue

        # Hebrew already exists?
        if db.find_by_hebrew(hebrew):
            typer.echo("[ERROR] This Hebrew idiom already exists.")
            continue

        # English already exists?
        if db.find_by_english(english):
            typer.echo("[ERROR] This English idiom already exists.")
            continue

        # Similarity detection
        similar = find_similar(hebrew, english)

        if similar:
            typer.echo("\nPossible similar idioms found:\n")

            for entry in similar:
                row = entry["row"]
                typer.echo(
                    f"- Hebrew:  {row['hebrew']}  (score {entry['score_he']})\n"
                    f"  English: {row['english']}  (score {entry['score_en']})\n"
                )

            same = input("Is this the same idiom / variant? (y/n): ").lower().strip()

            if same == "y":
                # Identify which side is the variant
                # If user typed a new Hebrew variant
                if is_hebrew(left):
                    lang = "he"
                    variant_text = left
                # If user typed a new English variant
                else:
                    lang = "en"
                    variant_text = right

                # Link to first matched idiom
                row = similar[0]["row"]
                db.insert_variant(row["id"], variant_text, lang)
                typer.echo("Stored as a variant.\n")
                continue

        # Insert new idiom pair
        db.insert_idiom(hebrew, english)
        typer.echo("Idiom added successfully.\n")


if __name__ == "__main__":
    start_loop()
