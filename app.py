import os
import csv
import json
import sqlite3
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser

# ------------------- App Meta -------------------
APP_NAME = "EasySQL Inventory Manager"
APP_VERSION = "1.0.0"
APP_AUTHOR = "©Thorsten Bylicki | ©BYLICKILABS"

GITHUB_URL = "https://github.com/bylickilabs"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "inventory.db")


# ------------------- Localization -------------------
LANG = {
    "de": {
        "title": f"{APP_NAME} v{APP_VERSION} - {APP_AUTHOR}",
        "tab_inventory": "Inventar",
        "group_form": "Artikel-Details",
        "lbl_name": "Name",
        "lbl_sku": "SKU",
        "lbl_location": "Lagerort",
        "lbl_qty": "Menge",
        "lbl_minqty": "Min.-Menge (Alert)",
        "lbl_notes": "Notizen",
        "btn_new": "Neu",
        "btn_save": "Speichern",
        "btn_update": "Aktualisieren",
        "btn_delete": "Löschen",
        "btn_clear": "Felder leeren",
        "search": "Suche",
        "placeholder_search": "Name, SKU, Lagerort …",
        "btn_export_csv": "Export CSV",
        "btn_export_json": "Export JSON",
        "btn_import_csv": "Import CSV",
        "chk_low_only": "Nur Niedrigbestand",
        "col_id": "ID",
        "col_name": "Name",
        "col_sku": "SKU",
        "col_location": "Lagerort",
        "col_qty": "Menge",
        "col_minqty": "Min.-Menge",
        "col_notes": "Notizen",
        "col_created": "Erstellt",
        "col_updated": "Aktualisiert",
        "btn_info": "Info",
        "btn_github": "GitHub",
        "menu_lang": "Sprache",
        "lang_de": "Deutsch",
        "lang_en": "Englisch",
        "confirm_delete": "Diesen Datensatz wirklich löschen?",
        "import_done": "Import abgeschlossen.",
        "export_done": "Export abgeschlossen.",
        "no_selection": "Bitte zuerst einen Datensatz auswählen.",
        "invalid_qty": "Bitte eine gültige Menge (Ganzzahl) eingeben.",
        "invalid_minqty": "Bitte eine gültige Min.-Menge (Ganzzahl) eingeben.",
        "required_fields": "Bitte mindestens Name oder SKU ausfüllen.",
        "status_ready": "Bereit.",
        "status_saved": "Gespeichert.",
        "status_updated": "Aktualisiert.",
        "status_deleted": "Gelöscht.",
        "status_imported": "Importiert.",
        "status_exported": "Exportiert.",
        "info_text": f"{APP_NAME}\n\nSQLite-basiertes Inventar mit Low-Stock-Alerts, Suche, Sortierung, CSV/JSON Export & CSV Import.\nBYLICKILABS · Thorsten Bylicki",
        "dialog_export_csv_title": "Als CSV exportieren",
        "dialog_export_json_title": "Als JSON exportieren",
        "dialog_import_csv_title": "CSV-Datei importieren",
        "dialog_confirm": "Bestätigen",
    },
    "en": {
        "title": f"{APP_NAME} v{APP_VERSION} - {APP_AUTHOR}",
        "tab_inventory": "Inventory",
        "group_form": "Item Details",
        "lbl_name": "Name",
        "lbl_sku": "SKU",
        "lbl_location": "Location",
        "lbl_qty": "Quantity",
        "lbl_minqty": "Min. Qty (Alert)",
        "lbl_notes": "Notes",
        "btn_new": "New",
        "btn_save": "Save",
        "btn_update": "Update",
        "btn_delete": "Delete",
        "btn_clear": "Clear Fields",
        "search": "Search",
        "placeholder_search": "Name, SKU, Location …",
        "btn_export_csv": "Export CSV",
        "btn_export_json": "Export JSON",
        "btn_import_csv": "Import CSV",
        "chk_low_only": "Low-stock only",
        "col_id": "ID",
        "col_name": "Name",
        "col_sku": "SKU",
        "col_location": "Location",
        "col_qty": "Qty",
        "col_minqty": "Min. Qty",
        "col_notes": "Notes",
        "col_created": "Created",
        "col_updated": "Updated",
        "btn_info": "Info",
        "btn_github": "GitHub",
        "menu_lang": "Language",
        "lang_de": "German",
        "lang_en": "English",
        "confirm_delete": "Really delete this record?",
        "import_done": "Import completed.",
        "export_done": "Export completed.",
        "no_selection": "Please select a record first.",
        "invalid_qty": "Please enter a valid quantity (integer).",
        "invalid_minqty": "Please enter a valid minimum quantity (integer).",
        "required_fields": "Please fill at least Name or SKU.",
        "status_ready": "Ready.",
        "status_saved": "Saved.",
        "status_updated": "Updated.",
        "status_deleted": "Deleted.",
        "status_imported": "Imported.",
        "status_exported": "Exported.",
        "info_text": f"{APP_NAME}\n\nSQLite-based inventory with low-stock alerts, search, sort, CSV/JSON export & CSV import.\nBYLICKILABS · Thorsten Bylicki",
        "dialog_export_csv_title": "Export as CSV",
        "dialog_export_json_title": "Export as JSON",
        "dialog_import_csv_title": "Import CSV File",
        "dialog_confirm": "Confirm",
    }
}


# ------------------- EasySQL Wrapper -------------------
class EasySQL:
    def __init__(self, db_path: str):
        self.path = db_path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            sku TEXT,
            location TEXT,
            qty INTEGER DEFAULT 0,
            min_qty INTEGER DEFAULT 0,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)
        cols = {r["name"] for r in self.query("PRAGMA table_info(items)")}
        if "min_qty" not in cols:
            self.execute("ALTER TABLE items ADD COLUMN min_qty INTEGER DEFAULT 0")
            
        self.execute("CREATE INDEX IF NOT EXISTS idx_items_sku ON items(sku)")
        self.execute("CREATE INDEX IF NOT EXISTS idx_items_name ON items(name)")
        self.execute("CREATE INDEX IF NOT EXISTS idx_items_location ON items(location)")

    def execute(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self):
        self.conn.close()


# ------------------- Main Application -------------------
class App(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.lang = "de"
        self.db = EasySQL(DB_FILE)
        self.sort_column = "id"
        self.sort_desc = False
        self.selected_id = None
        self.low_only = tk.BooleanVar(value=False)

        self._init_style()
        self._build_ui()
        self._apply_language()
        self._refresh_table()


    # ---------- Style / Window ----------
    def _init_style(self):
        self.master.title(LANG[self.lang]["title"])
        self.master.geometry("1980x700")
        self.master.minsize(1800, 620)
        style = ttk.Style()
        for th in ("vista", "xpnative", "clam", "default"):
            if th in style.theme_names():
                try:
                    style.theme_use(th)
                    break
                except Exception:
                    continue
        style.configure("TLabel", padding=4)
        style.configure("TButton", padding=6)
        style.configure("TEntry", padding=4)
        style.configure("Status.TLabel", foreground="#666")


    # ---------- Build UI ----------
    def _build_ui(self):
        top = ttk.Frame(self.master)
        top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        self.btn_github = ttk.Button(top, text="GitHub", command=lambda: webbrowser.open(GITHUB_URL))
        self.btn_github.pack(side=tk.RIGHT, padx=(6, 0))
        self.btn_info = ttk.Button(top, text="Info", command=self._show_info)
        self.btn_info.pack(side=tk.RIGHT, padx=(6, 0))

        self.cmb_lang = ttk.Combobox(top, state="readonly", values=["de", "en"], width=6)
        self.cmb_lang.set(self.lang)
        self.cmb_lang.pack(side=tk.RIGHT, padx=(6, 0))
        self.cmb_lang.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.nb = ttk.Notebook(self.master)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.tab_inv = ttk.Frame(self.nb)
        self.nb.add(self.tab_inv, text="Inventar")

        self.frm_details = ttk.LabelFrame(self.tab_inv, text="Artikel-Details")
        self.frm_details.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 6), pady=10)

        self.var_name = tk.StringVar()
        self.var_sku = tk.StringVar()
        self.var_location = tk.StringVar()
        self.var_qty = tk.StringVar(value="0")
        self.var_minqty = tk.StringVar(value="0")

        row = ttk.Frame(self.frm_details); row.pack(fill=tk.X, padx=10, pady=(10, 4))
        self.lbl_name = ttk.Label(row, text="Name"); self.lbl_name.pack(anchor="w")
        self.ent_name = ttk.Entry(row, textvariable=self.var_name, width=34); self.ent_name.pack(fill=tk.X)

        row = ttk.Frame(self.frm_details); row.pack(fill=tk.X, padx=10, pady=4)
        self.lbl_sku = ttk.Label(row, text="SKU"); self.lbl_sku.pack(anchor="w")
        self.ent_sku = ttk.Entry(row, textvariable=self.var_sku); self.ent_sku.pack(fill=tk.X)

        row = ttk.Frame(self.frm_details); row.pack(fill=tk.X, padx=10, pady=4)
        self.lbl_location = ttk.Label(row, text="Lagerort"); self.lbl_location.pack(anchor="w")
        self.ent_location = ttk.Entry(row, textvariable=self.var_location); self.ent_location.pack(fill=tk.X)

        row = ttk.Frame(self.frm_details); row.pack(fill=tk.X, padx=10, pady=4)
        self.lbl_qty = ttk.Label(row, text="Menge"); self.lbl_qty.pack(anchor="w")
        self.ent_qty = ttk.Entry(row, textvariable=self.var_qty); self.ent_qty.pack(fill=tk.X)

        row = ttk.Frame(self.frm_details); row.pack(fill=tk.X, padx=10, pady=4)
        self.lbl_minqty = ttk.Label(row, text="Min.-Menge (Alert)"); self.lbl_minqty.pack(anchor="w")
        self.ent_minqty = ttk.Entry(row, textvariable=self.var_minqty); self.ent_minqty.pack(fill=tk.X)

        row = ttk.Frame(self.frm_details); row.pack(fill=tk.BOTH, expand=False, padx=10, pady=4)
        self.lbl_notes = ttk.Label(row, text="Notizen"); self.lbl_notes.pack(anchor="w")
        self.txt_notes = tk.Text(self.frm_details, height=6, width=32)
        self.txt_notes.pack(fill=tk.BOTH, expand=False, padx=10)

        btns = ttk.Frame(self.frm_details); btns.pack(fill=tk.X, padx=10, pady=10)
        self.btn_new = ttk.Button(btns, text="Neu", command=self._on_new); self.btn_new.pack(side=tk.LEFT)
        self.btn_save = ttk.Button(btns, text="Speichern", command=self._on_save); self.btn_save.pack(side=tk.LEFT, padx=6)
        self.btn_update = ttk.Button(btns, text="Aktualisieren", command=self._on_update); self.btn_update.pack(side=tk.LEFT, padx=6)
        self.btn_delete = ttk.Button(btns, text="Löschen", command=self._on_delete); self.btn_delete.pack(side=tk.LEFT, padx=6)
        self.btn_clear = ttk.Button(btns, text="Felder leeren", command=self._clear_form); self.btn_clear.pack(side=tk.LEFT, padx=6)

        right = ttk.Frame(self.tab_inv)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 10), pady=10)

        searchbar = ttk.Frame(right); searchbar.pack(fill=tk.X)
        self.lbl_search = ttk.Label(searchbar, text="Suche"); self.lbl_search.pack(side=tk.LEFT)

        self.var_search = tk.StringVar()
        self.ent_search = ttk.Entry(searchbar, textvariable=self.var_search)
        self.ent_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.ent_search.insert(0, LANG[self.lang]["placeholder_search"])
        self.ent_search.bind("<FocusIn>", self._clear_search_placeholder)
        self.ent_search.bind("<KeyRelease>", lambda e: self._refresh_table())

        self.chk_low = ttk.Checkbutton(searchbar, variable=self.low_only, command=self._refresh_table, text="Nur Niedrigbestand")
        self.chk_low.pack(side=tk.LEFT, padx=(8, 0))

        toolbar = ttk.Frame(right); toolbar.pack(fill=tk.X, pady=(6, 4))
        self.btn_export_csv = ttk.Button(toolbar, text="Export CSV", command=self._export_csv)
        self.btn_export_csv.pack(side=tk.LEFT)
        self.btn_export_json = ttk.Button(toolbar, text="Export JSON", command=self._export_json)
        self.btn_export_json.pack(side=tk.LEFT, padx=6)
        self.btn_import_csv = ttk.Button(toolbar, text="Import CSV", command=self._import_csv)
        self.btn_import_csv.pack(side=tk.LEFT, padx=6)

        self.tree = ttk.Treeview(
            right,
            columns=("id","name","sku","location","qty","minqty","notes","created","updated"),
            show="headings",
            selectmode="browse"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        for col, width in [
            ("id",60), ("name",220), ("sku",150), ("location",150),
            ("qty",80), ("minqty",100), ("notes",320), ("created",150), ("updated",150)
        ]:
            self.tree.column(col, width=width, anchor=tk.W)
        self._setup_headings()


        # Tag for low-stock highlighting
        self.tree.tag_configure("low", background="#ffe5e5")


        # Status bar
        sb = ttk.Frame(self.master)
        sb.pack(side=tk.BOTTOM, fill=tk.X)
        self.status = ttk.Label(sb, text=LANG[self.lang]["status_ready"], style="Status.TLabel")
        self.status.pack(anchor="w", padx=10, pady=4)

    def _setup_headings(self):
        headers = {
            "id": LANG[self.lang]["col_id"],
            "name": LANG[self.lang]["col_name"],
            "sku": LANG[self.lang]["col_sku"],
            "location": LANG[self.lang]["col_location"],
            "qty": LANG[self.lang]["col_qty"],
            "minqty": LANG[self.lang]["col_minqty"],
            "notes": LANG[self.lang]["col_notes"],
            "created": LANG[self.lang]["col_created"],
            "updated": LANG[self.lang]["col_updated"],
        }
        for col in headers:
            self.tree.heading(col, text=headers[col], command=lambda c=col: self._sort_by(c))


    # ---------- Localization Application ----------
    def _apply_language(self):
        self.master.title(LANG[self.lang]["title"])
        self.nb.tab(self.tab_inv, text=LANG[self.lang]["tab_inventory"])
        self.frm_details.config(text=LANG[self.lang]["group_form"])

        self.lbl_name.config(text=LANG[self.lang]["lbl_name"])
        self.lbl_sku.config(text=LANG[self.lang]["lbl_sku"])
        self.lbl_location.config(text=LANG[self.lang]["lbl_location"])
        self.lbl_qty.config(text=LANG[self.lang]["lbl_qty"])
        self.lbl_minqty.config(text=LANG[self.lang]["lbl_minqty"])
        self.lbl_notes.config(text=LANG[self.lang]["lbl_notes"])

        self.btn_new.config(text=LANG[self.lang]["btn_new"])
        self.btn_save.config(text=LANG[self.lang]["btn_save"])
        self.btn_update.config(text=LANG[self.lang]["btn_update"])
        self.btn_delete.config(text=LANG[self.lang]["btn_delete"])
        self.btn_clear.config(text=LANG[self.lang]["btn_clear"])

        self.lbl_search.config(text=LANG[self.lang]["search"])
        if (not self.var_search.get()) or (self.var_search.get() in (LANG["de"]["placeholder_search"], LANG["en"]["placeholder_search"])):
            self.ent_search.delete(0, tk.END)
            self.ent_search.insert(0, LANG[self.lang]["placeholder_search"])

        self.btn_export_csv.config(text=LANG[self.lang]["btn_export_csv"])
        self.btn_export_json.config(text=LANG[self.lang]["btn_export_json"])
        self.btn_import_csv.config(text=LANG[self.lang]["btn_import_csv"])
        self.chk_low.config(text=LANG[self.lang]["chk_low_only"])

        self.btn_info.config(text=LANG[self.lang]["btn_info"])
        self.btn_github.config(text=LANG[self.lang]["btn_github"])

        self._setup_headings()
        self.status.config(text=LANG[self.lang]["status_ready"])


    # ---------- Events ----------
    def _on_lang_change(self, _e):
        new_lang = self.cmb_lang.get()
        if new_lang in LANG:
            self.lang = new_lang
            self._apply_language()
            self._refresh_table()

    def _clear_search_placeholder(self, _e):
        if self.var_search.get() in (LANG["de"]["placeholder_search"], LANG["en"]["placeholder_search"]):
            self.ent_search.delete(0, tk.END)

    def _show_info(self):
        messagebox.showinfo(APP_NAME, LANG[self.lang]["info_text"])

    def _on_new(self):
        self.selected_id = None
        self._clear_form()
        self.status.config(text=LANG[self.lang]["status_ready"])

    def _clear_form(self):
        self.var_name.set("")
        self.var_sku.set("")
        self.var_location.set("")
        self.var_qty.set("0")
        self.var_minqty.set("0")
        self.txt_notes.delete("1.0", tk.END)

    def _validate_form(self):
        name = self.var_name.get().strip()
        sku = self.var_sku.get().strip()
        if not name and not sku:
            messagebox.warning(self.master, LANG[self.lang]["required_fields"])
            return None
        try:
            qty = int(self.var_qty.get().strip())
        except ValueError:
            messagebox.warning(self.master, LANG[self.lang]["invalid_qty"])
            return None
        try:
            minqty = int(self.var_minqty.get().strip())
        except ValueError:
            messagebox.warning(self.master, LANG[self.lang]["invalid_minqty"])
            return None
        location = self.var_location.get().strip()
        notes = self.txt_notes.get("1.0", tk.END).strip()
        return dict(name=name, sku=sku, location=location, qty=qty, minqty=minqty, notes=notes)

    def _on_save(self):
        data = self._validate_form()
        if not data:
            return
        now = datetime.datetime.now().isoformat(timespec="seconds")
        self.db.execute("""
            INSERT INTO items(name, sku, location, qty, min_qty, notes, created_at, updated_at)
            VALUES(?,?,?,?,?,?,?,?)
        """, (data["name"], data["sku"], data["location"], data["qty"], data["minqty"], data["notes"], now, now))
        self._refresh_table()
        self._clear_form()
        self.status.config(text=LANG[self.lang]["status_saved"])

    def _on_update(self):
        if not self.selected_id:
            messagebox.warning(self.master, LANG[self.lang]["no_selection"])
            return
        data = self._validate_form()
        if not data:
            return
        now = datetime.datetime.now().isoformat(timespec="seconds")
        self.db.execute("""
            UPDATE items
            SET name=?, sku=?, location=?, qty=?, min_qty=?, notes=?, updated_at=?
            WHERE id=?
        """, (data["name"], data["sku"], data["location"], data["qty"], data["minqty"], data["notes"], now, self.selected_id))
        self._refresh_table()
        self.status.config(text=LANG[self.lang]["status_updated"])

    def _on_delete(self):
        if not self.selected_id:
            messagebox.warning(self.master, LANG[self.lang]["no_selection"])
            return
        if messagebox.askyesno(LANG[self.lang]["dialog_confirm"], LANG[self.lang]["confirm_delete"]):
            self.db.execute("DELETE FROM items WHERE id=?", (self.selected_id,))
            self._refresh_table()
            self._on_new()
            self.status.config(text=LANG[self.lang]["status_deleted"])

    def _on_select(self, _e):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        
        
        # (id, name, sku, location, qty, minqty, notes, created, updated)
        self.selected_id = int(vals[0])
        self.var_name.set(vals[1] or "")
        self.var_sku.set(vals[2] or "")
        self.var_location.set(vals[3] or "")
        self.var_qty.set(str(vals[4]))
        self.var_minqty.set(str(vals[5]))
        self.txt_notes.delete("1.0", tk.END)
        self.txt_notes.insert("1.0", vals[6] or "")


    # ---------- Query / Table ----------
    def _build_search_clause(self, q: str):
        q = (q or "").strip()
        if not q or q in (LANG["de"]["placeholder_search"], LANG["en"]["placeholder_search"]):
            return "", ()
        like = f"%{q}%"
        return "WHERE name LIKE ? OR sku LIKE ? OR location LIKE ? OR notes LIKE ?", (like, like, like, like)

    def _refresh_table(self):
        
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Build query
        q = self.var_search.get()
        where, params = self._build_search_clause(q)
        low_filter = ""
        if self.low_only.get():
            
            # qty < min_qty AND min_qty > 0
            low_filter = " AND (qty < min_qty AND min_qty > 0)" if where else "WHERE (qty < min_qty AND min_qty > 0)"
        order = f"ORDER BY {self.sort_column} {'DESC' if self.sort_desc else 'ASC'}"

        rows = self.db.query(f"""
            SELECT id, name, sku, location, qty, min_qty, notes, created_at, updated_at
            FROM items
            {where} {low_filter} {order}
        """, params)


        # Populate rows with low-stock tag
        for r in rows:
            is_low = (r["min_qty"] is not None) and (r["min_qty"] > 0) and (r["qty"] < r["min_qty"])
            tags = ("low",) if is_low else ()
            self.tree.insert("", tk.END, values=(
                r["id"], r["name"], r["sku"], r["location"], r["qty"], r["min_qty"],
                r["notes"], r["created_at"], r["updated_at"]
            ), tags=tags)

    def _sort_by(self, column: str):
        if self.sort_column == column:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_column = column
            self.sort_desc = False
        self._refresh_table()


    # ---------- Import / Export ----------
    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            title=LANG[self.lang]["dialog_export_csv_title"],
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        rows = self.db.query("""
            SELECT id, name, sku, location, qty, min_qty, notes, created_at, updated_at
            FROM items ORDER BY id ASC
        """)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["id","name","sku","location","qty","min_qty","notes","created_at","updated_at"])
            for r in rows:
                writer.writerow([r["id"], r["name"], r["sku"], r["location"], r["qty"],
                                 r["min_qty"], r["notes"], r["created_at"], r["updated_at"]])
        self.status.config(text=LANG[self.lang]["status_exported"])
        messagebox.showinfo(APP_NAME, LANG[self.lang]["export_done"])

    def _export_json(self):
        path = filedialog.asksaveasfilename(
            title=LANG[self.lang]["dialog_export_json_title"],
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        rows = self.db.query("""
            SELECT id, name, sku, location, qty, min_qty, notes, created_at, updated_at
            FROM items ORDER BY id ASC
        """)
        data = [dict(r) for r in rows]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.status.config(text=LANG[self.lang]["status_exported"])
        messagebox.showinfo(APP_NAME, LANG[self.lang]["export_done"])

    def _import_csv(self):
        path = filedialog.askopenfilename(
            title=LANG[self.lang]["dialog_import_csv_title"],
            filetypes=[("CSV", "*.csv"), ("All Files", "*.*")]
        )
        if not path:
            return


        # Robust delimiter detection
        with open(path, "r", encoding="utf-8") as f:
            sample = f.read(2048)
            f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=";,")
                delimiter = dialect.delimiter
            except Exception:
                delimiter = ";"
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                name = (row.get("name","") or "").strip()
                sku = (row.get("sku","") or "").strip()
                location = (row.get("location","") or "").strip()
                try:
                    qty = int((row.get("qty","0") or "0"))
                except ValueError:
                    qty = 0
                    
                    
                # accept both min_qty and minqty
                min_qty_raw = row.get("min_qty", row.get("minqty", "0"))
                try:
                    min_qty = int((min_qty_raw or "0"))
                except ValueError:
                    min_qty = 0
                notes = (row.get("notes","") or "").strip()
                now = datetime.datetime.now().isoformat(timespec="seconds")
                self.db.execute("""
                    INSERT INTO items(name, sku, location, qty, min_qty, notes, created_at, updated_at)
                    VALUES(?,?,?,?,?,?,?,?)
                """, (name, sku, location, qty, min_qty, notes, now, now))

        self._refresh_table()
        self.status.config(text=LANG[self.lang]["status_imported"])
        messagebox.showinfo(APP_NAME, LANG[self.lang]["import_done"])


# ------------------- Entrypoint -------------------
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
