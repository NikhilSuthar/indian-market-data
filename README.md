# nse-data

[![PyPI version](https://badge.fury.io/py/nse-data.svg)](https://pypi.org/project/nse-data/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library to download market data from NSE India as pandas DataFrames.

Works reliably from **AWS Lambda**, **Snowflake**, and any cloud/serverless environment — no Cloudflare bypass needed.

## Installation

```bash
pip install nse-data
```

From TestPyPI (latest dev):

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nse-data==0.2.2
```

## Quick Start

```python
from nsedata import reports

# Universal getter — returns DataFrame for any report type
df = reports.get("sec_bhavdata_full", "2026-05-19")
df = reports.get("ind_close_all", "2026-05-19")
df = reports.get("security_master", "2026-05-19")
df = reports.get("cmvolt", "2026-05-19")

# Named convenience functions
df = reports.get_bhavcopy("2026-05-19")
df = reports.get_sec_bhavdata("2026-05-19")
df = reports.get_ind_close_all("2026-05-19")
df = reports.get_market_activity("2026-05-19")

# Download raw file to disk (for .DAT/.T01 or archival)
from nsedata.reports import download_report
path = download_report("mto", "2026-05-19", output_dir="./data")
```

## Command Line

```bash
# Parse report and save as CSV
nse-data reports --type bhavcopy --date 2026-05-19
nse-data reports --type sec_bhavdata --date 2026-05-19
nse-data reports --type ind_close_all --date 2026-05-19

# Download raw file to disk
nse-data download --type cmvolt --date 2026-05-19 --out ./data
nse-data download --type security_master --date 2026-05-19 --out ./data
nse-data download --type mto --date 2026-05-19 --out ./data
```

## Complete Report Type Reference

All report types work with `reports.get(type, date)` → returns `pandas.DataFrame`.

Date format for all: **`YYYY-MM-DD`** (e.g. `"2026-05-19"`)

### Capital Market — Prices

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `pr` | `PR{DDMMYY}.zip` → `pr{DDMMYYYY}.csv` | ZIP containing 13 files | CSV (main price file extracted) |
| `sec_bhavdata_full` | `sec_bhavdata_full_{DDMMYYYY}.csv` | CSV | CSV |
| `bhav_udiff` | `BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | CSV |
| `sme` | `sme{DDMMYYYY}.csv` | CSV | CSV |

### Capital Market — Indices

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `ind_close_all` | `ind_close_all_{DDMMYYYY}.csv` | CSV | CSV |
| `pe` | `PE_{DDMMYY}.csv` | CSV | CSV |
| `reg_ind` | `REG_IND{DDMMYY}.csv` | CSV | CSV |

### Capital Market — Activity & Deals

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `market_activity` | `MA{DDMMYY}.csv` | CSV | CSV |
| `short_selling` | `shortselling_{DDMMYYYY}.csv` | CSV | CSV |

### Capital Market — Reference & Master

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `security_master` | `NSE_CM_security_{DDMMYYYY}.csv.gz` | GZIP→CSV | CSV (decompressed in memory) |
| `cm_52wk` | `CM_52_wk_High_low_{DDMMYYYY}.csv` | CSV | CSV |

### Capital Market — Risk & Margin

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `cmvolt` | `CMVOLT_{DDMMYYYY}.CSV` | CSV | CSV |
| `mto` | `MTO_{DDMMYYYY}.DAT` | DAT (fixed-width) | ⚠️ Best-effort parse; use `download_report()` for raw file |

### Derivatives — Equity F&O

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `fo_secban` | `fo_secban_{DDMMYYYY}.csv` | CSV | CSV |
| `fovolt` | `FOVOLT_{DDMMYYYY}.csv` | CSV | CSV |
| `fo_sett` | `FOSett_prce_{DDMMYYYY}.csv` | CSV | CSV |

### Derivatives — Commodity & Currency

| Input Param | NSE File Name | Source Format | Parsed As |
|-------------|---------------|---------------|-----------|
| `co_volt` | `CO_VOLT_{DDMMYYYY}.csv` | CSV | CSV |
| `x_volt` | `X_VOLT_{DDMMYYYY}.csv` | CSV | CSV |
| `cd_sett` | `CDSett_prce_{DDMMYYYY}.csv` | CSV | CSV |
| `trm_bc` | `TRM_BC{DDMMYYYY}.csv` | CSV | CSV |

### ⚠️ DAT/T01 Files

Files with `.DAT` or `.T01` extensions are fixed-width or pipe-delimited formats. `reports.get()` attempts to auto-detect the delimiter, but results may not be clean. For these files, prefer:

```python
# Download raw file, then parse manually
path = reports.download_report("mto", "2026-05-19", "./data")
# Parse with your own logic
df = pd.read_fwf(path)  # or custom parsing
```

## Source URLs

All data comes from `nsearchives.nseindia.com` — direct file downloads, no Cloudflare:

```
https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/content/indices/ind_close_all_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/content/cm/NSE_CM_security_{DDMMYYYY}.csv.gz
https://nsearchives.nseindia.com/archives/nsccl/volt/CMVOLT_{DDMMYYYY}.CSV
https://nsearchives.nseindia.com/archives/fo/sec_ban/fo_secban_{DDMMYYYY}.csv
```

## Cloud / Lambda Usage

```python
# AWS Lambda handler example
from nsedata import reports

def handler(event, context):
    date = event["date"]  # "2026-05-19"
    df = reports.get("sec_bhavdata_full", date)
    # Write to S3, Snowflake, etc.
    return {"rows": len(df), "columns": list(df.columns)}
```

**Dependencies:** Only `requests` + `pandas` — no heavy browser/Cloudflare libraries.

## Important Notes

- Data source is `nsearchives.nseindia.com` — **no Cloudflare**, works from any IP
- Data is only available for **trading days** (weekends/holidays return HTTP errors)
- NSE may rate-limit aggressive requests — add delays for bulk downloads
- URL patterns may change without notice — pin your version
- `.DAT`/`.T01` files may not parse cleanly as DataFrames — use `download_report()` for raw files

## Dependencies

| Package | Purpose |
|---------|---------|
| [requests](https://docs.python-requests.org/) | HTTP client |
| [pandas](https://pandas.pydata.org/) | DataFrame output |

## Contributing

```bash
git clone https://github.com/NikhilSuthar/nse-data.git
cd nse-data
pip install -e ".[dev]"
pytest
ruff check src/
```

## License

MIT — see [LICENSE](LICENSE) for details.
