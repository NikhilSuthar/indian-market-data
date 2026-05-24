---
layout: default
title: Spot Market
nav_order: 2
parent: MCX India
---

# MCX — Spot Market Prices

**Package:** `mcx-data` | **Install:** `pip install mcx-data`

MCX India publishes daily spot prices for 28 commodities across metals, energy, agri, and others.

```bash
pip install mcx-data
```

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Confirmed working — DataFrame + Download |

---

## Available Commodities

28 commodities as of May 2026:

| Metals | Energy | Agri / Others |
|--------|--------|---------------|
| GOLD, GOLDM, GOLDTEN | CRUDEOIL, CRUDEOILM | CARDAMOM, COTTON, COTTONOIL |
| GOLDGUINEA, GOLDPETAL | NATURALGAS, NATGASMINI | KAPAS, MENTHAOIL |
| SILVER, SILVERM, SILVERMIC | ELECDMBL | CPO |
| COPPER | | |
| ALUMINIUM, ALUMINI | | |
| LEAD, LEADMINI | | |
| NICKEL | | |
| ZINC, ZINCMINI | | |
| STEELREBAR | | |

---

## Datasets

### ✅ Spot Market Price — Recent

Today's spot prices for all commodities. No date param needed — always returns current market data.

```python
from mcxdata import mcx

# All 28 commodities
df = mcx.get_spot_recent()

# Single commodity filter
df = mcx.get_spot_recent(commodity="GOLD")
df = mcx.get_spot_recent(commodity="SILVER")
df = mcx.get_spot_recent(commodity="CRUDEOIL")
```

**Columns:** `Commodity, Unit, Location, Spot Price (Rs.), Up/Down, Date`

**Sample output:**

| Commodity | Unit | Location | Spot Price (Rs.) | Up/Down | Date |
|-----------|------|----------|-----------------|---------|------|
| GOLD | 10 GRMS | AHMEDABAD | 157549.0 | -0.20 | 22-May-2026 |
| SILVER | 1 KGS | AHMEDABAD | 266292.0 | -0.57 | 22-May-2026 |
| CRUDEOIL | 1 BBL | NA | 9280.0 | -2.48 | 22-May-2026 |

**API endpoint:** `POST https://www.mcxindia.com/backpage.aspx/GetSpotMarketPrice`

---

### ✅ Spot Market Price — Archive

Historical spot prices for a specific commodity over a date range.

> **Note:** MCX archive requires a specific commodity — `"ALL"` returns empty. Use commodity names from the table above.

```python
from mcxdata import mcx

# GOLD for May 2026
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")

# SILVER for April 2026
df = mcx.get_spot_archive("2026-04-01", "2026-04-30", commodity="SILVER")

# Also accepts DD/MM/YYYY format
df = mcx.get_spot_archive("01/05/2026", "22/05/2026", commodity="CRUDEOIL")
```

**Columns:** `Commodity, Unit, Location, Spot Price (Rs.), Up/Down, Date`

**Sample output (GOLD, May 2026):**

| Commodity | Unit | Location | Spot Price (Rs.) | Up/Down | Date |
|-----------|------|----------|-----------------|---------|------|
| GOLD | 10 GRMS | AHMEDABAD | 157549.0 | -1 | 22-May-2026 |
| GOLD | 10 GRMS | AHMEDABAD | 157857.0 | 1 | 22-May-2026 |
| GOLD | 10 GRMS | AHMEDABAD | 157838.0 | -1 | 21-May-2026 |

Returns ~30 rows per month per commodity (multiple sessions per day).

**API endpoint:** `POST https://www.mcxindia.com/backpage.aspx/GetSpotMarketArchive`
**Payload:** `{"Product":"GOLD","Location":"ALL","Fromdate":"20260501","Session":"0","Todate":"20260522"}`

---

## Generic API

Mirrors the `nse-data` pattern:

```python
from mcxdata import mcx

# Recent
df = mcx.get("spot", "market", "spot_recent")
df = mcx.get("spot", "market", "spot_recent", commodity="GOLD")

# Archive
df = mcx.get("spot", "market", "spot_archive",
             from_date="2026-05-01", to_date="2026-05-22", commodity="GOLD")
```

---

## Download to Disk or S3

```python
from mcxdata import mcx

# Save to local file
mcx.download("spot", "market", "spot_recent",
             output_dir="./mcx_data")
# → ./mcx_data/MCX_spot_recent_ALL_20260522.csv

# Save archive to S3
mcx.download("spot", "market", "spot_archive",
             from_date="2026-05-01", to_date="2026-05-22",
             commodity="GOLD",
             s3_bucket="my-bucket", s3_prefix="raw/mcx/")
# → s3://my-bucket/raw/mcx/MCX_spot_archive_GOLD_20260522.csv
```

---

## CLI

```bash
# Today's spot prices
mcx-data spot-recent

# Single commodity
mcx-data spot-recent --commodity GOLD

# Archive
mcx-data spot-archive --from 01/05/2026 --to 22/05/2026 --commodity GOLD

# Save to S3
mcx-data spot-archive --from 01/05/2026 --to 22/05/2026 \
  --commodity GOLD --s3-bucket my-bucket --s3-prefix raw/mcx/

# List datasets
mcx-data list

# List available commodities
mcx-data commodities
```

---

## List Datasets & Commodities

```python
from mcxdata import mcx

# All registered datasets
mcx.list_datasets()

# All 28 live commodity names from MCX
mcx.list_commodities()
```

---

## Session / WAF Notes

MCX India uses **Akamai WAF** which blocks plain Python `requests`. `mcx-data` automatically uses:

1. **`curl-cffi`** (preferred) — Chrome TLS fingerprint impersonation, bypasses Akamai
2. **`cloudscraper`** (fallback) — if `curl-cffi` not installed
3. **`requests`** (last resort) — may 403 on restricted IPs

For best results (especially on Lambda), `curl-cffi` is installed as a required dependency:

```bash
pip install mcx-data          # includes curl-cffi automatically
```

Lambda IPs are generally unblocked by Akamai — MCX data works reliably on AWS Lambda.
