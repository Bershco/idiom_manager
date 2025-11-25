# idioms_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import db
from util import detect_languages, is_hebrew
from similarity import find_similar

RTL = "\u200F"


def force_rtl(text: str):
    """Wrap with RTL markers for correct Hebrew display."""
    return RTL + text + RTL


class IdiomGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Idiom Manager")
        self.root.geometry("640x520")
        self.root.minsize(580, 480)

        db.init_db()

        # Load themes
        theme_path = os.path.join(os.path.dirname(__file__), "themes")

        self.root.tk.call("source", os.path.join(theme_path, "sun-valley.tcl"))
        self.root.tk.call("source", os.path.join(theme_path, "sun-valley-dark.tcl"))

        # Default theme
        ttk.Style().theme_use("sun-valley")

        # --- Main Frame ---
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        # --- Input boxes (symmetric, no labels) ---
        self.entry1 = tk.Entry(self.main_frame, font=("Segoe UI", 13), justify="center", relief="solid", bd=1)
        self.entry2 = tk.Entry(self.main_frame, font=("Segoe UI", 13), justify="center", relief="solid", bd=1)
        self.entry1.pack(pady=10, fill="x")
        self.entry2.pack(pady=10, fill="x")

        # Bind shortcut keys
        self._bind_shortcuts(self.entry1)
        self._bind_shortcuts(self.entry2)

        # --- Button Row ---
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        self.add_btn = ttk.Button(btn_frame, text="Add Idiom", command=self.add_idiom)
        self.export_btn = ttk.Button(btn_frame, text="Export CSV", command=self.export_csv)
        self.theme_btn = ttk.Button(btn_frame, text="Dark Mode", command=self.toggle_theme)

        self.add_btn.grid(row=0, column=0, padx=8)
        self.export_btn.grid(row=0, column=1, padx=8)
        self.theme_btn.grid(row=0, column=2, padx=8)

        # --- Status Log ---
        self.status = scrolledtext.ScrolledText(
            self.main_frame, height=12, width=68, font=("Segoe UI", 11)
        )
        self.status.pack(pady=15, fill="both", expand=True)
        self.status.config(state="disabled")

        # Save current theme
        self.current_theme = "light"

    # ---------------------------------------------------------
    # Keyboard shortcuts
    # ---------------------------------------------------------
    def _bind_shortcuts(self, widget):

        widget.bind("<Control-a>", lambda e: self._select_all(widget))
        widget.bind("<Control-A>", lambda e: self._select_all(widget))

        widget.bind("<Control-BackSpace>", lambda e: self._delete_prev_word(widget))
        widget.bind("<Control-Delete>", lambda e: self._delete_next_word(widget))

    def _select_all(self, widget):
        widget.select_range(0, "end")
        widget.icursor("end")
        return "break"

    def _delete_prev_word(self, widget):
        pos = widget.index("insert")
        text = widget.get()

        cut_pos = text.rfind(" ", 0, pos - 1)
        if cut_pos == -1:
            widget.delete(0, pos)
        else:
            widget.delete(cut_pos + 1, pos)
        return "break"

    def _delete_next_word(self, widget):
        pos = widget.index("insert")
        text = widget.get()

        cut_pos = text.find(" ", pos)
        if cut_pos == -1:
            widget.delete(pos, "end")
        else:
            widget.delete(pos, cut_pos)
        return "break"

    # ---------------------------------------------------------
    # Theme switching
    # ---------------------------------------------------------
    def toggle_theme(self):
        if self.current_theme == "light":
            ttk.Style().theme_use("sun-valley-dark")
            self.current_theme = "dark"
            self.theme_btn.config(text="Light Mode")

            self.status.config(bg="#111111", fg="#FFFFFF", insertbackground="#FFFFFF")
            self.entry1.config(background="#2A2A2A", foreground="#FFFFFF", insertbackground="#FFFFFF")
            self.entry2.config(background="#2A2A2A", foreground="#FFFFFF", insertbackground="#FFFFFF")

        else:
            ttk.Style().theme_use("sun-valley")
            self.current_theme = "light"
            self.theme_btn.config(text="Dark Mode")

            self.status.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            self.entry1.config(background="#FFFFFF", foreground="#000000", insertbackground="#000000")
            self.entry2.config(background="#FFFFFF", foreground="#000000", insertbackground="#000000")


    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------
    def log(self, msg):
        self.status.config(state="normal")
        self.status.insert("end", msg + "\n")
        self.status.config(state="disabled")
        self.status.see("end")

    # ---------------------------------------------------------
    # Export CSV
    # ---------------------------------------------------------
    def export_csv(self):
        import export_csv
        path = r"G:\My Drive\shared_idioms\idioms_export.csv"
        export_csv.export(path)
        messagebox.showinfo("Export CSV", f"Exported to:\n{path}")

    # ---------------------------------------------------------
    # Add idiom
    # ---------------------------------------------------------
    def add_idiom(self):
        text1 = self.entry1.get().strip()
        text2 = self.entry2.get().strip()

        if not text1 or not text2:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Preserve display formatting
        t1_disp = force_rtl(text1) if is_hebrew(text1) else text1
        t2_disp = force_rtl(text2) if is_hebrew(text2) else text2

        # Proper identification
        try:
            heb, eng = detect_languages(text1, text2)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Duplicate checks
        if db.find_exact_match(heb, eng):
            messagebox.showerror("Error", "This idiom already exists.")
            return

        if db.find_by_hebrew(heb):
            messagebox.showerror("Error", "Hebrew idiom already exists.")
            return

        if db.find_by_english(eng):
            messagebox.showerror("Error", "English idiom already exists.")
            return

        # Similarity
        matches = find_similar(heb, eng)
        if matches:
            row = matches[0]["row"]
            text = (
                "A similar idiom exists:\n\n"
                f"Hebrew:  {row['hebrew']}\n"
                f"English: {row['english']}\n\n"
                "Is this a variant?"
            )
            if messagebox.askyesno("Similar Found", text):
                # Determine which side is the variant
                if heb != row["hebrew"]:
                    # New Hebrew variant
                    variant_text = heb
                    lang = "he"
                elif eng != row["english"]:
                    # New English variant
                    variant_text = eng
                    lang = "en"
                else:
                    messagebox.showerror("Error", "Variant detection failed.")
                    return

                db.insert_variant(row["id"], variant_text, lang)
                self.log(f"Added {lang.upper()} variant: {variant_text}")

                # Clear the text boxes after adding variant
                self.entry1.delete(0, tk.END)
                self.entry2.delete(0, tk.END)

                return

        # Insert idiom
        db.insert_idiom(heb, eng)
        self.log(f"Added successfully:\n{t1_disp} | {t2_disp}")

        # Clear fields
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = IdiomGUI(root)
    root.mainloop()
