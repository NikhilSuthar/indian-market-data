---
layout: default
title: Debt — Corporate Segment
nav_order: 11
parent: NSE India
---

# Debt — Corporate Segment

**Category:** `debt` | **Sub-section:** `corporate`

NSE portal: [All Reports → Debt → Corporate Bond Market](https://www.nseindia.com/all-reports)

---

> **Note on timing:** Settlement files (cbm_*, sdt_*, cp_*, cd_*, gsec_*) are published on T-1 (previous trading day). Use yesterday's date for these.

---

### ✅ CB Daily Trades — same-day availability

```python
df = nse.get("debt", "corporate", "cbm_trd", "2026-05-22")
```
`cbm_trd{YYYYMMDD}.csv` | 511 rows × 8 cols

---

### ✅ Corporate Bond Monthly Report — same-day

```python
df = nse.get("debt", "corporate", "corporate_bond_report", "2026-05-22")
```
`Corporate_bond_report_{DD-Mon-YYYY}.csv` | 3,618 rows × 25 cols

---

### 🕐 Settlement Lists — T-1 (previous trading day)

```python
# Use T-1 date (e.g. May 21 for May 22 run)
t1_date = "2026-05-21"
df = nse.get("debt", "corporate", "cbm_list_man",      t1_date)
df = nse.get("debt", "corporate", "cbm_list_non_man",  t1_date)
df = nse.get("debt", "corporate", "cbm_fail",          t1_date)
df = nse.get("debt", "corporate", "cbm_unlist_man",    t1_date)
df = nse.get("debt", "corporate", "cbm_unlist_non_man",t1_date)
df = nse.get("debt", "corporate", "sdt_fail",          t1_date)
df = nse.get("debt", "corporate", "sdt_list_man",      t1_date)
df = nse.get("debt", "corporate", "sdt_list_non_man",  t1_date)
df = nse.get("debt", "corporate", "sdt_unlist_man",    t1_date)
df = nse.get("debt", "corporate", "sdt_unlist_non_man",t1_date)
df = nse.get("debt", "corporate", "cp_settlement",     t1_date)
df = nse.get("debt", "corporate", "cd_settlement",     t1_date)
df = nse.get("debt", "corporate", "gsec_settlement",   t1_date)
```

All return: `ISIN, Description, Trade Date, Quantity, Nominal Value, Weighted Average Price, Weighted Average Yield`
