# 🛠️ Troubleshooting – EasySQL Inventory Manager

### ❌ Problem: `ModuleNotFoundError: No module named 'tkinter'`
**Solution:**  
On Linux, install Tkinter:
```bash
sudo apt install python3-tk
```
On Windows/macOS, reinstall Python from [python.org](https://www.python.org/) and ensure Tkinter is included.

---

### ❌ Problem: Application window does not open
- Ensure you are running **Python 3.10 or newer**.  
- Run with:
```bash
python app.py
```

---

### ❌ Problem: Database errors (`sqlite3.OperationalError`)
**Solution:**  
The database file `inventory.db` may be corrupted.  
Close the application, back up the file, then delete it. A new one will be created automatically.

---

### ❌ Problem: Export/Import issues with CSV
- Ensure your CSV uses UTF-8 encoding.  
- Supported delimiters: `;` and `,`.  
- If your system uses Excel, save CSV as **UTF-8 with delimiter ;**.

---

### ❌ Problem: GUI text not fully translated
**Solution:**  
All translations are stored in the `LANG` dictionary inside `app.py`.  
Add missing entries or extend the dictionary for new languages.

---

### ❌ Problem: Low-stock highlighting not working
- Verify that you set a **Min.-Qty** value > 0.  
- Only items with `qty < min_qty` are highlighted red.
