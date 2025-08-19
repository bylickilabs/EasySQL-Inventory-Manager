# Usage Guide – EasySQL Inventory Manager

## Start the Application
```bash
python app.py
```

## Main Functions
1. **Add Item**
   - Fill in name, SKU, location, quantity, min. qty, and notes
   - Click **Save**

2. **Edit Item**
   - Select item in the table
   - Update fields → click **Update**

3. **Delete Item**
   - Select row → click **Delete**

4. **Search**
   - Use search bar for Name, SKU, or Location
   - Click column headers to sort

5. **Low-stock Alerts**
   - Items below **Min.-Qty** highlighted red
   - Toggle "Low-stock only" filter

6. **Export**
   - Save inventory as CSV or JSON

7. **Import**
   - Import CSV (`;` or `,` delimiters supported)

8. **Language**
   - Switch DE/EN from dropdown top-right

---

## Tips
- Keep backups of `inventory.db`
- Use CSV export for Excel compatibility
- JSON export for API/automation integrations

---

## Example Workflow
| Action | Steps |
|--------|-------|
| Add new item | Fill form → Save |
| Edit stock | Select row → change qty → Update |
| Highlight low stock | Set Min.-Qty lower than Qty |
| Export data | Click Export (CSV/JSON) |
| Import data | Choose CSV file with `;` or `,` delimiter |
