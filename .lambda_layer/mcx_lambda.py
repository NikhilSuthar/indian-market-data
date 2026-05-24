"""
AWS Lambda function — MCX India commodity data downloader
==========================================================
Downloads MCX spot market data to S3 using mcx-data.

S3 output structure:
    s3://bucket/<prefix>/
    ├── Spot Market/Recent/
    │   └── MCX_spot_recent_ALL_20260522.csv    ← all 28 commodities, today
    └── Spot Market/Archive/
        ├── MCX_spot_archive_GOLD_20260501_20260522.csv
        ├── MCX_spot_archive_SILVER_20260501_20260522.csv
        └── ...

Runtime:  Python 3.12+
Layer:    nse-data-lambda-layer.zip  (includes curl-cffi for Akamai WAF bypass)
Memory:   256 MB
Timeout:  120 seconds

IAM permissions required:
    s3:PutObject on arn:aws:s3:::YOUR-BUCKET/*

Environment variables:
    S3_BUCKET      Target bucket (can also pass in event)
    MCX_S3_PREFIX  Root prefix, default: "mcx-data/"

Event schema:
{
    "date":           "2026-05-22",       # YYYY-MM-DD (required)
    "bucket":         "my-bucket",        # S3 bucket (or set S3_BUCKET env var)
    "mcx_prefix":     "raw/mcx/",         # S3 prefix (optional)
    "mcx_spot":       true,               # Download today's spot prices (all 28)
    "mcx_archive":    true,               # Download historical archive
    "mcx_from_date":  "2026-05-01",       # Archive from date YYYY-MM-DD
    "mcx_to_date":    "2026-05-22",       # Archive to date YYYY-MM-DD
    "mcx_commodities": ["GOLD", "SILVER"] # Specific list (omit = all 28)
}

Example events:

    # Today's spot prices for all 28 commodities
    {"date": "2026-05-22", "bucket": "my-bucket", "mcx_spot": true}

    # Archive for specific commodities
    {"date": "2026-05-22", "bucket": "my-bucket",
     "mcx_archive": true, "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
     "mcx_commodities": ["GOLD", "SILVER", "CRUDEOIL"]}

    # Archive for ALL 28 commodities
    {"date": "2026-05-22", "bucket": "my-bucket",
     "mcx_archive": true, "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22"}

    # Both spot + archive together
    {"date": "2026-05-22", "bucket": "my-bucket",
     "mcx_spot": true, "mcx_archive": true,
     "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
     "mcx_commodities": ["GOLD", "SILVER", "CRUDEOIL", "NATURALGAS", "COPPER"]}

Notes:
    - MCX archive requires a specific commodity — "ALL" returns empty (MCX API limitation)
    - curl-cffi must be in the layer (bypasses MCX Akamai WAF via Chrome TLS impersonation)
    - Inter-commodity delay of 1.5s is applied to be polite to MCX servers
"""

import json
import os
import time
from datetime import datetime

# MCX import with graceful fallback
try:
    from mcxdata import mcx as _mcx
    MCX_AVAILABLE = True
except ImportError:
    MCX_AVAILABLE = False
    print("⚠️  mcx-data not found in layer — MCX downloads will be skipped")

# All 28 MCX commodities (as of 2026)
ALL_MCX_COMMODITIES = [
    "ALUMINI", "ALUMINIUM", "CARDAMOM", "COPPER", "COTTON", "COTTONOIL",
    "CPO", "CRUDEOIL", "CRUDEOILM", "ELECDMBL", "GOLD", "GOLDGUINEA",
    "GOLDM", "GOLDPETAL", "GOLDTEN", "KAPAS", "LEAD", "LEADMINI",
    "MENTHAOIL", "NATGASMINI", "NATURALGAS", "NICKEL", "SILVER", "SILVERM",
    "SILVERMIC", "STEELREBAR", "ZINC", "ZINCMINI",
]


def lambda_handler(event, context):
    """MCX Lambda handler — downloads MCX spot market data to S3."""

    date        = event.get("date")
    bucket      = event.get("bucket") or os.environ.get("S3_BUCKET")
    prefix      = event.get("mcx_prefix") or os.environ.get("MCX_S3_PREFIX", "mcx-data/")
    mcx_spot    = event.get("mcx_spot", False)
    mcx_archive = event.get("mcx_archive", False)
    from_date   = event.get("mcx_from_date")
    to_date     = event.get("mcx_to_date", date)
    commodities = event.get("mcx_commodities")

    if not date:
        return {"statusCode": 400, "body": "Missing 'date' (YYYY-MM-DD)"}
    if not bucket:
        return {"statusCode": 400, "body": "Missing 'bucket' or S3_BUCKET env var"}
    if not mcx_spot and not mcx_archive:
        return {"statusCode": 400,
                "body": "Set at least one of: mcx_spot=true, mcx_archive=true"}

    if not MCX_AVAILABLE:
        return {"statusCode": 500,
                "body": "mcx-data not installed in layer. "
                        "Rebuild with build.sh and redeploy."}

    # Log which HTTP backend is active (helps diagnose WAF issues)
    try:
        from mcxdata.session import get_session
        _, stype = get_session()
        print(f"MCX session type: {stype}  "
              f"(curl_cffi=best for Akamai WAF, requests=may 403)")
    except Exception:
        pass

    results = {"date": date, "bucket": bucket}

    # ── Spot Recent ───────────────────────────────────────────
    if mcx_spot:
        results["spot_recent"] = _download_spot_recent(bucket, prefix, date)

    # ── Spot Archive ──────────────────────────────────────────
    if mcx_archive:
        if not from_date:
            from_date = date[:7] + "-01"
            print(f"mcx_from_date not set — defaulting to {from_date}")
        comms = commodities if commodities else ALL_MCX_COMMODITIES
        results["spot_archive"] = _download_spot_archive(
            bucket, prefix, from_date, to_date, comms
        )

    # Summary
    total_uploaded = 0
    total_failed   = 0
    if "spot_recent" in results:
        if results["spot_recent"].get("status") == "SUCCESS":
            total_uploaded += 1
        else:
            total_failed += 1
    if "spot_archive" in results:
        total_uploaded += results["spot_archive"]["summary"]["uploaded"]
        total_failed   += results["spot_archive"]["summary"]["failed"]

    results["summary"] = {"uploaded": total_uploaded, "failed": total_failed}
    print(f"=== MCX: {total_uploaded} uploaded, {total_failed} failed ===")

    return {"statusCode": 200, "body": json.dumps(results, default=str)}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _download_spot_recent(bucket: str, prefix: str, date: str) -> dict:
    """Download today's MCX spot prices for all commodities."""
    try:
        df = _mcx.get_spot_recent()
        if df.empty:
            return {"status": "EMPTY", "rows": 0}

        import boto3
        date_compact = date.replace("-", "")
        key = f"{prefix}Spot Market/Recent/MCX_spot_recent_ALL_{date_compact}.csv"
        boto3.client("s3").put_object(
            Bucket=bucket, Key=key,
            Body=df.to_csv(index=False).encode("utf-8"),
            ContentType="text/csv",
        )
        uri = f"s3://{bucket}/{key}"
        print(f"✓ MCX spot_recent → {key.split('/')[-1]} ({len(df)} rows)")
        return {"status": "SUCCESS", "rows": len(df), "s3_uri": uri}

    except Exception as e:
        err = str(e)[:120]
        print(f"✗ MCX spot_recent: {err}")
        return {"status": "FAILED", "error": err}


def _download_spot_archive(bucket: str, prefix: str, from_date: str,
                            to_date: str, commodities: list) -> dict:
    """Download MCX spot archive for a list of commodities."""
    import boto3
    s3       = boto3.client("s3")
    uploaded = []
    failed   = []
    fd       = from_date.replace("-", "")
    td       = to_date.replace("-", "")

    for commodity in commodities:
        try:
            df = _mcx.get_spot_archive(from_date, to_date, commodity=commodity)
            if df.empty:
                print(f"  MCX archive {commodity}: no data")
                failed.append({"commodity": commodity, "error": "empty response"})
                time.sleep(1)
                continue

            key = (f"{prefix}Spot Market/Archive/"
                   f"MCX_spot_archive_{commodity}_{fd}_{td}.csv")
            s3.put_object(
                Bucket=bucket, Key=key,
                Body=df.to_csv(index=False).encode("utf-8"),
                ContentType="text/csv",
            )
            uri = f"s3://{bucket}/{key}"
            print(f"✓ MCX archive {commodity}: {len(df)} rows → {key.split('/')[-1]}")
            uploaded.append({"commodity": commodity, "rows": len(df), "s3_uri": uri})

        except Exception as e:
            err = str(e)[:100]
            print(f"✗ MCX archive {commodity}: {err}")
            failed.append({"commodity": commodity, "error": err})

        time.sleep(1.5)

    summary = {
        "total":    len(commodities),
        "uploaded": len(uploaded),
        "failed":   len(failed),
    }
    print(f"=== MCX archive: {summary['uploaded']} uploaded, "
          f"{summary['failed']} failed ===")
    return {"summary": summary, "uploaded": uploaded, "failed": failed}
