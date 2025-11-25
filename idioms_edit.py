# idioms_edit.py

import typer
import db

app = typer.Typer()

@app.command()
def edit(id: int, hebrew: str = None, english: str = None):
    conn = db.get_conn()
    c = conn.cursor()

    row = c.execute("SELECT * FROM idioms WHERE id=?", (id,)).fetchone()
    if not row:
        typer.echo("ID not found.")
        return

    new_hebrew = hebrew if hebrew else row["hebrew"]
    new_english = english if english else row["english"]

    c.execute("""
    UPDATE idioms
    SET hebrew = ?, english = ?
    WHERE id = ?
    """, (new_hebrew, new_english, id))

    conn.commit()
    conn.close()

    typer.echo("Updated successfully.")

if __name__ == "__main__":
    app()
