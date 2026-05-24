# indian-market-data

Download **NSE** and **MCX India** market data as pandas DataFrames — bhavcopy, Nifty indices, F&O, commodity spot prices. Works on **AWS Lambda**, **Snowflake**, and any cloud environment.

[![PyPI nse-data](https://img.shields.io/pypi/v/nse-data?label=nse-data)](https://pypi.org/project/nse-data/)
[![PyPI mcx-data](https://img.shields.io/pypi/v/mcx-data?label=mcx-data)](https://pypi.org/project/mcx-data/)
[![Python](https://img.shields.io/pypi/pyversions/nse-data)](https://pypi.org/project/nse-data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

```bash
pip install indian-market-data     # NSE + MCX together
pip install nse-data               # NSE only
pip install mcx-data               # MCX only
```

📖 **[Full Documentation](https://NikhilSuthar.github.io/indian-market-data)**

---

## Packages in this monorepo

| Package | PyPI | Datasets | Description |
|---------|------|----------|-------------|
| [`nse-data`](packages/nse-data/) | [↗](https://pypi.org/project/nse-data/) | 91 | NSE India — equities, F&O, debt, indices, EGR |
| [`mcx-data`](packages/mcx-data/) | [↗](https://pypi.org/project/mcx-data/) | 2 | MCX India — commodity spot prices |
| [`indian-market-data`](packages/indian-market-data/) | [↗](https://pypi.org/project/indian-market-data/) | All | Umbrella — installs both |

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

mcx.list_commodities()   # 28 commodities
```

---

## AWS Lambda

```bash
cd .lambda_layer
./build.sh      # builds layer with nse-data + mcx-data + pandas + curl-cffi
```

---

## Documentation

**[NikhilSuthar.github.io/indian-market-data](https://NikhilSuthar.github.io/indian-market-data)**

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
