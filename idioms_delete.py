# idioms_delete.py

import typer
import db

app = typer.Typer()

@app.command()
def delete(id: int):
    conn = db.get_conn()
    c = conn.cursor()

    row = c.execute("SELECT * FROM idioms WHERE id=?", (id,)).fetchone()
    if not row:
        typer.echo("ID not found.")
        return

    confirm = typer.confirm(f"Delete idiom '{row['hebrew']} | {row['english']}'?")
    if not confirm:
        typer.echo("Cancelled.")
        return

    c.execute("DELETE FROM idioms WHERE id=?", (id,))
    conn.commit()
    conn.close()
    typer.echo("Deleted successfully.")

if __name__ == "__main__":
    app()
