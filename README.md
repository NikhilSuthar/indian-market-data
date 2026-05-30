# indian-market-data

<p align="center">
  <img src="docs/assets/nse.jpg" alt="NSE India" height="80"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="docs/assets/BSE_logo.png" alt="BSE India" height="80"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="docs/assets/mcx.png" alt="MCX India" height="80"/>
</p>

<p align="center">
  Download <strong>NSE</strong>, <strong>BSE</strong> and <strong>MCX India</strong> market data as pandas DataFrames.<br/>
  Bhavcopy, SENSEX/Nifty indices, F&amp;O, commodity spot prices — direct from exchange archives.<br/>
  Works on <strong>AWS Lambda</strong>, <strong>Snowflake</strong>, and any cloud environment.
</p>

<p align="center">
  <a href="https://pypi.org/project/nse-archives/"><img src="https://img.shields.io/pypi/v/nse-archives?label=nse-archives" alt="nse-archives PyPI"/></a>
  <a href="https://pypi.org/project/bse-index-data/"><img src="https://img.shields.io/pypi/v/bse-index-data?label=bse-index-data" alt="bse-index-data PyPI"/></a>
  <a href="https://pypi.org/project/mcx-data/"><img src="https://img.shields.io/pypi/v/mcx-data?label=mcx-data" alt="mcx-data PyPI"/></a>
  <a href="https://pypi.org/project/indian-market-data/"><img src="https://img.shields.io/pypi/v/indian-market-data?label=indian-market-data" alt="indian-market-data PyPI"/></a>
  <a href="https://pypi.org/project/nse-archives/"><img src="https://img.shields.io/pypi/pyversions/nse-archives" alt="Python 3.9+"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"/></a>
</p>

```bash
pip install indian-market-data     # NSE + MCX together
pip install nse-archives           # NSE only
pip install bse-index-data         # BSE only
pip install mcx-data               # MCX only
```

📖 **[Full Documentation](https://NikhilSuthar.github.io/indian-market-data)**

---

## Packages in this monorepo

| Package | PyPI | Datasets | Description |
|---------|------|----------|-------------|
| [`nse-archives`](packages/nse-data/) | [↗](https://pypi.org/project/nse-archives/) | 91 | NSE India — equities, F&O, debt, indices, EGR |
| [`bse-index-data`](packages/bse-data/) | [↗](https://pypi.org/project/bse-index-data/) | 55+ indices | BSE India — SENSEX, BSE500, BANKEX and 50+ more |
| [`mcx-data`](packages/mcx-data/) | [↗](https://pypi.org/project/mcx-data/) | 2 | MCX India — commodity spot prices |
| [`indian-market-data`](packages/indian-market-data/) | [↗](https://pypi.org/project/indian-market-data/) | All | Umbrella — installs all |

---

## NSE — Quick Start

```python
from nsedata import nse

# Daily prices
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# F&O
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")
df = nse.get("derivatives", "equity", "fo_secban", "2026-05-22")

# Historical index + TRI (niftyindices.com)
df = nse.get_historical_index("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")

# Download to S3
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")

nse.list_datasets()   # 91 datasets
```

**86 datasets confirmed working** on Lambda (May 2026) — equities, F&O, debt, indices, IRD, SLB, EGR.

---

## BSE — Quick Start

```python
from bsedata import bse

# Historical SENSEX OHLC
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")

# Historical BSE500, BANKEX, BSEIT etc.
df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")
df = bse.get_index("BANKEX", "2026-01-01", "2026-05-22")

# All 120+ indices for one date (single call)
df = bse.get_all_indices("2026-05-22")

# Live SENSEX quote
df = bse.get_live_sensex()

# Download to S3
bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                   s3_bucket="my-bucket", s3_prefix="raw/bse/")

# List all 55 supported indices
bse.list_indices()
bse.list_indices(category="Sectoral")
```

**55 indices confirmed working** — Broad Market, Sectoral, Thematic, Strategy and Global.

---

## MCX — Quick Start

```python
from mcxdata import mcx

# Today's spot prices — all 28 commodities
df = mcx.get_spot_recent()

# Single commodity
df = mcx.get_spot_recent(commodity="GOLD")

# Historical
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="CRUDEOIL")

# Download to S3
mcx.download("spot", "market", "spot_recent",
             s3_bucket="my-bucket", s3_prefix="raw/mcx/")

mcx.list_commodities()   # 28 commodities: GOLD, SILVER, CRUDEOIL, ...
```

---

## AWS Lambda

```bash
cd .lambda_layer
./build.sh      # builds layer with nse-archives + mcx-data + pandas + curl-cffi
```

---

## Documentation

**[View Full Documentation →](https://NikhilSuthar.github.io/indian-market-data)**

| Page | Description |
|------|-------------|
| [NSE Equities & SME](https://NikhilSuthar.github.io/indian-market-data/capital-market) | 32 daily/monthly datasets |
| [NSE Indices](https://NikhilSuthar.github.io/indian-market-data/capital-market-indices) | Index closes, top movers |
| [NSE F&O](https://NikhilSuthar.github.io/indian-market-data/derivatives-equity) | F&O bhavcopy, contracts, ban list |
| [NSE Debt](https://NikhilSuthar.github.io/indian-market-data/debt-corporate) | Corporate bonds, settlements |
| [MCX Spot Market](https://NikhilSuthar.github.io/indian-market-data/mcx-spot) | Commodity spot prices (28 commodities) |

---

## License

MIT — data from [NSE India](https://www.nseindia.com) and [MCX India](https://www.mcxindia.com).
