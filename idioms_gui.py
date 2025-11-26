import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import db
import settings
import similarity
from util import normalize_text, required_fields_present, is_hebrew
from models import IdiomData
from export_csv import export_csv


# ---------------------------------------------------------
#   GUI CLASS
# ---------------------------------------------------------
class IdiomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Idiom Manager")
        self.root.geometry("1000x550")
        self.root.minsize(900, 500)

        # --------------------------
        #   THEME (Sun Valley local)
        # --------------------------
        style = ttk.Style(self.root)
        self.current_theme = "light"

        # Load themes from local directory
        theme_path = os.path.join(os.path.dirname(__file__), "themes")
        try:
            self.root.tk.call("source", os.path.join(theme_path, "sun-valley.tcl"))
            self.root.tk.call("source", os.path.join(theme_path, "sun-valley-dark.tcl"))
            style.theme_use("sun-valley")
            ttk.Style().theme_use("sun-valley-light")
            self.current_theme = "light"

        except:
            pass

        # --------------------------
        #   SETTINGS / DB PATH
        # --------------------------
        db_dir = settings.get_db_dir()
        if not db_dir:
            # Ask user to pick folder
            messagebox.showinfo("Choose Database Folder",
                                 "Pick the folder inside your Google Drive where idioms.db will be stored.")
            db_dir = filedialog.askdirectory(title="Select Google Drive folder")
            if not db_dir:
                messagebox.showerror("Error", "You must choose a folder to continue.")
                self.root.destroy()
                return
            settings.set_db_dir(db_dir)

        # Initialize DB
        db.set_db_path(db_dir)
        db.init_db()

        # --------------------------
        #   TOP FRAME (USERNAME)
        # --------------------------
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=20, pady=(10, 5))

        ttk.Label(top_frame, text="Username:", font=("Segoe UI", 11)).pack(side="left")
        self.username_entry = ttk.Entry(top_frame, width=30, font=("Segoe UI", 11))
        self.username_entry.pack(side="left", padx=10)
        self.username_entry.insert(0, settings.load_settings().get("last_username", ""))

        # Dark/Light toggle
        self.theme_button = ttk.Button(top_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side="right")

        # --------------------------
        #   MAIN INPUT AREA
        #   2 rows × 4 columns
        # --------------------------
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Row 1: English
        self.idiom_en = ttk.Entry(main_frame, font=("Segoe UI", 11))
        self.translation_en = ttk.Entry(main_frame, font=("Segoe UI", 11))
        self.half_en = ttk.Entry(main_frame, font=("Segoe UI", 11))
        self.off_en = ttk.Entry(main_frame, font=("Segoe UI", 11))

        # Row 2: Hebrew (RTL)
        self.idiom_he = ttk.Entry(main_frame, font=("Segoe UI", 11), justify="right")
        self.translation_he = ttk.Entry(main_frame, font=("Segoe UI", 11), justify="right")
        self.half_he = ttk.Entry(main_frame, font=("Segoe UI", 11), justify="right")
        self.off_he = ttk.Entry(main_frame, font=("Segoe UI", 11), justify="right")

        # Layout
        labels_row1 = ["Idiom (EN)*", "Translation (EN)*", "Half (EN)", "Off (EN)"]
        labels_row2 = ["Idiom (HE)*", "Translation (HE)*", "Half (HE)", "Off (HE)"]

        # Grid config
        for c in range(4):
            main_frame.columnconfigure(c, weight=1)

        # Put labels row1
        for c, txt in enumerate(labels_row1):
            ttk.Label(main_frame, text=txt).grid(row=0, column=c, sticky="w")

        self.idiom_en.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.translation_en.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.half_en.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        self.off_en.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Row 2
        for c, txt in enumerate(labels_row2):
            ttk.Label(main_frame, text=txt).grid(row=2, column=c, sticky="w")

        self.idiom_he.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.translation_he.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        self.half_he.grid(row=3, column=2, sticky="ew", padx=5, pady=5)
        self.off_he.grid(row=3, column=3, sticky="ew", padx=5, pady=5)

        # --------------------------
        #   ACTION BUTTONS
        # --------------------------
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=20)

        self.add_button = ttk.Button(btn_frame, text="Add Idiom", command=self.add_idiom)
        self.add_button.pack(side="left")

        self.export_button = ttk.Button(btn_frame, text="Export CSV", command=self.export_csv_file)
        self.export_button.pack(side="right")

        # --------------------------
        #   LOG OUTPUT
        # --------------------------
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        ttk.Label(log_frame, text="Status:").pack(anchor="w")

        self.log_box = tk.Text(log_frame, height=6, font=("Segoe UI", 10))
        self.log_box.pack(fill="both", expand=True)

        # Keyboard bindings
        self.root.bind("<Return>", self._enter_pressed)

        # Initial focus
        self.idiom_en.focus_set()

    # ---------------------------------------------------------
    #   THEME TOGGLE
    # ---------------------------------------------------------
    def toggle_theme(self):
        try:
            import tkinter.ttk as ttk
            style = ttk.Style()

            if self.current_theme == "light":
                style.theme_use("sun-valley-dark")
                self.current_theme = "dark"

                # Custom dark colors for widgets that ignore theme
                self.log_box.configure(
                    background="#1e1e1e",
                    foreground="#ffffff",
                    insertbackground="#ffffff"
                )
            else:
                style.theme_use("sun-valley")
                self.current_theme = "light"

                # Custom light colors for widgets that ignore theme
                self.log_box.configure(
                    background="#ffffff",
                    foreground="#000000",
                    insertbackground="#000000"
                )

        except Exception as e:
            print("Theme switching error:", e)


    # ---------------------------------------------------------
    #   ENTER KEY HANDLER
    # ---------------------------------------------------------
    def _enter_pressed(self, event):
        self.add_idiom()

    # ---------------------------------------------------------
    #   LOGGING
    # ---------------------------------------------------------
    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    # ---------------------------------------------------------
    #   EXPORT CSV
    # ---------------------------------------------------------
    def export_csv_file(self):
        try:
            path = export_csv()
            self.log(f"CSV exported to: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"CSV export failed:\n{e}")

    # ---------------------------------------------------------
    #   MAIN INSERT LOGIC
    # ---------------------------------------------------------
    def add_idiom(self):
        username = normalize_text(self.username_entry.get())
        if not username:
            messagebox.showerror("Error", "Username is required.")
            return

        # Save username persistently
        s = settings.load_settings()
        s["last_username"] = username
        settings.save_settings(s)

        data = IdiomData(
            created_by=username,

            idiom_en=self.idiom_en.get(),
            idiom_he=self.idiom_he.get(),

            translation_en=self.translation_en.get(),
            translation_he=self.translation_he.get(),

            half_en=self.half_en.get(),
            half_he=self.half_he.get(),

            off_en=self.off_en.get(),
            off_he=self.off_he.get(),
        )

        data.normalize()

        # Required fields
        if not required_fields_present(
            data.idiom_en, data.idiom_he, data.translation_en, data.translation_he
        ):
            messagebox.showerror("Missing fields", "English and Hebrew idiom + translations are required.")
            return

        # -------------------------
        #   SIMILARITY CHECK
        # -------------------------
        all_rows = {r["id"]: r for r in db.get_all_idioms()}

        match = similarity.find_best_match(
            idioms=all_rows,
            new_en=data.idiom_en,
            new_he=data.idiom_he
        )

        if match:
            idiom_id, score, lang = match
            existing = db.get_idiom(idiom_id)

            answer = messagebox.askyesno(
                "Possible Variant Detected",
                f"This idiom looks similar to:\n"
                f"EN: {existing['idiom_en']}\n"
                f"HE: {existing['idiom_he']}\n\n"
                f"Similarity: {round(score, 3)}\n\n"
                f"Is this a variant?"
            )

            if answer:
                # Insert row
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
                # Bidirectional linking
                db.add_variant_link(idiom_id, new_id)

                self.log(f"Added VARIANT #{new_id} linked to #{idiom_id}.")
                self._clear_fields()
                return

        # -------------------------
        #   NORMAL INSERT
        # -------------------------
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

        self.log(f"Added IDIOM #{new_id}: {data.idiom_en} | {data.idiom_he}")

        # User milestone
        count = db.count_user_idioms(username)
        if count % 10 == 0:
            self.log(f"🎉 {username}, you’ve added {count} idioms so far!")

        self._clear_fields()

    # ---------------------------------------------------------
    #   CLEAR INPUT FIELDS (NOT USERNAME)
    # ---------------------------------------------------------
    def _clear_fields(self):
        self.idiom_en.delete(0, "end")
        self.idiom_he.delete(0, "end")

        self.translation_en.delete(0, "end")
        self.translation_he.delete(0, "end")

        self.half_en.delete(0, "end")
        self.half_he.delete(0, "end")

        self.off_en.delete(0, "end")
        self.off_he.delete(0, "end")

        self.idiom_en.focus_set()


# ---------------------------------------------------------
#   ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = IdiomGUI(root)
    root.mainloop()
