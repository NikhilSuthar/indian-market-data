# Lambda Layer — indian-market-data

AWS Lambda layer containing `nse-archives` + `mcx-data` with all dependencies.

---

## Files in this folder

| File | Description |
|------|-------------|
| `build.sh` | Build script — creates `nse-data-lambda-layer.zip` |
| `nse_lambda.py` | Lambda function for NSE India data downloads |
| `mcx_lambda.py` | Lambda function for MCX India spot market data |
| `lambda_function.py` | Combined handler — NSE + MCX in one function |
| `download_all.py` | Local bulk download script (no Lambda needed) |
| `deploy.md` | Full AWS deployment guide with IAM, EventBridge etc. |

---

## Quick Start

### 1. Build the Layer

```bash
cd .lambda_layer
chmod +x build.sh

# Production — installs from PyPI (nse-archives + mcx-data)
./build.sh

# Development — installs from local source code
./build.sh --dev

# With cloudscraper (extra WAF fallback for TRI + MCX)
./build.sh --full
```

Output: `nse-data-lambda-layer.zip` (~37 MB)

### 2. Publish to AWS

```bash
aws lambda publish-layer-version \
  --layer-name indian-market-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --description "nse-archives + mcx-data + pandas + curl-cffi" \
  --region ap-south-1
```

Copy the `LayerVersionArn` from the response.

### 3. Attach to your Lambda function

```bash
aws lambda update-function-configuration \
  --function-name <YOUR_FUNCTION_NAME> \
  --layers <LAYER_VERSION_ARN> \
  --region ap-south-1
```

---

## Layer Contents

| Package | Purpose |
|---------|---------|
| `nse-archives` | NSE India data — 91 datasets |
| `mcx-data` | MCX India commodity spot prices |
| `pandas` | DataFrame processing |
| `numpy` | pandas dependency |
| `openpyxl` | Excel file parsing |
| `requests` | HTTP client |
| `curl-cffi` | Chrome TLS impersonation — bypasses MCX Akamai WAF |
| `cloudscraper` | JS challenge solver (optional, `--full` flag) |
| `boto3` | **NOT included** — Lambda runtime provides it |

> **Important:** `curl_cffi`'s `.dist-info` is preserved in the layer (unlike other packages). It reads its own metadata at import time to load native `.so` binaries. Do not delete it.

## Layer Size

| Build mode | Zipped | Unzipped |
|-----------|--------|----------|
| Standard (`./build.sh`) | ~37 MB | ~125 MB |
| With cloudscraper (`--full`) | ~42 MB | ~145 MB |

Lambda limit: 250 MB unzipped. Well within limits.

---

## Lambda Functions

### NSE — `nse_lambda.py`

Downloads NSE datasets to S3. Supports all 86 confirmed datasets, monthly datasets, VaR snapshots, and TRI from niftyindices.com.

```python
# handler: nse_lambda.lambda_handler
```

**Event examples:**

```json
// 5 default datasets (quick test)
{"date": "2026-05-22", "bucket": "my-bucket"}

// All 86 NSE datasets
{"date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket", "download_all": true}

// Specific datasets only
{"date": "2026-05-22", "bucket": "my-bucket",
 "datasets": [["capital_market", "equities_sme", "sec_bhavdata_full"],
              ["capital_market", "indices", "ind_close_all"]]}

// All NSE + TRI for 30 Nifty indices
{"date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket",
 "download_all": true, "test_tri": true,
 "tri_start": "01-May-2026", "tri_end": "22-May-2026"}
```

### MCX — `mcx_lambda.py`

Downloads MCX commodity spot prices to S3.

```python
# handler: mcx_lambda.lambda_handler
```

**Event examples:**

```json
// Today's spot prices — all 28 commodities
{"date": "2026-05-22", "bucket": "my-bucket", "mcx_spot": true}

// Historical archive — specific commodities
{"date": "2026-05-22", "bucket": "my-bucket",
 "mcx_archive": true, "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
 "mcx_commodities": ["GOLD", "SILVER", "CRUDEOIL"]}

// Historical archive — all 28 commodities
{"date": "2026-05-22", "bucket": "my-bucket",
 "mcx_archive": true, "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22"}
```

### Combined — `lambda_function.py`

Both NSE and MCX in a single Lambda function. Useful if you want one scheduled trigger to download everything.

```json
{
  "date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket",
  "download_all": true,
  "mcx_spot": true,
  "mcx_archive": true, "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
  "mcx_commodities": ["GOLD", "SILVER", "CRUDEOIL", "NATURALGAS"]
}
```

---

## S3 Output Structure

```
s3://my-bucket/nse-data/
├── Capital Market/
│   ├── Equities & SME/Daily/
│   │   ├── sec_bhavdata_full_22052026.csv
│   │   ├── CMVOLT_22052026.CSV
│   │   └── ...
│   └── Indices/Daily/
│       └── ind_close_all_22052026.csv
├── Derivatives/Equity Derivative/Daily/
│   └── fo_secban_22052026.csv
├── Debt/Corporate Segment/Daily/
└── niftyindices/tri/
    └── NIFTY_50_TRI_01-May-2026_to_22-May-2026.csv

s3://my-bucket/mcx-data/
├── Spot Market/Recent/
│   └── MCX_spot_recent_ALL_20260522.csv
└── Spot Market/Archive/
    ├── MCX_spot_archive_GOLD_20260501_20260522.csv
    └── MCX_spot_archive_SILVER_20260501_20260522.csv
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl_cffi not available` | Layer built without curl_cffi OR dist-info deleted | Rebuild with `build.sh`; ensure dist-info kept |
| `MCX session type: requests` | curl_cffi import failed | Check Lambda logs for the specific import error |
| NSE HTTP 404 | Non-trading day or file not published yet | NSE publishes after 6 PM IST on trading days |
| NSE HTTP 403 | Rate limiting | Lambda retries built-in; reduce parallel invocations |
| Timeout | All-datasets run takes ~5 min | Set timeout to 300s, memory to 512 MB |
| Memory error | `security_master` is 13 MB GZ | Set memory to 512 MB+ |

See [full deployment guide](deploy.md) for IAM setup, EventBridge scheduling, and more.
