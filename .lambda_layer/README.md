# Lambda Layer for nse-data

Pre-built AWS Lambda layer containing `nse-data` with all dependencies (`pandas`, `requests`).

## Quick Build

```bash
cd lambda_layer
chmod +x build.sh
./build.sh
```

Output: `nse-data-lambda-layer.zip`

## Upload to AWS

```bash
aws lambda publish-layer-version \
  --layer-name nse-data \
  --zip-file fileb://nse-data-lambda-layer.zip \
  --compatible-runtimes python3.12 python3.13 \
  --description "nse-data library with pandas and requests"
```

## Attach to Lambda Function

```bash
aws lambda update-function-configuration \
  --function-name my-nse-function \
  --layers arn:aws:lambda:ap-south-1:123456789:layer:nse-data:1
```

## Lambda Handler Example

```python
from nsedata import reports

def handler(event, context):
    date = event["date"]  # "2026-05-19"
    bucket = event.get("bucket", "my-nse-bucket")

    # Get as DataFrame (for processing)
    df = reports.get("sec_bhavdata_full", date)
    print(f"Rows: {len(df)}")

    # Or upload raw file to S3
    uri = reports.download_report(
        "sec_bhavdata_full", date,
        s3_bucket=bucket,
        s3_prefix=f"raw/sec_bhavdata/{date}/"
    )

    return {"s3_uri": uri, "rows": len(df)}
```

## IAM Policy

Your Lambda execution role needs:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:PutObject"],
            "Resource": "arn:aws:s3:::my-nse-bucket/*"
        }
    ]
}
```

## Layer Size

| Component | Approx Size |
|-----------|-------------|
| pandas | ~45 MB |
| numpy | ~30 MB |
| requests + deps | ~2 MB |
| nse-data | ~20 KB |
| **Total (zipped)** | **~35-50 MB** |

Lambda layer limit: 250 MB unzipped. This layer is well within limits.

## Notes

- `boto3` is NOT included in the layer — Lambda runtime already provides it
- Build on Linux/WSL for correct binary compatibility
- For Python 3.14: change `PYTHON_VERSION` in `build.sh` when Lambda supports it
- The layer includes `numpy` (pandas dependency) compiled for x86_64 Amazon Linux
