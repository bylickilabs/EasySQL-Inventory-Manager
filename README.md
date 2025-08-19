# EasySQL Inventory Manager

A lightweight, local inventory management application built with Python, Tkinter, and SQLite.  
**Features**: CRUD operations, multilingual support (DE/EN), CSV/JSON import & export, low-stock alerts, and search & sorting.

---

## ✨ Features
- 🗃️ **SQLite Database** – no external dependencies
- 🌐 **Language Switch (DE/EN)**
- 📉 **Low-stock alerts** (minimum quantity with red highlight)
- 🔎 **Search & sort** by any column
- 📤 **Export** to CSV & JSON
- 📥 **Import** from CSV (`,` or `;` delimiters)
- 💻 **Cross-platform** (Windows, Linux, macOS)

---

## 🚀 Quickstart

```bash
git clone https://github.com/bylickilabs/easysql-inventory-manager
cd easysql-inventory-manager
python app.py
```

The SQLite database (`inventory.db`) is created automatically in the same folder.

---

## 📖 Usage
- Add, edit, delete, and search items
- Set **minimum quantity** → items below threshold are highlighted
- Use the **Low-stock only** filter to show critical items
- Import/Export your inventory with CSV or JSON
- Switch language via dropdown (top-right)

---

## 📚 Documentation
- [USAGE.md](USAGE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
- [SUPPORT.md](SUPPORT.md)

---

## 📊 Advantages & Disadvantages

| Category | Advantages | Disadvantages |
|----------|-------------|---------------|
| Setup | Instant start, local | Not web-based |
| Cost | Free, open-source | No enterprise SLA |
| Database | SQLite (no server needed) | Limited for very large datasets |
| Features | CRUD, low-stock alerts, search, CSV/JSON | No HR/CRM/Finance modules |
| Integration | CSV/JSON compatibility | Advanced API requires customization |

---

## 👨‍💻 Author
Developed with ❤️ by **Thorsten Bylicki · BYLICKILABS**
