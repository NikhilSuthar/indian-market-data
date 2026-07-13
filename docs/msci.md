---
layout: default
title: MSCI
nav_order: 5
has_children: false
permalink: /msci
---

# MSCI

<img src="{{ '/assets/msci.png' | relative_url }}" alt="MSCI" style="height:50px;width:auto;max-width:160px;object-fit:contain;"/>

**msci-data** — Download MSCI index end-of-day levels as pandas DataFrames. No API key required.

```bash
pip install msci-data
```

Pulls daily index levels from MSCI's public chart data API for any index code, in any return variant — Price, Net Total Return, or Gross Total Return.

---

## Quick Start

```python
from mscidata import msci

# MSCI World — Net Total Return (default)
df = msci.get_levels("990100", "2026-01-01", "2026-07-01")

# MSCI India — Price Return
df = msci.get_levels("106220", "2026-01-01", "2026-07-01", variant="price")

# MSCI Emerging Markets — Gross Total Return
df = msci.get_levels("664185", "2026-01-01", "2026-07-01", variant="gross")

# Multiple indices — concatenated into one DataFrame
df = msci.get_levels(["990100", "664185", "106220"], "2026-01-01", "2026-07-01")

# Single date
df = msci.get_levels("990100", "2026-07-03")

# List supported variants
msci.list_variants()
```

---

## Output Columns

| Column | Description |
|--------|-------------|
| `INDEX_CODE` | MSCI numeric index code |
| `VARIANT` | API variant code (`STRD`, `NETR`, `GRTR`) |
| `RETURN_TYPE` | Human-readable return type |
| `CURRENCY` | Always `USD` |
| `DATE` | Trading date (`YYYY-MM-DD`) |
| `LEVEL` | End-of-day index level |

---

## Return Variants

| Code | Aliases | Description |
|------|---------|-------------|
| `STRD` | `price`, `pr` | Price Return |
| `NETR` | `net`, `ntr` | Net Total Return *(default)* |
| `GRTR` | `gross`, `tr`, `gtr` | Gross Total Return |

---

## Common Index Codes

| Code | Index |
|------|-------|
| `990100` | MSCI World (Developed Markets) |
| `891800` | MSCI ACWI (All Country World) |
| `664185` | MSCI Emerging Markets |
| `106220` | MSCI India |
| `929887` | MSCI USA |
| `990300` | MSCI EAFE (Europe, Australasia, Far East) |

Index codes are the numeric identifiers from MSCI's URL structure on [msci.com/indexes](https://www.msci.com/indexes).

---

## Download to S3

```python
from mscidata import msci

# Local CSV
path = msci.download("990100", "2026-01-01", "2026-07-01")
# → MSCI_990100_NETR_20260101_20260701.csv

# S3 (Lambda with IAM role)
uri = msci.download(
    ["990100", "664185"],
    "2026-01-01",
    "2026-07-01",
    s3_bucket="my-bucket",
    s3_prefix="raw/msci/",
)
```

---

## CLI

```bash
# Date range — MSCI World net return
msci-data levels --codes 990100 --from 2026-01-01 --to 2026-07-01

# Multiple indices, price variant
msci-data levels --codes 990100 664185 --from 2026-01-01 --to 2026-07-01 --variant price

# Save to S3
msci-data levels --codes 990100 --from 2026-01-01 --to 2026-07-01 \
                 --s3-bucket my-bucket --s3-prefix raw/msci/

# List return variants
msci-data variants
```

---

## Notes

- Data goes back to **2000-01-01** (MSCI API floor date)
- Currency is fixed to **USD**
- Frequency is **daily** (trading days only)
- No authentication required — uses MSCI's public chart data API
- No WAF or bot protection — plain `requests` works, no `curl_cffi` needed
