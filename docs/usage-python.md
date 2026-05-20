---
layout: default
title: Python API
nav_order: 3
---

# Python API

## Indices Module

Source: [niftyindices.com/reports/historical-data](https://niftyindices.com/reports/historical-data)

### get_historical — Price Index (OHLC)

```python
from nsedata import indices

df = indices.get_historical("NIFTY 50", "01-Apr-2026", "15-Apr-2026")
print(df)
```

Output:

| Index Name | Date | Open | High | Low | Close |
|-----------|------|------|------|-----|-------|
| NIFTY 50 | 2026-04-01 | 23410.50 | 23562.80 | 23385.15 | 23519.35 |
| NIFTY 50 | 2026-04-02 | 23540.00 | 23648.90 | 23472.60 | 23612.45 |
| NIFTY 50 | 2026-04-03 | 23625.10 | 23710.55 | 23558.30 | 23689.70 |

**Parameters:**
- `index_name` (str) — Index name exactly as shown on niftyindices.com (e.g. `"NIFTY 50"`, `"NIFTY BANK"`, `"Nifty Auto"`)
- `start_date` (str) — Start date in `dd-Mon-yyyy` format (e.g. `"01-Apr-2026"`)
- `end_date` (str) — End date in `dd-Mon-yyyy` format (e.g. `"15-May-2026"`)

**Returns:** `pandas.DataFrame` with columns: `Index Name`, `Date`, `Open`, `High`, `Low`, `Close`

---

### get_tri — Total Return Index

```python
from nsedata import indices

df = indices.get_tri("NIFTY 50", "01-Apr-2026", "15-Apr-2026")
print(df)
```

Output:

| Index Name | Date | Total Returns Index | Net Total Return Index |
|-----------|------|--------------------|-----------------------|
| NIFTY 50 | 2026-04-01 | 38245.62 | 35812.48 |
| NIFTY 50 | 2026-04-02 | 38312.85 | 35875.30 |

**Parameters:** Same as `get_historical`

**Returns:** `pandas.DataFrame` with columns: `Index Name`, `Date`, `Total Returns Index`, `Net Total Return Index`

---

## Reports Module

Source: [nseindia.com/all-reports](https://www.nseindia.com/all-reports) → [nsearchives.nseindia.com](https://nsearchives.nseindia.com)

All report functions take a date in `YYYY-MM-DD` format.

### get_bhavcopy — Price Record (PR file)

```python
from nsedata import reports

df = reports.get_bhavcopy("2026-04-17")
print(df.head())
```

Downloads the PR zip file from NSE archives and extracts the CSV. Contains OHLC data for all traded securities.

**Key columns:** `SYMBOL`, `SERIES`, `OPEN_PRICE`, `HIGH_PRICE`, `LOW_PRICE`, `CLOSE_PRICE`, `NET_TRDVAL`, `NET_TRDQTY`

---

### get_sec_bhavdata — Full Security Bhavcopy with Delivery

```python
from nsedata import reports

df = reports.get_sec_bhavdata("2026-04-17")

# Filter for a specific stock
reliance = df[df["SYMBOL"] == "RELIANCE"]
print(reliance)
```

**Key columns:** `SYMBOL`, `SERIES`, `DATE1`, `PREV_CLOSE`, `OPEN_PRICE`, `HIGH_PRICE`, `LOW_PRICE`, `CLOSE_PRICE`, `LAST_PRICE`, `AVG_PRICE`, `TTL_TRD_QNTY`, `TURNOVER_LACS`, `NO_OF_TRADES`, `DELIV_QTY`, `DELIV_PER`

---

### get_ind_close_all — All Index Closing Values

```python
from nsedata import reports

df = reports.get_ind_close_all("2026-04-17")

# Filter for NIFTY 50
nifty = df[df["Index Name"] == "Nifty 50"]
print(nifty)
```

**Key columns:** `Index Name`, `Index Date`, `Open Index Value`, `High Index Value`, `Low Index Value`, `Closing Index Value`, `Points Change`, `Change(%)`, `Volume`, `Turnover (Rs. Cr.)`, `P/E`, `P/B`, `Div Yield`

---

### get_market_activity — Market Activity Report

```python
from nsedata import reports

df = reports.get_market_activity("2026-04-17")
print(df)
```

**Key columns:** `Category`, `No. of Trades`, `Traded Qty (Lacs)`, `Traded Value (Rs. Crores)`

---

### download_report — Save Raw File to Disk

```python
from nsedata.reports import download_report

# Download raw file without parsing
path = download_report("sec_bhavdata_full", "2026-04-17", output_dir="./data")
print(f"Saved to: {path}")
```

**Parameters:**
- `report_type` (str) — One of: `"pr"`, `"sec_bhavdata_full"`, `"ind_close_all"`, `"market_activity"`, `"bhav_copy"`
- `date` (str) — Date in `YYYY-MM-DD` format
- `output_dir` (str) — Directory to save the file (default: current directory)

**Returns:** `pathlib.Path` to the saved file

---

## Date Formats

| Module | Format | Example |
|--------|--------|---------|
| `indices` | `dd-Mon-yyyy` | `"01-Apr-2026"`, `"15-May-2026"` |
| `reports` | `YYYY-MM-DD` | `"2026-04-17"` |

The different formats match what the underlying NSE websites expect.

---

## Error Handling

All functions raise `RuntimeError` on HTTP errors:

```python
from nsedata import reports

try:
    df = reports.get_bhavcopy("2026-04-19")  # Saturday — no data
except RuntimeError as e:
    print(f"Failed: {e}")
    # Failed: Failed to download PR file: HTTP 403 for ...
```

Common errors:
- **HTTP 403** — NSE blocked the request (rate limiting or non-trading day)
- **HTTP 404** — File not available for that date
- **Timeout** — NSE server slow to respond
