# ❓ FAQ – EasySQL Inventory Manager

### 1. Do I need to install external packages?
No. The application only uses the Python Standard Library.  
On Linux, you may need to install `python3-tk`:
```bash
sudo apt install python3-tk
```

---

### 2. Where is the database stored?
The file `inventory.db` is created automatically in the same folder as `app.py`.

---

### 3. How can I change the language?
Use the dropdown menu at the top right of the GUI to switch between **German (DE)** and **English (EN)**.

---

### 4. How can I back up my data?
Simply copy the `inventory.db` file.  
Alternatively, export to **CSV** or **JSON** via the Export buttons.

---

### 5. Can I run this on Windows, Linux, and macOS?
Yes. It is fully cross-platform.  
On Linux, install Tkinter manually if missing.

---

### 6. Can multiple people use it at the same time?
Not directly. The current version is designed for **local use** by a single user.  
For multi-user setups, consider a migration to PostgreSQL/MySQL and a web frontend.

---

### 7. What happens if my CSV uses commas instead of semicolons?
The importer automatically detects both `;` and `,` delimiters.  
Your data will be imported correctly.

---

### 8. What if I want additional languages?
You can extend the `LANG` dictionary inside `app.py`.  
Each label, button, and message must have translations for new language codes.
