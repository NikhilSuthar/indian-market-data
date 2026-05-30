---
layout: default
title: Home
nav_order: 1
---

# Indian Market Data

<p align="center">
  <img src="{{ '/assets/nse.jpg' | relative_url }}" alt="NSE India" width="160"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="{{ '/assets/BSE_logo.png' | relative_url }}" alt="BSE India" width="160"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="{{ '/assets/mcx.png' | relative_url }}" alt="MCX India" width="160"/>
</p>

<p align="center">
  Download <strong>NSE</strong>, <strong>BSE</strong> and <strong>MCX India</strong> market data as pandas DataFrames.<br/>
  Bhavcopy · Nifty/Sensex indices · F&amp;O · Commodity spot prices<br/>
  Works on <strong>AWS Lambda</strong>, Snowflake, and any cloud environment.
</p>

---

## Packages

| Package | PyPI | Datasets | Exchange |
|---------|------|----------|----------|
| `nse-archives` | [↗](https://pypi.org/project/nse-archives/) | 91 | NSE India — equities, F&O, debt, indices, EGR |
| `bse-index-data` | [↗](https://pypi.org/project/bse-index-data/) | 55+ indices | BSE India — SENSEX, BSE500, BANKEX and 50+ more |
| `mcx-data` | [↗](https://pypi.org/project/mcx-data/) | 2 | MCX India — commodity spot prices |
| `indian-market-data` | [↗](https://pypi.org/project/indian-market-data/) | All | Umbrella — installs all |

```bash
pip install indian-market-data     # NSE + MCX together
pip install nse-archives           # NSE only
pip install bse-index-data         # BSE only
pip install mcx-data               # MCX only
```

---

## NSE Quick Start

```python
from nsedata import nse

# Daily prices
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# F&O
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

# Download to S3 (Lambda with IAM role)
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")
```

→ [Full NSE documentation]({{ site.baseurl }}/nse)

---

## BSE Quick Start

```python
from bsedata import bse

# Historical SENSEX OHLC
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")

# All 120+ indices for one date
df = bse.get_all_indices("2026-05-22")

# Live SENSEX quote
df = bse.get_live_sensex()

# Download to S3
bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                   s3_bucket="my-bucket", s3_prefix="raw/bse/")
```

→ [Full BSE documentation]({{ site.baseurl }}/bse)

---

## MCX Quick Start

```python
from mcxdata import mcx

# Today's spot prices — all 28 commodities
df = mcx.get_spot_recent()

# Historical archive — must specify commodity
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
```

→ [Full MCX documentation]({{ site.baseurl }}/mcx)

---

## AWS Lambda

All packages run on Lambda. A pre-built layer script is included:

```bash
cd .lambda_layer && ./build.sh
```

→ [Lambda deployment guide]({{ site.baseurl }}/lambda)

---

## NSE Dataset Status (May 2026)

| Status | Count |
|--------|-------|
| ✅ DataFrame + Download | 59 |
| ⬇️ Download only | 8 |
| 🕐 T-1 (previous trading day) | 16 |
| ⏭ Portal-only | 8 |

---

## BSE Datasets

| Dataset | Description | Status |
|---------|-------------|--------|
| `get_index(name, from, to)` | Historical OHLC for any of 55 registered indices | ✅ |
| `get_all_indices(date)` | All 120+ indices for one date (single call) | ✅ |
| `get_live_sensex()` | Real-time SENSEX quote | ✅ |

---

## MCX Datasets

| Dataset | Description | Status |
|---------|-------------|--------|
| `spot_recent` | Today's spot prices — all 28 commodities | ✅ |
| `spot_archive` | Historical by commodity + date range | ✅ |

---

## License

MIT — data from [NSE India](https://www.nseindia.com), [BSE India](https://www.bseindia.com) and [MCX India](https://www.mcxindia.com).
