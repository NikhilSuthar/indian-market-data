---
layout: default
title: Capital Market — Indices
nav_order: 3
---

# Capital Market — Indices

**Category:** `capital_market` | **Sub-section:** `indices`

NSE portal path: All Reports → Capital Market → Indices

---

## All Indices Daily Close Values

Single-file snapshot of EOD values for **all 147+ NSE indices** — OHLC, P/E, P/B, Div Yield, Volume.

```python
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# Filter for Nifty 50
df[df["Index Name"] == "Nifty 50"]
```
```bash
nse-data get capital_market indices ind_close_all 2026-05-22
```
**File:** `ind_close_all_{DDMMYYYY}.csv`  
**~147 rows × 13 cols**  
**Columns:** `Index Name, Index Date, Open Index Value, High Index Value, Low Index Value, Closing Index Value, Points Change, Change(%), Volume, Turnover (Rs. Cr.), P/E, P/B, Div Yield`

---

## Index Top Movers

Top 10 securities by weight/movement for Nifty 50.

```python
df = nse.get("capital_market", "indices", "top_movers", "2026-05-22")
```
```bash
nse-data get capital_market indices top_movers 2026-05-22
```
**File:** `top10nifty50_{DDMMYY}.csv`  
**Columns:** `SYMBOL, SECURITY, WEIGHTAGE(%)`
