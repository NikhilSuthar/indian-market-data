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
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nse-data==0.2.0
```

## Quick Start

```python
from nsedata import reports

# Universal getter — works for all 20 report types, returns DataFrame
df = reports.get("sec_bhavdata_full", "2026-05-19")
df = reports.get("ind_close_all", "2026-05-19")
df = reports.get("cmvolt", "2026-05-19")
df = reports.get("fo_secban", "2026-05-19")

# Named convenience functions
df = reports.get_bhavcopy("2026-05-19")
df = reports.get_sec_bhavdata("2026-05-19")
df = reports.get_ind_close_all("2026-05-19")
df = reports.get_market_activity("2026-05-19")

# Download raw file to disk
from nsedata.reports import download_report
path = download_report("security_master", "2026-05-19", output_dir="./data")
```

## Command Line

```bash
# Parse report and save as CSV
nse-data reports --type bhavcopy --date 2026-05-19
nse-data reports --type sec_bhavdata --date 2026-05-19
nse-data reports --type ind_close_all --date 2026-05-19
nse-data reports --type market_activity --date 2026-05-19

# Download raw file
nse-data download --type cmvolt --date 2026-05-19 --out ./data
nse-data download --type security_master --date 2026-05-19 --out ./data
```

## All 20 Supported Report Types

Every report type returns a **pandas DataFrame** via `reports.get(type, date)`:

### Capital Market — Prices

| Type | Description | Format |
|------|-------------|--------|
| `pr` | Bhavcopy (PR) Daily Zip Bundle | ZIP→CSV |
| `sec_bhavdata_full` | Full Bhavcopy with Delivery Data | CSV |
| `bhav_udiff` | UDiFF Bhavcopy (ISIN-keyed, modern format) | ZIP→CSV |
| `sme` | SME Platform EOD Market Data | CSV |

### Capital Market — Indices

| Type | Description | Format |
|------|-------------|--------|
| `ind_close_all` | All Indices Daily Close (147+ indices OHLC) | CSV |
| `pe` | Index P/E, P/B & Dividend Yield | CSV |
| `reg_ind` | Regional Indices Daily | CSV |

### Capital Market — Activity & Deals

| Type | Description | Format |
|------|-------------|--------|
| `market_activity` | Market Activity Report (turnover, breadth) | CSV |
| `short_selling` | Short Selling Daily Report | CSV |

### Capital Market — Reference & Master

| Type | Description | Format |
|------|-------------|--------|
| `security_master` | NSE CM Security Master (ISIN, face value, lot) | GZIP→CSV |
| `cm_52wk` | 52-Week High/Low for all securities | CSV |

### Capital Market — Risk & Margin

| Type | Description | Format |
|------|-------------|--------|
| `cmvolt` | CM Security Volatility (annualized + daily) | CSV |
| `mto` | Multiple Trade Orders (delivery breakdown) | DAT |

### Derivatives — Equity F&O

| Type | Description | Format |
|------|-------------|--------|
| `fo_secban` | F&O Security Ban List | CSV |
| `fovolt` | F&O Volatility | CSV |
| `fo_sett` | F&O Settlement Prices | CSV |

### Derivatives — Commodity & Currency

| Type | Description | Format |
|------|-------------|--------|
| `co_volt` | Commodity Volatility | CSV |
| `x_volt` | Currency Volatility | CSV |
| `cd_sett` | Currency Derivatives Settlement Prices | CSV |
| `trm_bc` | Tri-Party Repo Bhavcopy | CSV |

## Source URLs

All data comes from `nsearchives.nseindia.com` (direct file downloads, no Cloudflare):

```
https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/content/indices/ind_close_all_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/archives/nsccl/volt/CMVOLT_{DDMMYYYY}.CSV
https://nsearchives.nseindia.com/archives/fo/sec_ban/fo_secban_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/content/cm/NSE_CM_security_{DDMMYYYY}.csv.gz
...
```

Date format for all functions: **`YYYY-MM-DD`** (e.g. `"2026-05-19"`)

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
