# Idiom Manager (Hebrew ↔ English)

A lightweight Python application for collecting, managing, and sharing Hebrew↔English idioms across a small team.

Features both a **modern GUI** and a **simple CLI**, automatic language detection, similarity matching, variant management, and shared storage via **Google Drive Desktop** — no tokens, no APIs, no authentication logic.

---

# ✨ Features

### 🔤 Automatic Hebrew ↔ English Detection
Order does not matter — the system identifies which text is Hebrew and which is English.

### 🔍 Smart Similarity Recognition
Detects:
- Alternative idiom phrasings  
- English tense variants  
- Hebrew punctuation variants  
- Extremely close idiomatic matches  

Prompts for variant addition when needed.

### 📝 Variant Management
Each idiom can have multiple Hebrew variants and English variants, each properly linked to a single canonical idiom.

### 💾 Shared SQLite DB (via Google Drive Desktop)
- No server required  
- No API keys  
- No risk of data loss  
- All teammates automatically stay in sync  

### 🖥 Modern GUI
- Sun Valley modern theme (light + dark)
- Fully keyboard friendly (Tab + Enter)
- Accurate RTL Hebrew display
- CSV export
- Error-safe idiom validation

### 💻 CLI Tools
- Infinite input loop  
- Editing  
- Deletion  
- CSV export

---

# 📁 Project Structure

```
idiom_manager/
│
├── idioms_gui.py           # Main GUI app
├── idioms_loop.py          # CLI infinite input loop
├── idioms_edit.py          # Edit existing idioms
├── idioms_delete.py        # Delete idioms
├── export_csv.py           # CSV export tool
│
├── db.py                   # SQLite backend
├── models.py               # Data models
├── similarity.py           # Fuzzy matching logic
├── util.py                 # Language detection, helpers
│
├── requirements.txt
├── README.md
├── LICENSE
│
└── themes/
       sun-valley.tcl
       sun-valley-dark.tcl
```

---

# ☁️ Google Drive Desktop Sync

The idioms database (`idioms.db`) is stored in a **shared Google Drive folder** so all team members share the same database transparently.

Below are separate instructions for:

---

# 👑 **Setup for Project Manager (Roee)**

### **1. Install Google Drive Desktop**
Download:
https://www.google.com/drive/download/

Log in with your Google account.

### **2. Create a new folder for the idiom database**
Recommended name:

```
shared_idioms
```

### **3. Share the folder with your team**
Right-click the folder → **Share** → add their Gmail addresses.

Give them **Editor** permissions.

### **4. Locate the folder on your machine**

On Windows (default):
```
G:\My Drive\shared_idioms\
```

On macOS:
```
~/Library/CloudStorage/GoogleDrive-<your-email>/My Drive/shared_idioms/
```

### **5. Place your database here**
The app will automatically create the DB if it doesn’t yet exist.

You’re done.  
Your teammates now have a shared location to sync idioms.

---

# 👥 **Setup for Project Members (Teammates)**

### **1. Install Google Drive Desktop**
Download:
https://www.google.com/drive/download/

Sign in with the Google account that Roee invited.

### **2. Accept the shared folder**
You will receive an email + a Google Drive notification.

Once accepted, the folder will appear inside:

Windows:
```
G:\My Drive\shared_idioms\
```

macOS:
```
~/Library/CloudStorage/GoogleDrive-<your-email>/My Drive/shared_idioms/
```

### **3. Clone the project**
```
git clone <the repo URL>
cd idiom_manager
```

### **4. Create a virtual environment**

Windows:
```
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### **5. Install dependencies**
```
pip install -r requirements.txt
```

### **6. Launch the GUI**
```
python idioms_gui.py
```

The app will automatically detect the shared folder and use the synced database.

**No extra setup required.**

---

# ▶️ Running the App

### **GUI (recommended)**
```
python idioms_gui.py
```

Supports:
- Idiom insertion
- Auto-language detection
- Variant linking
- Similarity alerts
- Dark/light toggle
- CSV export
- Keyboard-only operation

### **CLI Input Loop**
```
python idioms_loop.py
```

Enter:
```
Hebrew | English
```

Exit with:
```
q, quit, exit, Ctrl+C, Ctrl+D
```

### **Edit an idiom**
```
python idioms_edit.py --id 12 --hebrew "..." --english "..."
```

### **Delete an idiom**
```
python idioms_delete.py --id 7
```

### **Export CSV**
```
python export_csv.py
```

---

# 🔧 Environment Variable Override (Optional)

To manually force the database directory:

Windows:
```
setx IDIOM_DB_DIR "D:\SomePath"
```

macOS/Linux:
```
export IDIOM_DB_DIR="/path/to/dir"
```

---

# 🤝 Team Usage Notes

- All team members must keep Google Drive running  
- Concurrent reads are safe  
- Concurrent writes are rare and SQLite handles them well  
- Ideal for collaborative annotation or idiom collection  

---

# 📄 License

This project is licensed under the **MIT License**.  
See `LICENSE` for details.

---

# 🙋 Support

For issues or contributions, please open a GitHub issue or pull request.
