# Lambda Deployment Guide

Complete setup to run `nse-data` on AWS Lambda.

## Architecture

```
EventBridge (daily cron) → Lambda → NSE Archives → S3 Bucket
                              ↓
                         nse-data layer
                       (pandas + requests)
```

## Step 1: Upload Lambda Layer

```bash
cd .lambda_layer
./build.sh

# Upload layer
aws lambda publish-layer-version \
  --layer-name nse-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --description "nse-data library with pandas and requests" \
  --region ap-south-1
```

Save the returned `LayerVersionArn`.

## Step 2: Create IAM Role

```bash
# Create role
aws iam create-role \
  --role-name nse-data-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach basic Lambda execution
aws iam attach-role-policy \
  --role-name nse-data-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Attach S3 write (create inline policy)
aws iam put-role-policy \
  --role-name nse-data-lambda-role \
  --policy-name nse-data-s3-write \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/nse-data/*"
    }]
  }'
```

## Step 3: Create Lambda Function

```bash
# Zip the handler
zip lambda_function.zip lambda_function.py

# Create function
aws lambda create-function \
  --function-name nse-data-downloader \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT_ID:role/nse-data-lambda-role \
  --handler lambda_function.handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 300 \
  --memory-size 512 \
  --layers arn:aws:lambda:ap-south-1:ACCOUNT_ID:layer:nse-data:1 \
  --environment "Variables={S3_BUCKET=YOUR-BUCKET-NAME,S3_PREFIX=nse-data/}" \
  --region ap-south-1
```

## Step 4: Schedule Daily Run (EventBridge)

```bash
# Create rule (runs Mon-Fri at 6:30 PM IST = 1:00 PM UTC)
aws events put-rule \
  --name nse-daily-download \
  --schedule-expression "cron(0 13 ? * MON-FRI *)" \
  --description "Download NSE reports after market close" \
  --region ap-south-1

# Add Lambda as target
aws events put-targets \
  --rule nse-daily-download \
  --targets '[{
    "Id": "nse-data-lambda",
    "Arn": "arn:aws:lambda:ap-south-1:ACCOUNT_ID:function:nse-data-downloader",
    "Input": "{\"date\": \"TODAY\", \"download_all\": true, \"include_pdfs\": true}"
  }]' \
  --region ap-south-1

# Grant EventBridge permission to invoke Lambda
aws lambda add-permission \
  --function-name nse-data-downloader \
  --statement-id eventbridge-daily \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:ap-south-1:ACCOUNT_ID:rule/nse-daily-download
```

> **Note:** For dynamic date, modify the Lambda to use `datetime.now()` if `date` is `"TODAY"`.

## Step 5: Test

```bash
# Invoke manually
aws lambda invoke \
  --function-name nse-data-downloader \
  --payload '{"date": "2026-05-19", "report_types": ["ind_close_all", "sec_bhavdata_full"]}' \
  --region ap-south-1 \
  output.json

cat output.json
```

## S3 Output Structure

```
s3://my-bucket/nse-data/
├── 2026-05-19/
│   ├── sec_bhavdata_full/
│   │   └── sec_bhavdata_full_19052026.csv
│   ├── ind_close_all/
│   │   └── ind_close_all_19052026.csv
│   ├── cmvolt/
│   │   └── CMVOLT_19052026.CSV
│   ├── fo_secban/
│   │   └── fo_secban_19052026.csv
│   ├── security_master/
│   │   └── NSE_CM_security_19052026.csv.gz
│   └── ...
└── pdfs/
    ├── index_dashboard_pdf/
    │   └── Index_Dashboard_May2026.pdf
    └── passive_fund_pdf/
        └── NiftyPassiveFundReport-May2026-B2B-HR.pdf
```

## Event Examples

### Download default reports (5 most useful)
```json
{
  "date": "2026-05-19",
  "bucket": "my-nse-bucket"
}
```

### Download ALL reports + PDFs
```json
{
  "date": "2026-05-19",
  "bucket": "my-nse-bucket",
  "download_all": true,
  "include_pdfs": true
}
```

### Download specific reports only
```json
{
  "date": "2026-05-19",
  "bucket": "my-nse-bucket",
  "report_types": ["sec_bhavdata_full", "ind_close_all", "fo_secban", "cmvolt"]
}
```

### Custom S3 prefix
```json
{
  "date": "2026-05-19",
  "bucket": "my-nse-bucket",
  "prefix": "raw/nse-india/",
  "download_all": true
}
```

## Local Testing (without AWS)

```bash
cd .lambda_layer
python3 lambda_function.py 2026-05-19
```

This tests DataFrame downloads without S3. To test with S3:

```bash
export S3_BUCKET=my-nse-bucket
python3 lambda_function.py 2026-05-19 my-nse-bucket
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Timeout | Increase to 300s. NSE session warmup takes 3-5s. |
| Memory error | Increase to 512MB+. `security_master` is ~13MB CSV. |
| HTTP 403 | Non-trading day (weekend/holiday). Add date validation. |
| HTTP 404 | File not yet published. NSE publishes after 6 PM IST. |
| Rate limited | Add delays between downloads (script has 0.5s delay). |
