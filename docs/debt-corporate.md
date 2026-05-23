---
layout: default
title: Debt — Corporate Segment
nav_order: 9
---

# Debt — Corporate Segment

**Category:** `debt` | **Sub-section:** `corporate`

NSE portal path: All Reports → Debt → Corporate Segment

---

All corporate bond settlement files share the same column structure:
`ISIN, Description, Trade Date, Quantity, Nominal Value, Weighted Average Price, Weighted Average Yield`

```python
# CB Daily Trades
df = nse.get("debt", "corporate", "cbm_trd", "2026-05-22")

# Settlement lists
df = nse.get("debt", "corporate", "cbm_list_man",      "2026-05-22")  # Mandatory
df = nse.get("debt", "corporate", "cbm_list_non_man",  "2026-05-22")  # Non-mandatory
df = nse.get("debt", "corporate", "cbm_fail",          "2026-05-22")  # Fails
df = nse.get("debt", "corporate", "cbm_unlist_man",    "2026-05-22")  # Unlisted mandatory
df = nse.get("debt", "corporate", "cbm_unlist_non_man","2026-05-22")  # Unlisted non-mandatory

# SDT (Settlement Direct Trades)
df = nse.get("debt", "corporate", "sdt_fail",         "2026-05-22")
df = nse.get("debt", "corporate", "sdt_list_man",     "2026-05-22")
df = nse.get("debt", "corporate", "sdt_list_non_man", "2026-05-22")
df = nse.get("debt", "corporate", "sdt_unlist_man",   "2026-05-22")
df = nse.get("debt", "corporate", "sdt_unlist_non_man","2026-05-22")

# Settlement order reports
df = nse.get("debt", "corporate", "cp_settlement",    "2026-05-22")  # Commercial Paper
df = nse.get("debt", "corporate", "cd_settlement",    "2026-05-22")  # Convertible Debenture
df = nse.get("debt", "corporate", "gsec_settlement",  "2026-05-22")  # G-Sec

# Monthly corporate bond report
df = nse.get("debt", "corporate", "corporate_bond_report", "2026-05-22")
```

```bash
nse-data get debt corporate cbm_trd 2026-05-22
nse-data get debt corporate cbm_list_man 2026-05-22
nse-data get debt corporate gsec_settlement 2026-05-22
```
