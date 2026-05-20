# nse-data

[![PyPI version](https://badge.fury.io/py/nse-data.svg)](https://pypi.org/project/nse-data/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library to download market data from NSE India — indices, bhavcopy, and daily reports.

**Documentation:** [NikhilSuthar.github.io/nse-data](https://NikhilSuthar.github.io/nse-data)

## Data Sources

| Source | Website | Data Available |
|--------|---------|----------------|
| NSE Indices | [niftyindices.com](https://niftyindices.com/reports/historical-data) | Historical Price Index (OHLC), Total Return Index |
| NSE Archives | [nsearchives.nseindia.com](https://www.nseindia.com/all-reports) | Bhavcopy, Security Bhavdata, Index Close, Market Activity |

## Installation

```bash
pip install nse-data
```

Or install from source:

```bash
git clone https://github.com/NikhilSuthar/nse-data.git
cd nse-data
pip install -e .
```

## Quick Start

### Python API

```python
from nsedata import indices, reports

# Historical Price Index (OHLC)
df = indices.get_historical("NIFTY 50", "01-Apr-2026", "15-May-2026")

# Total Return Index
df = indices.get_tri("NIFTY 50", "01-Apr-2026", "15-May-2026")

# Daily Bhavcopy (PR file)
df = reports.get_bhavcopy("2026-04-17")

# Full security-wise bhavcopy with delivery data
df = reports.get_sec_bhavdata("2026-04-17")

# All index closing values for a date
df = reports.get_ind_close_all("2026-04-17")

# Market Activity report
df = reports.get_market_activity("2026-04-17")

# Download raw file to disk
from nsedata.reports import download_report
path = download_report("sec_bhavdata_full", "2026-04-17", output_dir="./data")
```

### Command Line

```bash
# Historical index data
nse-data indices --index "NIFTY 50" --from "01-Apr-2026" --to "15-May-2026"

# Total Return Index
nse-data indices --index "NIFTY 50" --type tri --from "01-Apr-2026" --to "15-May-2026"

# Daily reports
nse-data reports --type bhavcopy --date 2026-04-17
nse-data reports --type sec_bhavdata --date 2026-04-17
nse-data reports --type ind_close_all --date 2026-04-17
nse-data reports --type market_activity --date 2026-04-17
```

## Sample Output

See the [`samples/`](samples/) folder for example CSV files showing what each command produces:

```
samples/
├── indices/
│   ├── NIFTY_50_price_01-Apr-2026_to_15-Apr-2026.csv
│   └── NIFTY_50_TRI_01-Apr-2026_to_15-Apr-2026.csv
└── reports/
    ├── bhavcopy_2026-04-17.csv
    ├── sec_bhavdata_full_2026-04-17.csv
    ├── ind_close_all_2026-04-17.csv
    └── market_activity_2026-04-17.csv
```

## Available Data

### Indices (`nsedata.indices`)

| Function | Description | Columns |
|----------|-------------|---------|
| `get_historical(index, start, end)` | Price Index OHLC | Index Name, Date, Open, High, Low, Close |
| `get_tri(index, start, end)` | Total Return Index | Index Name, Date, Total Returns Index, Net Total Return Index |

**Supported indices** — all indices on [niftyindices.com](https://niftyindices.com/reports/historical-data):
- **Broad Market:** NIFTY 50, NIFTY 100, NIFTY 200, NIFTY 500, NIFTY MIDCAP 50, NIFTY NEXT 50
- **Sectoral:** NIFTY BANK, NIFTY IT, NIFTY AUTO, NIFTY PHARMA, NIFTY FMCG, NIFTY METAL, NIFTY ENERGY
- **Thematic:** NIFTY COMMODITIES, NIFTY CONSUMPTION, NIFTY FIN SERVICE, NIFTY100 QUALITY 30
- **Fixed Income:** Nifty 8-13 yr G-Sec, Nifty 10 yr Benchmark G-Sec

Date format: `dd-Mon-yyyy` (e.g. `01-Apr-2026`, `15-May-2026`)

### Reports (`nsedata.reports`)

| Function | Description | Source URL Pattern |
|----------|-------------|-------------------|
| `get_bhavcopy(date)` | Price Record (PR zip) | `nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip` |
| `get_sec_bhavdata(date)` | Full bhavcopy with delivery | `nsearchives.nseindia.com/products/content/sec_bhavdata_full_{ddmmyyyy}.csv` |
| `get_ind_close_all(date)` | All index closing values | `nsearchives.nseindia.com/content/indices/ind_close_all_{ddmmyyyy}.csv` |
| `get_market_activity(date)` | Market activity summary | `nsearchives.nseindia.com/archives/equities/market-activity/MA{ddmmyy}.csv` |
| `download_report(type, date, dir)` | Download raw file | Any of the above |

Date format: `YYYY-MM-DD` (e.g. `2026-04-17`)

## Full Dataset Catalog (79 datasets)

This package aims to support **all 79 downloadable datasets** from NSE India. See the [complete catalog](https://NikhilSuthar.github.io/nse-data/datasets) for the full list with commands.

**Currently implemented (v0.1.0):** Bhavcopy, sec_bhavdata_full, ind_close_all, Market Activity, Historical Indices (Price + TRI)

**Planned (v0.2.0+):** UDiFF Bhavcopy, Security Master, CMVOLT, Short Selling, F&O data, Commodity, Currency derivatives, and more.

## Important Notes

- This library uses **web scraping** (not official APIs). NSE does not provide a public REST API.
- `niftyindices.com` is behind **Cloudflare** — we use `cloudscraper` to bypass JS challenges.
- URL patterns and response formats may change without notice. Pin your version.
- No retry logic built-in yet — add your own for production use.
- NSE may rate-limit or block IPs making too many requests.
- Data is only available for **trading days**. Weekends and [NSE holidays](https://www.nseindia.com/resources/exchange-communication-holidays) will return errors.

## Dependencies

| Package | Purpose |
|---------|---------|
| [requests](https://docs.python-requests.org/) | HTTP client for NSE India |
| [pandas](https://pandas.pydata.org/) | Data manipulation and DataFrame output |
| [cloudscraper](https://github.com/VeNoMouS/cloudscraper) | Cloudflare bypass for niftyindices.com |

## Project Structure

```
nse-data/
├── src/nsedata/          ← Package source (import as: from nsedata import ...)
│   ├── __init__.py
│   ├── indices.py        ← Historical index data from niftyindices.com
│   ├── reports.py        ← Daily reports from nsearchives.nseindia.com
│   ├── session.py        ← HTTP session management
│   └── cli.py            ← CLI entry point
├── samples/              ← Example output files
├── docs/                 ← GitHub Pages documentation
├── pyproject.toml        ← Package metadata & build config
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Contributing

```bash
git clone https://github.com/NikhilSuthar/nse-data.git
cd nse-data
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/
```

## License

MIT — see [LICENSE](LICENSE) for details.
