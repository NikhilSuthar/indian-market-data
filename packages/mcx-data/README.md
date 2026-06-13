# mcx-data

<p align="center">
  <img src="https://raw.githubusercontent.com/NikhilSuthar/indian-market-data/main/docs/assets/mcx.png" alt="MCX India" height="55"/>
</p>

<p align="center">
  Download <strong>MCX India</strong> commodity spot market data as pandas DataFrames.<br/>
  28 commodities — GOLD, SILVER, CRUDEOIL, NATURALGAS and more.<br/>
  Works on <strong>AWS Lambda</strong> via Chrome TLS impersonation (bypasses Akamai WAF).
</p>

[![PyPI version](https://badge.fury.io/py/mcx-data.svg)](https://pypi.org/project/mcx-data/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Download **MCX India** commodity spot market data as pandas DataFrames. Works from **AWS Lambda** and any cloud environment.

**Full Documentation → [NikhilSuthar.github.io/indian-market-data/mcx-spot](https://NikhilSuthar.github.io/indian-market-data/mcx-spot)**

Part of the [indian-market-data](https://github.com/NikhilSuthar/indian-market-data) monorepo — also see [`nse-archives`](https://pypi.org/project/nse-archives/).

```bash
pip install mcx-data
```

## Quick Start

```python
from mcxdata import mcx

# Today's spot prices — all 28 commodities
df = mcx.get_spot_recent()

# Single commodity
df = mcx.get_spot_recent(commodity="GOLD")

# Historical (requires specific commodity)
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="SILVER")

# Download to S3
mcx.download("spot", "market", "spot_recent",
             s3_bucket="my-bucket", s3_prefix="raw/mcx/")

# Available commodities (28)
mcx.list_commodities()
```

## Datasets

| Dataset | Description | Date Param |
|---------|-------------|-----------|
| `spot_recent` | Today's spot prices — all 28 commodities | None |
| `spot_archive` | Historical spot prices by commodity + date range | `from_date`, `to_date` |

## Available Commodities (28)

`ALUMINI, ALUMINIUM, CARDAMOM, COPPER, COTTON, COTTONOIL, CPO, CRUDEOIL, CRUDEOILM, ELECDMBL, GOLD, GOLDGUINEA, GOLDM, GOLDPETAL, GOLDTEN, KAPAS, LEAD, LEADMINI, MENTHAOIL, NATGASMINI, NATURALGAS, NICKEL, SILVER, SILVERM, SILVERMIC, STEELREBAR, ZINC, ZINCMINI`

## Notes

- MCX archive requires a **specific commodity** — `"ALL"` returns empty (MCX API limitation)
- Uses `curl-cffi` Chrome TLS impersonation to bypass MCX Akamai WAF
- Lambda IPs are generally unblocked — works reliably on AWS

## Polars output (optional)

By default every function returns a **pandas** DataFrame. To get **polars**
DataFrames instead, install the extra and set one environment variable before
importing — no code changes needed:

```bash
pip install mcx-data[polars]
```

```python
import os
os.environ["IMD_DATAFRAME"] = "polars"   # set before importing mcxdata

from mcxdata import mcx
df = mcx.get_spot_recent()
type(df)   # polars.DataFrame
```

All internal logic stays in pandas; conversion happens only at the final return
step. Leave `IMD_DATAFRAME` unset (or `=pandas`) for the default pandas output.

## License

MIT — data from [MCX India](https://www.mcxindia.com).
