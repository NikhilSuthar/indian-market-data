# bse-index-data

[![PyPI version](https://badge.fury.io/py/bse-index-data.svg)](https://pypi.org/project/bse-index-data/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <strong>BSE India market data as pandas DataFrames.</strong><br/>
  SENSEX, BSE500, BANKEX and 50+ indices — historical OHLC + live quotes.<br/>
  Works on <strong>AWS Lambda</strong> and any cloud environment.
</p>

```bash
pip install bse-index-data
```

Part of the [indian-market-data](https://github.com/NikhilSuthar/indian-market-data) monorepo.

---

## Quick Start

```python
from bsedata import bse

# Historical SENSEX OHLC
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")

# Historical BSE500
df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")

# All 120+ indices for one date (single API call)
df = bse.get_all_indices("2026-05-22")

# Live SENSEX quote
df = bse.get_live_sensex()

# Download to S3 (Lambda with IAM role)
bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                   s3_bucket="my-bucket", s3_prefix="raw/bse/")

# List all 55 supported indices
bse.list_indices()
bse.list_indices(category="Sectoral")
```

## Supported Indices (55)

| Category | Indices |
|----------|---------|
| Broad Market | SENSEX, SENSEX50, SENSEXNXT50, BSE100, BSE200, BSE500, BSEALLCAP, BSEMIDCAP, BSESMALLCAP, BSE150MIDCAP, BSE250SMALLCAP, BSE400MIDSMALLCAP, BSE250LARGEMIDCAP, BSEMIDCAPSELECT, BSESMALLCAPSELECT, BSELARGECAP |
| Sectoral | BANKEX, BSEAUTO, BSECG, BSECD, BSECDGS, BSEENERGY, BSEFMCG, BSEFINANCE, BSEHC, BSEIT, BSEINDUSTRIALS, BSEMETAL, BSEOILGAS, BSEPOWER, BSEPRIVATEBANKS, BSEPSU, BSEREALTY, BSESERVICES, BSETECK, BSETELECOM, BSEUTILS |
| Thematic | BSECPSE, BSEIPO, BSESMEIPO, BSEGREENEX, BSECARBONEX, BSEINFRA, BSEMANUFACTURING, BHARAT22 |
| Strategy | BSEMOMENTUM, BSEQUALITY, BSEVALUE, BSELOWVOL, BSEDIVSTAB, BSE100ESG |
| Global | DOLLEX30, DOLLEX100, DOLLEX200 |

## CLI

```bash
bse-index-data list
bse-index-data list --category Sectoral
bse-index-data index --name SENSEX --from 2026-01-01 --to 2026-05-22
bse-index-data all-indices --date 2026-05-22
bse-index-data live
```

## Polars output (optional)

By default every function returns a **pandas** DataFrame. To get **polars**
DataFrames instead, install the extra and set one environment variable before
importing — no code changes needed:

```bash
pip install bse-index-data[polars]
```

```python
import os
os.environ["IMD_DATAFRAME"] = "polars"   # set before importing bsedata

from bsedata import bse
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")
type(df)   # polars.DataFrame
```

All internal logic stays in pandas; conversion happens only at the final return
step. Leave `IMD_DATAFRAME` unset (or `=pandas`) for the default pandas output.

## License

MIT — data from [BSE India](https://www.bseindia.com).
