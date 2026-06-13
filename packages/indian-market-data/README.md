# indian-market-data

<p align="center">
  <img src="https://raw.githubusercontent.com/NikhilSuthar/indian-market-data/main/docs/assets/nse.jpg" alt="NSE India" height="55"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/NikhilSuthar/indian-market-data/main/docs/assets/mcx.png" alt="MCX India" height="55"/>
</p>

<p align="center">
  Download <strong>NSE</strong> and <strong>MCX India</strong> market data as pandas DataFrames.<br/>
  Bhavcopy · Nifty indices · F&amp;O · Commodity spot prices · Works on AWS Lambda
</p>

[![PyPI](https://img.shields.io/pypi/v/indian-market-data)](https://pypi.org/project/indian-market-data/)
[![Python](https://img.shields.io/pypi/pyversions/indian-market-data)](https://pypi.org/project/indian-market-data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

```bash
pip install indian-market-data
```

---

## What's included

| Package | Datasets | Exchange | Description |
|---------|----------|----------|-------------|
| `nse-data` | 91 | NSE India | Equities, F&O, debt, indices, EGR |
| `mcx-data` | 2 | MCX India | Commodity spot prices (recent + archive) |

Install individually or together:

```bash
pip install nse-archives            # NSE only
pip install mcx-data            # MCX only
pip install indian-market-data  # Both
```

---

## NSE — Quick Start

```python
from nsedata import nse
# or: from indianmarketdata import nse

# Daily prices
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# F&O
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")
df = nse.get("derivatives", "equity", "fo_secban", "2026-05-22")

# Debt
df = nse.get("debt", "corporate", "cbm_trd", "2026-05-22")

# Historical index + TRI (from niftyindices.com)
df = nse.get_historical_index("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")

# Download to S3
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")

# 91 datasets across equities, F&O, debt, indices, EGR
nse.list_datasets()
```

**86 datasets confirmed working** on AWS Lambda (May 2026). Covers:
- Capital Market: Equities & SME (32), Indices (2), Mutual Fund (1), SLB (12)
- Derivatives: Equity F&O (8), Commodity (3), Currency (3), Interest Rate (9)
- Debt: Corporate (15), Debt Segment (4), Tri-Party Repo (1)
- EGR (1)

---

## MCX — Quick Start

```python
from mcxdata import mcx
# or: from indianmarketdata import mcx

# Today's spot prices — all 28 commodities
df = mcx.get_spot_recent()
# → Commodity, Unit, Location, Spot Price (Rs.), Up/Down, Date

# Single commodity
df = mcx.get_spot_recent(commodity="GOLD")

# Historical (requires specific commodity — ALL not supported by MCX)
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="SILVER")
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="CRUDEOIL")

# Download to S3
mcx.download("spot", "market", "spot_recent",
             s3_bucket="my-bucket", s3_prefix="raw/mcx/")

# Available commodities (28 total)
mcx.list_commodities()
# → ['ALUMINI', 'ALUMINIUM', 'CARDAMOM', 'COPPER', 'COTTON', 'COTTONOIL',
#    'CPO', 'CRUDEOIL', 'CRUDEOILM', 'ELECDMBL', 'GOLD', 'GOLDGUINEA',
#    'GOLDM', 'GOLDPETAL', 'GOLDTEN', 'KAPAS', 'LEAD', 'LEADMINI',
#    'MENTHAOIL', 'NATGASMINI', 'NATURALGAS', 'NICKEL', 'SILVER', 'SILVERM',
#    'SILVERMIC', 'STEELREBAR', 'ZINC', 'ZINCMINI']
```

---

## Combined Usage

```python
from indianmarketdata import nse, mcx

date = "2026-05-22"

# NSE equity prices
nse_df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", date)

# MCX gold spot
mcx_df = mcx.get_spot_recent(commodity="GOLD")

print(f"NSE: {len(nse_df)} securities")
print(f"MCX Gold: ₹{mcx_df['Spot Price (Rs.)'].iloc[0]:,.2f}/10g")
```

---

## AWS Lambda

Both packages are designed to work from Lambda:

```python
# lambda_function.py
import json
from nsedata import nse
from mcxdata import mcx

def lambda_handler(event, context):
    date = event["date"]

    # NSE bhav
    nse.download("capital_market", "equities_sme", "sec_bhavdata_full", date,
                 s3_bucket=event["bucket"], s3_prefix="nse/")

    # MCX gold
    mcx.download("spot", "market", "spot_archive",
                 from_date=date, to_date=date, commodity="GOLD",
                 s3_bucket=event["bucket"], s3_prefix="mcx/")

    return {"statusCode": 200}
```

Build the layer:

```bash
cd .lambda_layer
./build.sh          # nse-data + mcx-data + pandas + curl-cffi + openpyxl
```

---

## CLI

```bash
# NSE
nse-data --help
nse-data list

# MCX
mcx-data --help
mcx-data spot-recent --commodity GOLD
mcx-data spot-archive --from 01/05/2026 --to 22/05/2026 --commodity GOLD
```

---

## Documentation

Full docs at **[View Documentation →](https://NikhilSuthar.github.io/indian-market-data)**

---

## Polars output (optional)

By default every function returns a **pandas** DataFrame. To get **polars**
DataFrames instead, install the extra and set one environment variable before
importing — no code changes needed, and it applies to NSE, BSE and MCX alike:

```bash
pip install indian-market-data[polars]
```

```python
import os
os.environ["IMD_DATAFRAME"] = "polars"   # set before importing

from indianmarketdata import nse, bse, mcx
type(nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22"))  # polars.DataFrame
type(bse.get_index("SENSEX", "2026-01-01", "2026-05-22"))                            # polars.DataFrame
type(mcx.get_spot_recent())                                                          # polars.DataFrame
```

All internal logic stays in pandas; conversion happens only at the final return
step. Leave `IMD_DATAFRAME` unset (or `=pandas`) for the default pandas output.

---

## License

MIT — data sourced from [NSE India](https://www.nseindia.com) and [MCX India](https://www.mcxindia.com).
