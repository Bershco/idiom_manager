# export_csv.py

import csv
import typer
import db

app = typer.Typer()
DEFAULT_CSV_PATH = r"G:\My Drive\shared_idioms\idioms_export.csv"

@app.command()
def export(path: str = DEFAULT_CSV_PATH):
    rows = db.fetch_all_idioms()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id",
            "hebrew",
            "english",
            "hebrew_variants",
            "english_variants",
            "created_at"
        ])

        for r in rows:
            writer.writerow([
                r["id"],
                r["hebrew"],
                r["english"],
                r["hebrew_variants"] or "",
                r["english_variants"] or "",
                r["created_at"]
            ])

    typer.echo(f"Exported {len(rows)} idioms to '{path}'.")
