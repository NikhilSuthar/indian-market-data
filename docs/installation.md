---
layout: default
title: Installation
nav_order: 13
---

# Installation

## Option 1 — Both NSE + MCX (recommended)

```bash
pip install indian-market-data
```

Installs `nse-data` + `mcx-data` together.

## Option 2 — NSE only

```bash
pip install nse-data

# With S3 support
pip install nse-data[s3]

# With Cloudflare bypass (for niftyindices.com TRI)
pip install nse-data[cloudflare]
```

## Option 3 — MCX only

```bash
pip install mcx-data

# With S3 support
pip install mcx-data[s3]
```

**Requirements:** Python 3.9+ | `requests` | `pandas` | `openpyxl`

**MCX additionally requires:** `curl-cffi>=0.7.0` (installed automatically)

---

## Verify

```python
import nsedata
print(nsedata.__version__)   # 0.9.1

import mcxdata
print(mcxdata.__version__)   # 0.1.0

from nsedata import nse
from mcxdata import mcx

nse.list_datasets()          # 91 NSE datasets
mcx.list_datasets()          # 2 MCX datasets
```

---

## Lambda Layer

Includes both `nse-data` and `mcx-data` + all dependencies:

```bash
cd .lambda_layer
./build.sh                   # standard
./build.sh --full            # + cloudscraper (TRI + MCX WAF extra fallback)
```

Upload and attach to your Lambda function:

```bash
aws lambda publish-layer-version \
  --layer-name indian-market-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --description "nse-data + mcx-data + pandas + curl-cffi"
```
