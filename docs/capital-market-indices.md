---
layout: default
title: Capital Market — Indices
nav_order: 5
parent: NSE India
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

---

## Historical Index Data & Total Return Index (TRI)

Historical OHLC and TRI come from `niftyindices.com` — a separate source.

> ⚠️ **Cloudflare note:** niftyindices.com is Cloudflare-protected. Works from residential IPs. May be blocked from AWS Lambda (AWS IP ranges are blocklisted by Cloudflare). Test it — if it works from your Lambda region, great. If not, use `derive_tri()` or the S3-handoff pattern.

### Install cloudscraper
```bash
pip install nse-archives[cloudflare]   # adds cloudscraper
# or: pip install cloudscraper
```

### Historical Price Index (OHLC)
```python
from nsedata import nse

df = nse.get_historical_index("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
df = nse.get_historical_index("nifty50", "01-Jan-2026", "31-Mar-2026")  # shorthand also works
```
```bash
nse-data get-index "NIFTY 50" --from "01-Jan-2026" --to "31-Mar-2026"
```
**Returns:** `Index Name, Date, Open, High, Low, Close`  
**Date format:** `dd-Mon-yyyy` (different from other datasets)

### Total Return Index (TRI)
TRI = price movement + dividends reinvested. Essential for AMC benchmarking.

```python
df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
df = nse.get_tri("niftybank", "01-Apr-2026", "30-Apr-2026")  # shorthand
```
**Returns:** `Index Name, Date, Total Returns Index, Net Total Return Index`

| Column | Description |
|--------|-------------|
| `Total Returns Index` | Gross TRI — dividends reinvested pre-tax |
| `Net Total Return Index` | Net TRI — dividends reinvested at ~15% tax |

### Available Index Shorthands
```python
nse.list_index_names()  # shows all shorthands and full names
```
Common: `nifty50`, `nifty100`, `niftybank`, `niftyit`, `niftyauto`, `niftypharma`, `niftyfmcg`, `niftynext50`

---

## Deriving TRI from Price Data (Lambda-compatible)

If niftyindices.com is blocked from Lambda, derive an approximate TRI from
`ind_close_all` data using the formula:

```
TRI(t) = TRI(t-1) × (Price(t) + Div(t)) / Price(t-1)
```

```python
# Step 1: get closing index values (works from Lambda)
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
nifty = df[df["Index Name"] == "Nifty 50"].rename(
    columns={"Index Date": "Date", "Closing Index Value": "Close"})

# Step 2: derive TRI (approximate — uses 1.5% annual yield estimate)
tri_df = nse.derive_tri(nifty)
print(tri_df[["Date", "Close", "Derived_TRI"]])

# Step 3: with actual dividends (more accurate)
# Get corporate actions from PR bundle
bc_df = nse.get("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22")
# ... extract index constituent dividends and pass to derive_tri(dividends=...)
```

**Note:** The derived TRI is approximate. The official TRI uses exact constituent-level dividend data and historical weights. For accurate TRI, use `nse.get_tri()` directly.
