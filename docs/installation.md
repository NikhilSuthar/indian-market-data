---
layout: default
title: Installation
nav_order: 13
---

# Installation

```bash
pip install nse-data

# With S3 support (adds boto3)
pip install nse-data[s3]
```

**Requirements:** Python 3.9+ | `requests` | `pandas`

## Verify

```python
import nsedata
print(nsedata.__version__)  # 0.5.0

from nsedata import nse
nse.list_datasets()
```

## Lambda Layer

```bash
cd .lambda_layer
./build.sh
aws lambda publish-layer-version \
  --layer-name nse-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13
```

See [deploy guide](.lambda_layer/deploy.md) for full Lambda setup.
