---
layout: default
title: Installation
nav_order: 1
---

# Installation

## Option 1 — All packages together

```bash
pip install indian-market-data
```

Installs `nse-archives` + `bse-index-data` + `mcx-data` together.

## Option 2 — Individual packages

```bash
pip install nse-archives           # NSE only
pip install bse-index-data         # BSE only
pip install mcx-data               # MCX only
```

## Optional extras

```bash
# S3 upload support
pip install nse-archives[s3]
pip install mcx-data[s3]
pip install bse-index-data[s3]

# Cloudflare bypass (for niftyindices.com TRI)
pip install nse-archives[cloudflare]

# Polars output (optional — see below)
pip install nse-archives[polars]
pip install mcx-data[polars]
pip install bse-index-data[polars]
```

**Requirements:** Python 3.9+ | `requests` | `pandas` | `openpyxl`

**BSE + MCX additionally require:** `curl-cffi>=0.7.0` (installed automatically)

---

## Optional: Polars Output

All packages support **optional Polars output** with zero code changes — just set one environment variable before importing:

```python
import os
os.environ["IMD_DATAFRAME"] = "polars"   # must be set before importing

from nsedata import nse
from bsedata import bse
from mcxdata import mcx

df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
type(df)  # polars.DataFrame

df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")  # polars.DataFrame
df = mcx.get_spot_recent()                                  # polars.DataFrame
```

All internal logic stays in pandas. The conversion to polars happens only at the last step before returning to you.

Polars must be installed separately:
```bash
pip install nse-archives[polars]      # adds polars>=0.20.0
pip install mcx-data[polars]
pip install bse-index-data[polars]
```

Polars works on AWS Lambda — compatible Linux wheels, ~15 MB.

---

## Verify

```python
import nsedata, mcxdata, bsedata
print(nsedata.__version__)    # 1.1.0
print(mcxdata.__version__)    # 1.1.0
print(bsedata.__version__)    # 1.1.0

from nsedata import nse
from bsedata import bse
from mcxdata import mcx

nse.list_datasets()           # 91 NSE datasets
bse.list_indices()            # 55 BSE indices
mcx.list_datasets()           # 2 MCX datasets
```

---

## Lambda Layer

Includes `nse-archives` + `bse-index-data` + `mcx-data` + all dependencies:

```bash
cd .lambda_layer
./build.sh                   # standard (from PyPI)
./build.sh --dev             # from local source (development)
./build.sh --full            # + cloudscraper (TRI + extra WAF fallback)
```

Upload and attach to your Lambda function:

```bash
aws lambda publish-layer-version \
  --layer-name indian-market-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --description "nse-archives + bse-index-data + mcx-data + pandas + curl-cffi"
```
