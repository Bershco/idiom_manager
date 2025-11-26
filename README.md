
# Idiom Manager (Hebrew ↔ English)

A lightweight, Python-based CLI tool for collecting, managing, and sharing Hebrew–English idiom pairs within a team.  
Designed for accuracy, multi-user collaboration, persistent storage, and long-term maintainability.

This tool automatically detects Hebrew/English, prevents duplicates, identifies similar idioms using fuzzy matching, stores variants, and syncs the database across team members using Google Drive Desktop.

---

## Features

### Idiom Pair Storage
- Store Hebrew ↔ English idiom pairs
- Order-independent (languages detected automatically)
- Rejects duplicates on either side
- Supports persistent storage via SQLite

### Language & Unicode Support
- Hebrew detection using Unicode range matching
- English detection fallback logic
- Full UTF-8 database storage

### Variants
- Supports **both Hebrew and English variants**
- Useful for:
  - Alternate spellings
  - Verb tense differences (e.g., “bite” vs “bit”)
  - Slight idiom reformulations
- Variants are linked to a canonical idiom entry

### Similarity Detection
- Uses `rapidfuzz` for fast Levenshtein fuzzy matching
- Warns user about similar idioms
- Option to store input as a variant instead of a new idiom

### CLI Interaction
- Infinite interactive loop
- Idioms entered using: `Hebrew | English`
- Exit via:
  - `quit`, `exit`, `out`, `q`
  - or Ctrl+C / Ctrl+D
- All operations are local and fast

### Multi-User Collaboration
- Database stored in a **shared Google Drive folder**
- All changes automatically sync to teammates' machines
- No Google API keys or tokens required

### Tools Included
- Interactive input loop
- Edit CLI
- Delete CLI
- CSV Export CLI (with variant separation)
- Database auto-detection
- SQLite-based persistence

---

## Requirements

### Python
- Python 3.9 or higher  
- Works on Windows, macOS, and Linux

### Python Dependencies
Installed via:

```
pip install -r requirements.txt
```

Libraries used:
- `typer` — CLI framework
- `rapidfuzz` — similarity matching
- `sqlite3` — built-in SQLite engine

### Google Drive Desktop (Required for multi-user sync)
The database is stored in a folder such as:

```
G:\My Drive\shared_idioms\
```

Google Drive Desktop automatically syncs this folder across all team members.

#### Windows:
- Google Drive Desktop mounts as a virtual disk (commonly `G:`)
- “My Drive” folder appears at:
  ```
  G:\My Drive\
  ```

#### macOS:
- Google Drive appears at:
  ```
  ~/Google Drive/
  ```
  or:
  ```
  ~/My Drive/
  ```

#### Linux:
Google Drive Desktop is not available.  
Use one of:
- `insync`
- `rclone + mount`
- `google-drive-ocamlfuse`

Or store the DB in a shared network folder.

---

## Database Location

By default, the tool automatically searches for common Google Drive Desktop locations:

1. `G:\My Drive\shared_idioms\idioms.db`  
2. `G:\Google Drive\shared_idioms\idioms.db`  
3. `~/Google Drive/shared_idioms/idioms.db`  
4. `~/My Drive/shared_idioms/idioms.db`  
5. Fallback: `~/shared_idioms/idioms.db`

### Override Database Location (Optional)

Set an environment variable:

#### Windows:
```
setx IDIOM_DB_DIR "D:\SomeFolder\idioms"
```

#### macOS/Linux:
```
export IDIOM_DB_DIR="/path/to/folder"
```

The database will be stored at:
```
<IDIOM_DB_DIR>/idioms.db
```

---

## Installation

### 1. Clone the repository
```
git clone https://github.com/<yourname>/idiom_manager.git
cd idiom_manager
```

### 2. Create a virtual environment

#### Windows:
```
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

## Usage

### Interactive Input Loop
Enter idioms continuously:
```
python idioms_loop.py
```

Format:
```
Hebrew | English
```

Exit:
- `quit`, `exit`, `q`, `out`
- Ctrl+C / Ctrl+D

### Editing Entries
```
python idioms_edit.py --id <id> --hebrew "..." --english "..."
```

### Deleting Entries
```
python idioms_delete.py --id <id>
```

### Export to CSV
```
python export_csv.py
```

CSV contains:
- Hebrew idiom
- English idiom
- Hebrew variants
- English variants
- Creation timestamp

---

## Project Structure

```
idioms_loop.py        - Interactive idiom input CLI
idioms_edit.py        - Edit existing idioms
idioms_delete.py      - Delete idioms
export_csv.py         - Export database to CSV

db.py                 - SQLite database logic
similarity.py         - Levenshtein similarity logic
util.py               - Hebrew/English detection helpers
requirements.txt      - Python dependencies
README.md             - Documentation
```

---

## Notes for Team Use

- All team members must sync the same Google Drive folder  
- SQLite handles multi-user reads well  
- Writes may conflict if two users modify DB simultaneously  
- Hebrew display direction may vary depending on terminal  
- Database grows safely and remains ACID-compliant  

---

## License

Choose a license (MIT recommended).

---

## Contact

For questions or suggestions, open an issue or pull request.
