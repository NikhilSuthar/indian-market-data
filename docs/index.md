---
layout: default
title: Home
nav_order: 1
---

# nse-data

**Python library to download market data from NSE India**

Download historical index data, daily bhavcopy, security-wise delivery data, and market activity reports — all as clean pandas DataFrames.

---

## Why nse-data?

NSE India does not provide a public REST API. Getting market data requires navigating multiple websites, handling Cloudflare protection, managing session cookies, and parsing inconsistent file formats.

`nse-data` handles all of that for you:

- **One-line data access** — get any NSE dataset as a pandas DataFrame
- **Cloudflare bypass** — automatically handles JS challenges on niftyindices.com
- **Session management** — cookie warming for nseindia.com
- **Clean output** — standardized column names, parsed dates, numeric types
- **CLI included** — download data from the terminal without writing Python

---

## Quick Install

```bash
pip install nse-data
```

## Quick Example

```python
from nsedata import indices, reports

# NIFTY 50 historical OHLC data
df = indices.get_historical("NIFTY 50", "01-Apr-2026", "15-May-2026")

# Daily bhavcopy with delivery data
df = reports.get_sec_bhavdata("2026-04-17")
```

---

## Data Sources

| Source | Website | Data |
|--------|---------|------|
| NSE Indices | [niftyindices.com](https://niftyindices.com/reports/historical-data) | Historical Price Index, Total Return Index |
| NSE Archives | [nsearchives.nseindia.com](https://www.nseindia.com/all-reports) | Bhavcopy, Security Bhavdata, Index Close, Market Activity |

---

## Supported Indices

All indices available on [niftyindices.com](https://niftyindices.com/reports/historical-data):

### Broad Market
- NIFTY 50, NIFTY NEXT 50, NIFTY 100, NIFTY 200, NIFTY 500, NIFTY MIDCAP 50, NIFTY MIDCAP 100

### Sectoral
- NIFTY BANK, NIFTY IT, NIFTY AUTO, NIFTY PHARMA, NIFTY FMCG, NIFTY METAL, NIFTY REALTY, NIFTY ENERGY, NIFTY INFRA, NIFTY PSE, NIFTY MEDIA

### Thematic
- NIFTY COMMODITIES, NIFTY CONSUMPTION, NIFTY CPSE, NIFTY FIN SERVICE, NIFTY GROWSECT 15, NIFTY100 QUALITY 30, NIFTY MIDCAP LIQ 15

### Fixed Income
- Nifty 8-13 yr G-Sec, Nifty 10 yr Benchmark G-Sec, Nifty 4-8 yr G-Sec Index

---

## Architecture

```
nse-data (PyPI package)
│
├── nsedata.indices     → niftyindices.com (Cloudflare-protected)
│   ├── get_historical()   Price Index OHLC
│   └── get_tri()          Total Return Index
│
├── nsedata.reports     → nsearchives.nseindia.com
│   ├── get_bhavcopy()        PR zip file
│   ├── get_sec_bhavdata()    Full security bhavcopy
│   ├── get_ind_close_all()   All index closing values
│   ├── get_market_activity() Market activity report
│   └── download_report()     Raw file download
│
└── nsedata.session     → Session management
    ├── create_niftyindices_session()  Cloudflare bypass
    └── create_nse_session()           Cookie warming
```

---

## Links

- **PyPI**: [pypi.org/project/nse-data](https://pypi.org/project/nse-data/)
- **GitHub**: [github.com/NikhilSuthar/nse-data](https://github.com/NikhilSuthar/nse-data)
- **Issues**: [github.com/NikhilSuthar/nse-data/issues](https://github.com/NikhilSuthar/nse-data/issues)
- **NSE India**: [nseindia.com](https://www.nseindia.com)
- **Nifty Indices**: [niftyindices.com](https://niftyindices.com)
