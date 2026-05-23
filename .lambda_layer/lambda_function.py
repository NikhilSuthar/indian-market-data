"""
AWS Lambda function — nse-data v0.6.0
======================================
Downloads NSE datasets to S3 using the new hierarchical API:
    nse.download(category, subcategory, dataset, date, s3_bucket=..., s3_prefix=...)

Runtime:  Python 3.12+
Layer:    nse-data-lambda-layer.zip
Memory:   512 MB (pandas needs headroom for large files)
Timeout:  300 seconds

Environment Variables:
    S3_BUCKET   — Target S3 bucket (required)
    S3_PREFIX   — Key prefix, default: "nse-data/"

IAM Policy required (attach to Lambda execution role):
    { "Effect": "Allow", "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::YOUR-BUCKET/nse-data/*" }

Event examples:
    # Download defaults (5 core datasets)
    { "date": "2026-05-22", "bucket": "my-bucket" }

    # Download all supported daily datasets
    { "date": "2026-05-22", "bucket": "my-bucket", "download_all": true }

    # Specific datasets
    { "date": "2026-05-22", "bucket": "my-bucket",
      "datasets": [
        ["capital_market", "equities_sme", "sec_bhavdata_full"],
        ["capital_market", "indices", "ind_close_all"],
        ["derivatives", "equity", "fo_bhav_udiff"]
      ]}

    # Monthly datasets
    { "date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket",
      "download_all": true }
"""

import json
import os
import time
from datetime import datetime

from nsedata import nse
from nsedata.registry import get_config

# ─── Default datasets (confirmed working from Lambda) ────────────────────────
DEFAULT_DATASETS = [
    ("capital_market", "equities_sme", "sec_bhavdata_full"),
    ("capital_market", "indices",      "ind_close_all"),
    ("capital_market", "equities_sme", "cmvolt"),
    ("derivatives",    "equity",       "fo_secban"),
    ("capital_market", "equities_sme", "security_master"),
]

# ─── All daily datasets (91 total in registry) ───────────────────────────────
ALL_DAILY_DATASETS = [
    # Capital Market — Equities & SME
    ("capital_market", "equities_sme", "bhavcopy_pr"),
    ("capital_market", "equities_sme", "sec_bhavdata_full"),
    ("capital_market", "equities_sme", "bhav_udiff"),
    ("capital_market", "equities_sme", "security_master"),
    ("capital_market", "equities_sme", "market_activity"),
    ("capital_market", "equities_sme", "cmvolt"),
    ("capital_market", "equities_sme", "short_selling"),
    ("capital_market", "equities_sme", "mto"),
    ("capital_market", "equities_sme", "52wk_high_low"),
    ("capital_market", "equities_sme", "block_deals"),
    ("capital_market", "equities_sme", "bulk_deals"),
    ("capital_market", "equities_sme", "pe"),
    ("capital_market", "equities_sme", "reg_ind"),
    ("capital_market", "equities_sme", "reg1_ind"),
    ("capital_market", "equities_sme", "sme"),
    ("capital_market", "equities_sme", "sme_bands"),
    ("capital_market", "equities_sme", "eq_band_changes"),
    ("capital_market", "equities_sme", "sec_list"),
    ("capital_market", "equities_sme", "series_change"),
    ("capital_market", "equities_sme", "mf_var"),
    ("capital_market", "equities_sme", "appsec_collval"),
    ("capital_market", "equities_sme", "csqr"),
    ("capital_market", "equities_sme", "c_stt"),
    ("capital_market", "equities_sme", "c_stt_ind"),
    ("capital_market", "equities_sme", "cm_latency"),
    ("capital_market", "equities_sme", "fcm_bc"),
    ("capital_market", "equities_sme", "corpbond"),
    ("capital_market", "equities_sme", "mrg_trading"),
    # C_VAR1 snapshots 1-6 (download only)
    # ("capital_market", "equities_sme", "cvar1"),  # needs snapshot=1..6
    # Capital Market — Indices
    ("capital_market", "indices", "ind_close_all"),
    ("capital_market", "indices", "top_movers"),
    # Capital Market — SLB
    ("capital_market", "slb", "slb_elg_sec"),
    ("capital_market", "slb", "slb_openpos"),
    ("capital_market", "slb", "slb_foreclosure"),
    # Derivatives — Equity
    ("derivatives", "equity", "fo_bhav_udiff"),
    ("derivatives", "equity", "fo_contract"),
    ("derivatives", "equity", "fo_secban"),
    ("derivatives", "equity", "fovolt"),
    # Derivatives — Commodity
    ("derivatives", "commodity", "co_bhav_udiff"),
    ("derivatives", "commodity", "co_contract"),
    # Derivatives — Currency
    ("derivatives", "currency", "cd_bhav_udiff"),
    ("derivatives", "currency", "cd_contract"),
    # Derivatives — Interest Rate
    ("derivatives", "interest_rate", "irf_bhavcopy"),
    ("derivatives", "interest_rate", "i_volt"),
    ("derivatives", "interest_rate", "cd_sett_irf"),
    ("derivatives", "interest_rate", "ewpl"),
    ("derivatives", "interest_rate", "fpi_long"),
    ("derivatives", "interest_rate", "fii_long"),
    # Debt — Corporate
    ("debt", "corporate", "cbm_trd"),
    ("debt", "corporate", "cbm_list_man"),
    ("debt", "corporate", "cbm_list_non_man"),
    ("debt", "corporate", "cbm_fail"),
    ("debt", "corporate", "cbm_unlist_man"),
    ("debt", "corporate", "cbm_unlist_non_man"),
    ("debt", "corporate", "sdt_fail"),
    ("debt", "corporate", "sdt_list_man"),
    ("debt", "corporate", "sdt_list_non_man"),
    ("debt", "corporate", "sdt_unlist_man"),
    ("debt", "corporate", "sdt_unlist_non_man"),
    ("debt", "corporate", "cp_settlement"),
    ("debt", "corporate", "cd_settlement"),
    ("debt", "corporate", "gsec_settlement"),
    ("debt", "corporate", "corporate_bond_report"),
    # Debt — Debt Segment
    ("debt", "debt_segment", "wdmlist"),
    ("debt", "debt_segment", "dly_bundle"),
    # Debt — Tri-Party Repo
    ("debt", "tri_party_repo", "trm_bc"),
]

ALL_MONTHLY_DATASETS = [
    ("capital_market", "equities_sme", "c_catg"),
    ("capital_market", "slb", "slb_cli"),
    ("capital_market", "slb", "slb_fopl"),
    ("capital_market", "slb", "slb_mpl"),
    ("capital_market", "slb", "slb_ppl"),
    ("capital_market", "slb", "slb_transaction_data"),
    ("derivatives", "equity", "fopl"),
    ("derivatives", "equity", "mpl"),
    ("derivatives", "equity", "tmopl"),
    ("derivatives", "equity", "fo_impact_cost"),
    ("derivatives", "commodity", "payinpayout"),
    ("debt", "debt_segment", "accrued_interest"),
]


def lambda_handler(event, context):
    """Main Lambda handler."""

    # Parse input
    date  = event.get("date")
    month = event.get("month") or (date[:7] if date else None)  # auto-derive YYYY-MM from date
    bucket = event.get("bucket") or os.environ.get("S3_BUCKET")
    prefix = event.get("prefix") or os.environ.get("S3_PREFIX", "nse-data/")

    if not date:
        return {"statusCode": 400, "body": "Missing 'date' (YYYY-MM-DD)"}
    if not bucket:
        return {"statusCode": 400, "body": "Missing 'bucket' or S3_BUCKET env var"}

    download_all = event.get("download_all", False)
    specific     = event.get("datasets")  # list of [cat, sub, dataset]

    # Determine which datasets to download
    if specific:
        daily_list   = [(c, s, d) for c, s, d in specific if not _is_monthly(c, s, d)]
        monthly_list = [(c, s, d) for c, s, d in specific if _is_monthly(c, s, d)]
    elif download_all:
        daily_list   = ALL_DAILY_DATASETS
        monthly_list = ALL_MONTHLY_DATASETS
    else:
        daily_list   = DEFAULT_DATASETS
        monthly_list = []

    results = {"uploaded": [], "failed": [], "date": date, "month": month, "bucket": bucket}

    # ─── Download daily datasets ──────────────────────────────────────────
    for cat, sub, ds in daily_list:
        _do_download(cat, sub, ds, date, bucket, prefix, results)
        time.sleep(0.3)

    # ─── Download VaR snapshots (6 intraday) ──────────────────────────────
    if download_all:
        for snap in range(1, 7):
            _do_download("capital_market", "equities_sme", "cvar1", date,
                         bucket, prefix, results, snapshot=snap)
            time.sleep(0.3)

    # ─── Download monthly datasets ─────────────────────────────────────────
    for cat, sub, ds in monthly_list:
        _do_download(cat, sub, ds, month, bucket, prefix, results)
        time.sleep(0.3)

    results["summary"] = {
        "total":    len(results["uploaded"]) + len(results["failed"]),
        "uploaded": len(results["uploaded"]),
        "failed":   len(results["failed"]),
    }

    print(f"=== Summary: {results['summary']['uploaded']} uploaded, "
          f"{results['summary']['failed']} failed ===")

    return {"statusCode": 200, "body": json.dumps(results, default=str)}


def _is_monthly(cat, sub, ds):
    try:
        cfg = get_config(cat, sub, ds)
        return cfg.date_type == "monthly"
    except Exception:
        return False


def _do_download(cat, sub, ds, date_val, bucket, prefix, results, **kwargs):
    s3_key_prefix = f"{prefix}{date_val}/{cat}/{sub}/"
    try:
        uri = nse.download(cat, sub, ds, date_val,
                           s3_bucket=bucket, s3_prefix=s3_key_prefix, **kwargs)
        results["uploaded"].append({"dataset": f"{cat}/{sub}/{ds}", "s3_uri": uri})
        print(f"✓ {cat}/{sub}/{ds} → {uri.split('/')[-1]}")
    except Exception as e:
        results["failed"].append({"dataset": f"{cat}/{sub}/{ds}", "error": str(e)[:80]})
        print(f"✗ {cat}/{sub}/{ds}: {str(e)[:70]}")
