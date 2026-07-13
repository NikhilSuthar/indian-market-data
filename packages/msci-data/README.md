# msci-data

<p align="center">
  <img src="https://raw.githubusercontent.com/NikhilSuthar/indian-market-data/main/docs/assets/msci.png" alt="MSCI" height="50"/>
</p>

**Download MSCI index levels as pandas DataFrames. No API key required.**

Pulls end-of-day index levels from MSCI's public levels API — the same one that powers charts on [msci.com/indexes](https://www.msci.com/indexes).

---

## Install

```bash
pip install msci-data
```

---

## Quick Start

```python
from mscidata import msci

# MSCI World — Net Total Return, date range
df = msci.get_levels("990100", "2026-01-01", "2026-07-01")
print(df)
#    INDEX_CODE VARIANT       RETURN_TYPE CURRENCY        DATE          LEVEL
# 0      990100    NETR  Net Total Return      USD  2026-01-02  14821.123456
# ...

# MSCI India — Price Return
df = msci.get_levels("106220", "2026-01-01", "2026-07-01", variant="price")

# MSCI Emerging Markets — Gross Total Return
df = msci.get_levels("664185", "2026-01-01", "2026-07-01", variant="gross")

# Multiple indices — concatenated into one DataFrame
df = msci.get_levels(["990100", "664185", "106220"], "2026-01-01", "2026-07-01")

# Single date
df = msci.get_levels("990100", "2026-07-03")

# List supported return variants
msci.list_variants()
```

---

## API Reference

### `msci.get_levels(index_codes, from_date, to_date=None, variant="NETR")`

| Param | Type | Description |
|---|---|---|
| `index_codes` | `str` or `list[str]` | MSCI numeric index code(s) |
| `from_date` | `str` | Start date — `"YYYY-MM-DD"` or `"YYYYMMDD"` |
| `to_date` | `str` | End date (defaults to `from_date` for single day) |
| `variant` | `str` | Return variant — see table below |

**Returns:** `DataFrame` with columns: `INDEX_CODE, VARIANT, RETURN_TYPE, CURRENCY, DATE, LEVEL`

### Return Variants

| Code | Aliases | Description |
|---|---|---|
| `STRD` | `price`, `pr` | Price Return |
| `NETR` | `net`, `ntr` | Net Total Return *(default)* |
| `GRTR` | `gross`, `tr`, `gtr` | Gross Total Return |

### `msci.download(index_codes, from_date, to_date=None, variant="NETR", output_dir=".", s3_bucket=None, s3_prefix="msci-data/")`

Download to local CSV or S3.

```python
# Local file
path = msci.download("990100", "2026-01-01", "2026-07-01")
# → MSCI_990100_NETR_20260101_20260701.csv

# S3 (Lambda with IAM role)
uri = msci.download(["990100", "664185"], "2026-01-01", "2026-07-01",
                     s3_bucket="my-bucket", s3_prefix="raw/msci/")
# → s3://my-bucket/raw/msci/MSCI_990100_664185_NETR_20260101_20260701.csv
```

---

## Common MSCI Index Codes

| Code | Index |
|---|---|
| `990100` | MSCI World (Developed Markets) |
| `891800` | MSCI ACWI (All Country World) |
| `664185` | MSCI Emerging Markets |
| `106220` | MSCI India |
| `929887` | MSCI USA |
| `990300` | MSCI EAFE (Europe, Australasia, Far East) |

Index codes are the numeric identifiers from MSCI's URL structure on msci.com/indexes.

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

# List variants
msci-data variants
```

---

## Notes

- Data goes back to **2000-01-01** (MSCI API floor date)
- Currency is fixed to **USD**
- Data frequency is **daily** (trading days only)
- No authentication required — uses MSCI's public chart data API

---

## Links

- [PyPI](https://pypi.org/project/msci-data/)
- [Documentation](https://NikhilSuthar.github.io/indian-market-data)
- [GitHub](https://github.com/NikhilSuthar/indian-market-data)
