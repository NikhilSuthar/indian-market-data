# AWS Lambda Deployment Guide

Complete step-by-step guide to deploy `nse-archives` + `mcx-data` on AWS Lambda for automated daily downloads to S3.

---

## Architecture

```
EventBridge Scheduler (daily cron)
         │
         ▼
   AWS Lambda Function
   ├── nse_lambda.py   → NSE India datasets (86 confirmed)
   ├── mcx_lambda.py   → MCX commodity spot prices (28 commodities)
   └── lambda_function.py  (combined)
         │
         ├── Layer: indian-market-data
         │   ├── nse-archives + mcx-data
         │   ├── pandas, openpyxl, requests
         │   └── curl-cffi (Chrome TLS for MCX Akamai WAF)
         │
         ▼
   S3 Bucket (raw zone)
         │
         ▼
   Snowflake (via Snowpipe or COPY INTO)
```

---

## Prerequisites

- AWS CLI configured (`aws configure`)
- Python 3.12 + pip on Linux or WSL
- An S3 bucket already created

---

## Step 1 — Build the Layer

```bash
cd .lambda_layer
chmod +x build.sh

# Standard (uses PyPI releases — recommended for production)
./build.sh

# With cloudscraper (extra WAF fallback)
./build.sh --full

# Dev mode (uses local source code — for testing changes)
./build.sh --dev
```

---

## Step 2 — Publish Layer to AWS

```bash
aws lambda publish-layer-version \
  --layer-name indian-market-data \
  --zip-file fileb://.lambda_layer/nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --description "nse-archives + mcx-data + pandas + curl-cffi" \
  --region ap-south-1
```

Note the `LayerVersionArn` in the response — e.g.:
```
arn:aws:lambda:ap-south-1:123456789012:layer:indian-market-data:1
```

---

## Step 3 — Create IAM Role

```bash
# Create role
aws iam create-role \
  --role-name indian-market-data-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach basic Lambda execution (CloudWatch Logs)
aws iam attach-role-policy \
  --role-name indian-market-data-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Attach S3 write policy
aws iam put-role-policy \
  --role-name indian-market-data-lambda-role \
  --policy-name s3-write-market-data \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }]
  }'
```

Replace `YOUR-BUCKET-NAME` with your actual bucket name.

---

## Step 4 — Create Lambda Functions

You can create **one combined function** or **two separate functions** (recommended for independent scheduling).

### Option A — Separate NSE and MCX functions (recommended)

```bash
# Package NSE handler
zip nse_lambda.zip .lambda_layer/nse_lambda.py

aws lambda create-function \
  --function-name nse-india-downloader \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT_ID:role/indian-market-data-lambda-role \
  --handler nse_lambda.lambda_handler \
  --zip-file fileb://nse_lambda.zip \
  --timeout 300 \
  --memory-size 512 \
  --layers LAYER_VERSION_ARN \
  --environment "Variables={S3_BUCKET=YOUR-BUCKET-NAME,S3_PREFIX=nse-data/}" \
  --region ap-south-1
```

```bash
# Package MCX handler
zip mcx_lambda.zip .lambda_layer/mcx_lambda.py

aws lambda create-function \
  --function-name mcx-india-downloader \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT_ID:role/indian-market-data-lambda-role \
  --handler mcx_lambda.lambda_handler \
  --zip-file fileb://mcx_lambda.zip \
  --timeout 120 \
  --memory-size 256 \
  --layers LAYER_VERSION_ARN \
  --environment "Variables={S3_BUCKET=YOUR-BUCKET-NAME,MCX_S3_PREFIX=mcx-data/}" \
  --region ap-south-1
```

### Option B — Single combined function

```bash
zip lambda_function.zip .lambda_layer/lambda_function.py

aws lambda create-function \
  --function-name indian-market-data-downloader \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT_ID:role/indian-market-data-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 300 \
  --memory-size 512 \
  --layers LAYER_VERSION_ARN \
  --environment "Variables={S3_BUCKET=YOUR-BUCKET-NAME}" \
  --region ap-south-1
```

---

## Step 5 — Schedule with EventBridge

NSE publishes data after 6 PM IST (12:30 UTC). MCX polls twice daily.

```bash
# NSE — daily at 6:30 PM IST (1:00 PM UTC), Mon–Fri
aws events put-rule \
  --name nse-daily-download \
  --schedule-expression "cron(0 13 ? * MON-FRI *)" \
  --description "Download NSE reports after market close" \
  --region ap-south-1

# MCX — daily at 7 PM IST (1:30 PM UTC), Mon–Sat
aws events put-rule \
  --name mcx-daily-download \
  --schedule-expression "cron(30 13 ? * MON-SAT *)" \
  --description "Download MCX spot prices" \
  --region ap-south-1
```

Add Lambda targets:

```bash
# NSE target
aws events put-targets \
  --rule nse-daily-download \
  --targets '[{
    "Id": "nse-lambda",
    "Arn": "arn:aws:lambda:ap-south-1:ACCOUNT_ID:function:nse-india-downloader",
    "Input": "{\"date\": \"<REPLACE_WITH_DATE>\", \"download_all\": true}"
  }]' \
  --region ap-south-1

# MCX target
aws events put-targets \
  --rule mcx-daily-download \
  --targets '[{
    "Id": "mcx-lambda",
    "Arn": "arn:aws:lambda:ap-south-1:ACCOUNT_ID:function:mcx-india-downloader",
    "Input": "{\"date\": \"<REPLACE_WITH_DATE>\", \"mcx_spot\": true}"
  }]' \
  --region ap-south-1
```

> **Tip:** For dynamic date, modify the Lambda to use `datetime.today().strftime("%Y-%m-%d")` when `event.get("date")` is missing.

Grant EventBridge permission to invoke:

```bash
aws lambda add-permission \
  --function-name nse-india-downloader \
  --statement-id eventbridge-nse-daily \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:ap-south-1:ACCOUNT_ID:rule/nse-daily-download

aws lambda add-permission \
  --function-name mcx-india-downloader \
  --statement-id eventbridge-mcx-daily \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:ap-south-1:ACCOUNT_ID:rule/mcx-daily-download
```

---

## Step 6 — Test Manually

```bash
# Test NSE (5 default datasets)
aws lambda invoke \
  --function-name nse-india-downloader \
  --payload '{"date": "2026-05-22", "bucket": "YOUR-BUCKET"}' \
  --region ap-south-1 \
  response.json && cat response.json

# Test MCX (today's spot + GOLD archive)
aws lambda invoke \
  --function-name mcx-india-downloader \
  --payload '{"date": "2026-05-22", "bucket": "YOUR-BUCKET",
              "mcx_spot": true, "mcx_archive": true,
              "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
              "mcx_commodities": ["GOLD", "SILVER"]}' \
  --region ap-south-1 \
  response.json && cat response.json
```

---

## Update Layer (after new release)

```bash
# 1. Rebuild
cd .lambda_layer
./build.sh

# 2. Publish new layer version
aws lambda publish-layer-version \
  --layer-name indian-market-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --region ap-south-1

# 3. Update function to use new layer version
aws lambda update-function-configuration \
  --function-name nse-india-downloader \
  --layers <NEW_LAYER_VERSION_ARN> \
  --region ap-south-1

aws lambda update-function-configuration \
  --function-name mcx-india-downloader \
  --layers <NEW_LAYER_VERSION_ARN> \
  --region ap-south-1
```

---

## Recommended Settings

| Setting | NSE function | MCX function |
|---------|-------------|-------------|
| Memory | 512 MB | 256 MB |
| Timeout | 300 s | 120 s |
| Runtime | python3.12 | python3.12 |
| Trigger | EventBridge Mon–Fri 6:30 PM IST | EventBridge Mon–Sat 7 PM IST |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl_cffi not available` | Layer missing dist-info | Rebuild with `build.sh` (dist-info fix included) |
| `MCX session type: requests` | curl_cffi import failed | Check CloudWatch logs for exact error |
| MCX HTTP 403 | Akamai WAF block | Ensure `curl_cffi` in layer; use `--full` for cloudscraper fallback |
| NSE HTTP 404 | Non-trading day or early invocation | Add logic to skip holidays; NSE publishes after 6 PM IST |
| NSE HTTP 403 | Rate limiting | Built-in 0.3s delay; reduce parallel runs |
| Lambda timeout | `download_all` on all 86 datasets | Set timeout to 300s |
| Out of memory | `security_master` is 13 MB GZ | Set memory to 512 MB+ |
| `slb_transaction_data` 404 | Month-end file — published in next month | Expected; file appears ~1st of following month |
