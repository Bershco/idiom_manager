# Idiom Manager (Hebrew ↔ English)

A lightweight collaborative tool for collecting, validating, and managing Hebrew ↔ English idiom pairs.  
Built for research teams who need a shared database synced through **Google Drive Desktop**, with a simple GUI, variant detection, CSV export, and per-user metric tracking.

This tool requires **no internet APIs**, no authentication tokens, and no database server.  
Everything runs locally and synchronizes automatically through Google Drive Desktop.

---

# ✨ Features

### 🖥 Modern GUI Application
- Two-row layout: English row + Hebrew row  
- 4 required fields (idiom + translation for EN & HE)  
- 4 optional fields (half & off idioms)  
- Username box (saved locally, persistent)  
- Add idiom via Enter key or button  
- Built-in log console  
- Dark/Light theme toggle  
- Fully keyboard operable (Tab to cycle, Enter to submit)

### 🔎 Smart Variant Detection
- English idioms only compared with English  
- Hebrew idioms only compared with Hebrew  
- Levenshtein-based similarity scoring  
- Asks user if match is a true variant  
- Variants stored via **bidirectional link table**  
- CSV export includes variant mappings

### 💾 Shared Google Drive Database
- Database stored in a **shared Google Drive folder**  
- Every team member operates on the same idioms.db  
- settings.json is local and never synced  
- No DB conflicts, no manual merging needed

### 📤 CSV Export
- Exports to `<chosen_db_folder>/idioms.csv`  
- UTF-8 with BOM (Excel and Google Sheets safe)  
- Includes all idiom fields with variant mappings  
- 100% correct Hebrew (no mojibake)

### 🧵 Optional CLI Mode
- Infinite loop idiom entry  
- Same logic as GUI  
- Variant detection  
- Username tracking  
- Quit with q/quit/exit or Ctrl+C  

---

# 📁 Project Structure

```
idiom_manager/
├── db.py
├── idioms_gui.py
├── idioms_loop.py
├── idioms_edit.py
├── idioms_delete.py
├── export_csv.py
├── similarity.py
├── util.py
├── settings.py
├── models.py
├── settings.json         # Local only
├── README.md
├── LICENSE
├── requirements.txt
└── themes/
      sun-valley.tcl
      sun-valley-dark.tcl
```

---

# 👑 Setup — Project Manager

### 1. Install Google Drive Desktop  
https://www.google.com/drive/download/

### 2. Create the shared folder  
Example: `shared_idioms`

### 3. Share it with your team  
Give everyone **Editor** permissions.

### 4. Clone the project  
```
git clone <repo-url>
cd idiom_manager
```

### 5. Install dependencies (Windows)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Install dependencies (macOS/Linux)
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Run GUI once
```
python idioms_gui.py
```

Choose the shared Google Drive folder.  
This creates `<shared_folder>/idioms.db` and local `settings.json`.

---

# 👥 Setup — Team Members

### 1. Install Google Drive Desktop  
### 2. Accept shared folder  
### 3. Clone repo  
### 4. Install dependencies  
### 5. Run GUI:
```
python idioms_gui.py
```

Select your local path to shared folder (e.g. `G:\My Drive\shared_idioms`).

---

# ▶️ Running the GUI

```
python idioms_gui.py
```

Features:
- Username (persistent)  
- Required + optional idiom fields  
- Enter to submit  
- Variant linking  
- Dark/light toggle  
- CSV export  
- Per-user milestones (every 10 idioms)

---

# 🧵 CLI (Optional)

```
python idioms_loop.py
```

---

# ✏ Editing Idioms

```
python idioms_edit.py --id 12 --idiom_en "Break the ice"
```

# 🗑 Deleting Idioms

```
python idioms_delete.py --id 12
```

---

# 📤 Export CSV

```
python export_csv.py
```

Creates `<db_dir>/idioms.csv` (UTF-8 BOM).

---

# 🔗 Database Schema

Tables: idioms, variants_link  
(Fields detailed above)

---

# 🛟 Troubleshooting

- If Hebrew appears corrupted → Excel Import → UTF-8  
- If GUI asks for DB every run → ensure settings.json writable  
- If DB empty for teammate → wrong folder selected  

---

# 📄 License

MIT License included in repository.

---

# 🙌 Contributions

PRs and suggestions welcome.
