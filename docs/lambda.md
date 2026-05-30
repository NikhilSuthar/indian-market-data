---
layout: default
title: AWS Lambda
nav_order: 5
has_children: true
permalink: /lambda
---

# AWS Lambda

All three packages — `nse-archives`, `bse-index-data` and `mcx-data` — are designed to run on AWS Lambda. A pre-built layer script is included in the repository.Both `nse-archives` and `mcx-data` are designed to run on AWS Lambda. A pre-built layer script is included in the repository.

```bash
cd .lambda_layer
./build.sh          # installs from PyPI — production
./build.sh --dev    # installs from local source — development
```

Output: `nse-data-lambda-layer.zip` (~37 MB)

---

## Architecture

```
EventBridge (daily cron)
       │
       ▼
  Lambda Function
  ├── nse_lambda.py   → NSE datasets → S3
  └── mcx_lambda.py   → MCX spot prices → S3
       │
       ▼
  S3 (raw zone) → Snowflake
```

---

## Quick Test Events

```json
// NSE defaults (5 datasets)
{"date": "2026-05-22", "bucket": "my-bucket"}

// MCX spot prices
{"date": "2026-05-22", "bucket": "my-bucket", "mcx_spot": true}
```

See the [Deploy Guide]({{ site.baseurl }}/lambda/deploy) for full setup.
