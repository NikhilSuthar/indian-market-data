---
layout: default
title: Python API — MCX
nav_order: 1
parent: MCX India
---

# Python API — MCX

```bash
pip install mcx-data
```

---

## Quick Start

```python
from mcxdata import mcx

# Today's spot prices — all 28 commodities
df = mcx.get_spot_recent()

# Historical archive — GOLD for May 2026
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
```

---

## `mcx.get_spot_recent()` — Today's Prices

```python
mcx.get_spot_recent(commodity="ALL", location="ALL") → pd.DataFrame
```

Returns spot prices as of the latest MCX polling session (updated ~2x daily).

```python
from mcxdata import mcx

# All 28 commodities
df = mcx.get_spot_recent()

# Filter by commodity
df = mcx.get_spot_recent(commodity="GOLD")
df = mcx.get_spot_recent(commodity="SILVER")
df = mcx.get_spot_recent(commodity="CRUDEOIL")
df = mcx.get_spot_recent(commodity="NATURALGAS")
df = mcx.get_spot_recent(commodity="COPPER")
```

**Returns:** `Commodity, Unit, Location, Spot Price (Rs.), Up/Down, Date`

| Commodity | Unit | Location | Spot Price (Rs.) | Up/Down | Date |
|-----------|------|----------|-----------------|---------|------|
| GOLD | 10 GRMS | AHMEDABAD | 157549.0 | -0.20 | 2026-05-22 12:33:08 |
| SILVER | 1 KGS | AHMEDABAD | 266292.0 | -0.57 | 2026-05-22 12:33:08 |
| CRUDEOIL | 1 BBL | NA | 9280.0 | -2.48 | 2026-05-22 12:33:08 |

---

## `mcx.get_spot_archive()` — Historical Prices

```python
mcx.get_spot_archive(from_date, to_date, commodity="ALL", location="ALL") → pd.DataFrame
```

> **Important:** MCX archive API requires a specific commodity — `"ALL"` returns empty. Always specify a commodity name.

```python
from mcxdata import mcx

# GOLD — May 2026
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")

# SILVER — April 2026
df = mcx.get_spot_archive("2026-04-01", "2026-04-30", commodity="SILVER")

# CRUDEOIL — year to date
df = mcx.get_spot_archive("2026-01-01", "2026-05-22", commodity="CRUDEOIL")

# Date formats accepted: YYYY-MM-DD, DD/MM/YYYY, YYYYMMDD
df = mcx.get_spot_archive("01/05/2026", "22/05/2026", commodity="GOLD")
```

**Returns:** `Commodity, Unit, Location, Spot Price (Rs.), Up/Down, Date`

| Commodity | Unit | Location | Spot Price (Rs.) | Up/Down | Date |
|-----------|------|----------|-----------------|---------|------|
| GOLD | 10 GRMS | AHMEDABAD | 157549.0 | -1 | 2026-05-22 12:33:08 |
| GOLD | 10 GRMS | AHMEDABAD | 157857.0 | 1 | 2026-05-22 08:15:12 |
| GOLD | 10 GRMS | AHMEDABAD | 157838.0 | -1 | 2026-05-21 12:27:04 |

Returns ~2 rows per trading day per commodity (morning + afternoon polling sessions).

---

## `mcx.list_commodities()` — Available Commodities

```python
commodities = mcx.list_commodities()
# → ['ALUMINI', 'ALUMINIUM', 'CARDAMOM', 'COPPER', 'COTTON', 'COTTONOIL',
#    'CPO', 'CRUDEOIL', 'CRUDEOILM', 'ELECDMBL', 'GOLD', 'GOLDGUINEA',
#    'GOLDM', 'GOLDPETAL', 'GOLDTEN', 'KAPAS', 'LEAD', 'LEADMINI',
#    'MENTHAOIL', 'NATGASMINI', 'NATURALGAS', 'NICKEL', 'SILVER', 'SILVERM',
#    'SILVERMIC', 'STEELREBAR', 'ZINC', 'ZINCMINI']
```

---

## Generic `mcx.get()` — Mirrors nse-data API

```python
# Recent
df = mcx.get("spot", "market", "spot_recent")
df = mcx.get("spot", "market", "spot_recent", commodity="GOLD")

# Archive
df = mcx.get("spot", "market", "spot_archive",
             from_date="2026-05-01", to_date="2026-05-22", commodity="GOLD")
```

---

## `mcx.download()` — Save to Disk or S3

```python
from mcxdata import mcx

# Local file
path = mcx.download("spot", "market", "spot_recent",
                    commodity="GOLD", output_dir="./data")
# → "./data/MCX_spot_recent_GOLD_20260522.csv"

# S3 (Lambda with IAM role)
uri = mcx.download("spot", "market", "spot_archive",
                   from_date="2026-05-01", to_date="2026-05-22",
                   commodity="GOLD",
                   s3_bucket="my-bucket", s3_prefix="raw/mcx/")
# → "s3://my-bucket/raw/mcx/MCX_spot_archive_GOLD_20260522.csv"
```

---

## Date Format

The `Date` column is returned as `YYYY-MM-DD HH:MM:SS` (UTC).

```python
df = mcx.get_spot_recent()
print(df["Date"].iloc[0])
# → "2026-05-22 12:33:08"
```

MCX polls spot prices at approximately **08:00 IST** and **12:30 IST** (02:30 UTC and 07:00 UTC). The archive returns both sessions per trading day.

To convert to IST in pandas:
```python
import pandas as pd
df["Date_IST"] = pd.to_datetime(df["Date"]).dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
```

---

## Error Handling

```python
from mcxdata import mcx

try:
    df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="ALL")
    # Returns empty DataFrame — MCX doesn't support ALL for archive
    if df.empty:
        print("No data — specify a commodity name")
except RuntimeError as e:
    print(f"Failed: {e}")
    # RuntimeError: HTTP 403 — Akamai WAF (curl_cffi not installed or blocked)
```
