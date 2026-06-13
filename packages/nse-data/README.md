# nse-archives

<p align="center">
  <img src="https://raw.githubusercontent.com/NikhilSuthar/indian-market-data/main/docs/assets/nse.jpg" alt="NSE India" height="55"/>
</p>

<p align="center">
  Download <strong>NSE India</strong> market data as pandas DataFrames.<br/>
  91 datasets — bhavcopy, Nifty indices, F&amp;O, debt, SLB, IRD, EGR.<br/>
  Works on <strong>AWS Lambda</strong> and Snowflake.
</p>

[![PyPI version](https://badge.fury.io/py/nse-archives.svg)](https://pypi.org/project/nse-archives/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Download NSE India market data as **pandas DataFrames** or raw files to **local disk / S3**. Works from AWS Lambda, Snowflake, or any cloud environment.

**Full Documentation → [NikhilSuthar.github.io/indian-market-data](https://NikhilSuthar.github.io/indian-market-data)**

Part of the [indian-market-data](https://github.com/NikhilSuthar/indian-market-data) monorepo — also see [`mcx-data`](https://pypi.org/project/mcx-data/).

---

## Installation

```bash
pip install nse-archives

# With S3 support
pip install nse-archives[s3]
```

## Quick Start

```python
from nsedata import nse

# Get any dataset as a DataFrame
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices",      "ind_close_all",     "2026-05-22")
df = nse.get("derivatives",    "equity",        "fo_bhav_udiff",     "2026-05-22")
df = nse.get("debt",           "tri_party_repo","trm_bc",            "2026-05-22")

# Download raw file to disk
nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22",
             output_dir="./data")

# Download to S3 (uses IAM role — no credentials needed)
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")

# List all 91 supported datasets
nse.list_datasets()
nse.list_datasets(category="capital_market")
```

## API

```
nse.get(category, subcategory, dataset, date, **kwargs)  → DataFrame
nse.download(category, subcategory, dataset, date, ...)  → path or s3://uri
nse.list_datasets(category=None, subcategory=None)       → DataFrame
nse.get_config_info(category, subcategory, dataset)      → dict
```

## CLI

```bash
# Get data as CSV
nse-data get capital_market equities_sme sec_bhavdata_full 2026-05-22
nse-data get capital_market indices ind_close_all 2026-05-22
nse-data get derivatives equity fo_bhav_udiff 2026-05-22

# Download raw file
nse-data dl capital_market equities_sme bhavcopy_pr 2026-05-22 --out ./data
nse-data dl capital_market equities_sme cvar1 2026-05-22 --out ./data --snapshot 1

# List datasets
nse-data list
nse-data list --category capital_market
nse-data list --category derivatives --subcategory equity

# Dataset info
nse-data info capital_market equities_sme sec_bhavdata_full
```

## Dataset Categories

| Category | Subcategory | Datasets | Docs |
|----------|-------------|----------|------|
| `capital_market` | `equities_sme` | 26 | [→ Capital Market](https://NikhilSuthar.github.io/nse-data/capital-market) |
| `capital_market` | `indices` | 2 | [→ Indices](https://NikhilSuthar.github.io/nse-data/capital-market-indices) |
| `capital_market` | `mutual_fund` | 1 | [→ Mutual Fund](https://NikhilSuthar.github.io/nse-data/capital-market-mf) |
| `capital_market` | `slb` | 10 | [→ SLB](https://NikhilSuthar.github.io/nse-data/capital-market-slb) |
| `derivatives` | `equity` | 8 | [→ Equity F&O](https://NikhilSuthar.github.io/nse-data/derivatives-equity) |
| `derivatives` | `commodity` | 3 | [→ Commodity](https://NikhilSuthar.github.io/nse-data/derivatives-commodity) |
| `derivatives` | `currency` | 3 | [→ Currency](https://NikhilSuthar.github.io/nse-data/derivatives-currency) |
| `derivatives` | `interest_rate` | 9 | [→ Interest Rate](https://NikhilSuthar.github.io/nse-data/derivatives-ird) |
| `debt` | `corporate` | 13 | [→ Debt Corporate](https://NikhilSuthar.github.io/nse-data/debt-corporate) |
| `debt` | `debt_segment` | 4 | [→ Debt Segment](https://NikhilSuthar.github.io/nse-data/debt-segment) |
| `debt` | `tri_party_repo` | 1 | [→ Tri-Party Repo](https://NikhilSuthar.github.io/nse-data/debt-trm) |
| `egr` | `egr` | 1 | [→ EGR](https://NikhilSuthar.github.io/nse-data/egr) |

**Total: 91 datasets | 83 return DataFrame | 8 download-only**

## Notes

- Data source: `nsearchives.nseindia.com` — no Cloudflare, works from any IP
- Only available on **trading days** — weekends and [NSE holidays](https://www.nseindia.com/resources/exchange-communication-holidays) return HTTP 404
- Date format: `YYYY-MM-DD` for daily, `YYYY-MM` for monthly datasets
- S3 upload uses IAM role — install `pip install nse-archives[s3]` for boto3

## Polars output (optional)

By default every function returns a **pandas** DataFrame. To get **polars**
DataFrames instead, install the extra and set one environment variable before
importing — no code changes needed:

```bash
pip install nse-archives[polars]
```

```python
import os
os.environ["IMD_DATAFRAME"] = "polars"   # set before importing nsedata

from nsedata import nse
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
type(df)   # polars.DataFrame
```

All internal logic stays in pandas; conversion happens only at the final return
step. Leave `IMD_DATAFRAME` unset (or `=pandas`) for the default pandas output.

## License

MIT — see [LICENSE](LICENSE)
