"""
AWS Lambda function — NSE India data downloader
================================================
Downloads NSE market data to S3 using nse-archives.

S3 output structure:
    s3://bucket/<prefix>/
    ├── Capital Market/Equities & SME/Daily/
    │   ├── sec_bhavdata_full_22052026.csv
    │   ├── CMVOLT_22052026.CSV
    │   └── ...
    ├── Capital Market/Indices/Daily/
    ├── Derivatives/Equity Derivative/Daily/
    ├── Debt/Corporate Segment/Daily/
    └── niftyindices/tri/          ← TRI data (when test_tri=true)

Runtime:  Python 3.12+
Layer:    nse-data-lambda-layer.zip
Memory:   512 MB recommended
Timeout:  300 seconds

IAM permissions required:
    s3:PutObject on arn:aws:s3:::YOUR-BUCKET/*

Environment variables:
    S3_BUCKET    Target bucket (can also pass in event)
    S3_PREFIX    Root prefix, default: "nse-data/"

Event schema:
{
    "date":         "2026-05-22",     # YYYY-MM-DD (required)
    "month":        "2026-05",        # YYYY-MM (optional, derived from date)
    "bucket":       "my-bucket",      # S3 bucket (or set S3_BUCKET env var)
    "prefix":       "raw/nse/",       # S3 prefix (optional)
    "download_all": true,             # Download all 86 confirmed datasets
    "datasets": [                     # Or specify exact datasets
        ["capital_market", "equities_sme", "sec_bhavdata_full"],
        ["capital_market", "indices", "ind_close_all"]
    ],
    "test_tri":     true,             # Also download TRI from niftyindices.com
    "tri_only":     false,            # ONLY download TRI, skip all NSE datasets
    "tri_index":    "NIFTY 50",       # Specific index (omit = all 30 indices)
    "tri_start":    "01-May-2026",    # TRI from date (DD-Mon-YYYY)
    "tri_end":      "22-May-2026"     # TRI to date (DD-Mon-YYYY)
}

Example events:

    # 5 default datasets (quick test)
    {"date": "2026-05-22", "bucket": "my-bucket"}

    # All 86 confirmed NSE datasets
    {"date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket", "download_all": true}

    # All NSE + TRI for all 30 Nifty indices
    {"date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket",
     "download_all": true, "test_tri": true,
     "tri_start": "01-May-2026", "tri_end": "22-May-2026"}

    # TRI only (no NSE datasets)
    {"date": "2026-05-22", "bucket": "my-bucket",
     "tri_only": true, "tri_start": "01-May-2026", "tri_end": "22-May-2026"}
"""

import json
import os
import time
from datetime import datetime

from nsedata import nse
from nsedata.registry import get_config

# ── Folder mapping — mirrors NSE Data Download-Sample structure ──────────────
FOLDER_MAP = {
    ("capital_market", "equities_sme"):   ("Capital Market", "Equities & SME"),
    ("capital_market", "indices"):        ("Capital Market", "Indices"),
    ("capital_market", "mutual_fund"):    ("Capital Market", "Mutual Fund"),
    ("capital_market", "slb"):            ("Capital Market", "Securities Lending & Borrowing"),
    ("derivatives",    "equity"):         ("Derivatives",    "Equity Derivative"),
    ("derivatives",    "commodity"):      ("Derivatives",    "Commodity Derivative"),
    ("derivatives",    "currency"):       ("Derivatives",    "Currency Derivative"),
    ("derivatives",    "interest_rate"):  ("Derivatives",    "Interest Rate Derivative"),
    ("debt",           "corporate"):      ("Debt",           "Corporate Segment"),
    ("debt",           "debt_segment"):   ("Debt",           "Debt Segment"),
    ("debt",           "tri_party_repo"): ("Debt",           "Tri-Party Repo"),
    ("egr",            "egr"):            ("EGR",            "EGR"),
}

FREQ_FOLDER = {
    "Daily":                              "Daily",
    "Monthly":                            "Monthly",
    "Weekly/Monthly":                     "Weekly",
    "Monthly (static)":                   "Monthly",
    "Daily (static)":                     "Daily",
    "Daily (6 intraday snapshots)":       "Daily",
    "Archive/Daily":                      "Daily",
    "Weekly":                             "Weekly",
    "Monthly (static file, always current)": "Monthly",
}

# ── All confirmed working datasets ───────────────────────────────────────────
ALL_DAILY = [
    # Capital Market — Equities & SME
    ("capital_market", "equities_sme", "bhavcopy_pr"),
    ("capital_market", "equities_sme", "sec_bhavdata_full"),
    ("capital_market", "equities_sme", "bhav_udiff"),
    ("capital_market", "equities_sme", "security_master"),
    ("capital_market", "equities_sme", "market_activity"),
    ("capital_market", "equities_sme", "cmvolt"),
    ("capital_market", "equities_sme", "short_selling"),
    ("capital_market", "equities_sme", "mto"),
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
    ("capital_market", "equities_sme", "auction_buy"),   # settno auto-calculated
    ("capital_market", "equities_sme", "csqr"),          # settno auto-calculated
    ("capital_market", "equities_sme", "c_stt"),
    ("capital_market", "equities_sme", "c_stt_ind"),
    ("capital_market", "equities_sme", "fcm_bc"),
    ("capital_market", "equities_sme", "corpbond"),
    ("capital_market", "equities_sme", "daily_settlement_doc"),
    # Capital Market — Indices
    ("capital_market", "indices", "ind_close_all"),
    ("capital_market", "indices", "top_movers"),
    # Capital Market — Mutual Fund
    ("capital_market", "mutual_fund", "nsccl_cm_ann_mf"),
    # Capital Market — SLB
    ("capital_market", "slb", "slb_elg_sec"),
    ("capital_market", "slb", "slb_openpos"),
    ("capital_market", "slb", "slb_foreclosure"),
    ("capital_market", "slb", "slb_bc"),
    ("capital_market", "slb", "slb_var"),
    # Derivatives — Equity F&O
    ("derivatives", "equity", "fo_bhav_udiff"),
    ("derivatives", "equity", "fo_contract"),
    ("derivatives", "equity", "fo_secban"),
    ("derivatives", "equity", "fovolt"),
    # Derivatives — Commodity
    ("derivatives", "commodity", "co_bhav_udiff"),
    ("derivatives", "commodity", "co_contract"),
    # Derivatives — Currency
    ("derivatives", "currency", "cd_contract"),
    # Derivatives — Interest Rate
    ("derivatives", "interest_rate", "irf_bhavcopy"),
    ("derivatives", "interest_rate", "i_volt"),
    ("derivatives", "interest_rate", "cd_sett_irf"),
    ("derivatives", "interest_rate", "ewpl"),
    ("derivatives", "interest_rate", "fpi_long"),
    ("derivatives", "interest_rate", "fii_long"),
    ("derivatives", "interest_rate", "tenure_symbol_map"),
    ("derivatives", "interest_rate", "irf_cli_oi"),
    ("derivatives", "interest_rate", "irf_tm_oi"),
    # Debt — Corporate (T-1 settlement files)
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
    # Debt — Segment
    ("debt", "debt_segment", "dly_bundle"),
    # Debt — Tri-Party Repo
    ("debt", "tri_party_repo", "trm_bc"),
    # EGR
    ("egr", "egr", "egr_bc"),
]

ALL_MONTHLY = [
    ("capital_market", "equities_sme", "c_catg"),
    ("capital_market", "mutual_fund",  "nsccl_cm_ann_mf"),
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
]

DEFAULT_DATASETS = [
    ("capital_market", "equities_sme", "sec_bhavdata_full"),
    ("capital_market", "indices",      "ind_close_all"),
    ("capital_market", "equities_sme", "cmvolt"),
    ("derivatives",    "equity",       "fo_secban"),
    ("capital_market", "equities_sme", "security_master"),
]

ALL_TRI_INDICES = [
    "NIFTY 50", "NIFTY NEXT 50", "NIFTY 100", "NIFTY 200",
    "NIFTY 500", "NIFTY MIDCAP 50", "NIFTY MIDCAP 100",
    "NIFTY MIDCAP 150", "NIFTY SMALLCAP 50", "NIFTY SMALLCAP 100",
    "NIFTY SMALLCAP 250", "NIFTY BANK", "NIFTY IT", "NIFTY AUTO",
    "NIFTY PHARMA", "NIFTY FMCG", "NIFTY METAL", "NIFTY ENERGY",
    "NIFTY REALTY", "NIFTY MEDIA", "NIFTY PSE", "NIFTY PSU BANK",
    "NIFTY PVT BANK", "NIFTY FIN SERVICE", "NIFTY OIL & GAS",
    "NIFTY INFRA", "NIFTY MNC", "NIFTY CONSUMPTION",
    "NIFTY SERVICES", "NIFTY COMMODITIES",
]


def lambda_handler(event, context):
    """NSE Lambda handler — downloads NSE datasets to S3."""

    date   = event.get("date")
    month  = event.get("month") or (date[:7] if date else None)
    bucket = event.get("bucket") or os.environ.get("S3_BUCKET")
    prefix = event.get("prefix") or os.environ.get("S3_PREFIX", "nse-data/")

    if not date:
        return {"statusCode": 400, "body": "Missing 'date' (YYYY-MM-DD)"}
    if not bucket:
        return {"statusCode": 400, "body": "Missing 'bucket' or S3_BUCKET env var"}

    download_all_flag = event.get("download_all", False)
    specific          = event.get("datasets")
    test_tri          = event.get("test_tri", False)
    tri_only          = event.get("tri_only", False)

    # Build dataset lists
    if tri_only:
        daily_list   = []
        monthly_list = []
        test_tri     = True
    elif specific:
        daily_list   = [(c, s, d) for c, s, d in specific if not _is_monthly(c, s, d)]
        monthly_list = [(c, s, d) for c, s, d in specific if _is_monthly(c, s, d)]
    elif download_all_flag:
        daily_list   = ALL_DAILY
        monthly_list = ALL_MONTHLY
    else:
        daily_list   = DEFAULT_DATASETS
        monthly_list = []

    results = {"uploaded": [], "failed": [], "date": date, "month": month}

    # Daily datasets
    for cat, sub, ds in daily_list:
        _do_download(cat, sub, ds, date, bucket, prefix, results)
        time.sleep(0.3)

    # VaR snapshots (6 intraday)
    if download_all_flag and not tri_only:
        for snap in range(1, 7):
            _do_download("capital_market", "equities_sme", "cvar1", date,
                         bucket, prefix, results, snapshot=snap)
            time.sleep(0.2)

    # Monthly datasets
    for cat, sub, ds in monthly_list:
        _do_download(cat, sub, ds, month, bucket, prefix, results)
        time.sleep(0.3)

    # TRI from niftyindices.com
    if test_tri:
        indices   = [event["tri_index"]] if event.get("tri_index") else ALL_TRI_INDICES
        tri_start = event.get("tri_start", f"01-{_month_name(date)}-{date[:4]}")
        tri_end   = event.get("tri_end",   _to_ddmonyyyy(date))
        tri_res   = {"uploaded": [], "failed": []}

        for idx in indices:
            r = _download_tri(idx, tri_start, tri_end, bucket, prefix)
            if r["status"] == "SUCCESS":
                tri_res["uploaded"].append({"index": idx, "s3_uri": r["s3_uri"]})
                print(f"✓ TRI {idx}: {r['rows']} rows → {r['s3_uri'].split('/')[-1]}")
            else:
                tri_res["failed"].append({"index": idx, "error": r.get("error", "")[:60]})
                print(f"✗ TRI {idx}: {r.get('error', '')[:60]}")
                if r.get("cloudflare_blocked"):
                    print("Cloudflare blocking — stopping TRI")
                    break
            time.sleep(2)

        tri_res["summary"] = {
            "total":    len(indices),
            "uploaded": len(tri_res["uploaded"]),
            "failed":   len(tri_res["failed"]),
        }
        results["tri"] = tri_res
        print(f"=== TRI: {tri_res['summary']['uploaded']} uploaded, "
              f"{tri_res['summary']['failed']} failed ===")

    results["summary"] = {
        "total":    len(results["uploaded"]) + len(results["failed"]),
        "uploaded": len(results["uploaded"]),
        "failed":   len(results["failed"]),
    }
    print(f"=== NSE: {results['summary']['uploaded']} uploaded, "
          f"{results['summary']['failed']} failed ===")

    return {"statusCode": 200, "body": json.dumps(results, default=str)}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _s3_path(cat, sub, cfg, prefix):
    folder = FOLDER_MAP.get((cat, sub), (cat.title(), sub.title()))
    freq   = FREQ_FOLDER.get(cfg.frequency, "Daily")
    return f"{prefix}{folder[0]}/{folder[1]}/{freq}/"


def _do_download(cat, sub, ds, date_val, bucket, prefix, results, **kwargs):
    try:
        cfg = get_config(cat, sub, ds)
    except Exception:
        return
    if getattr(cfg, "portal_only", False) or not cfg.url_pattern:
        return
    s3_prefix = _s3_path(cat, sub, cfg, prefix)
    try:
        uri = nse.download(cat, sub, ds, date_val,
                           s3_bucket=bucket, s3_prefix=s3_prefix, **kwargs)
        results["uploaded"].append({"dataset": f"{cat}/{sub}/{ds}", "s3_uri": uri})
        print(f"✓ {cat}/{sub}/{ds} → {uri.split('/')[-1]}")
    except Exception as e:
        results["failed"].append({"dataset": f"{cat}/{sub}/{ds}", "error": str(e)[:80]})
        print(f"✗ {cat}/{sub}/{ds}: {str(e)[:60]}")


def _download_tri(index_name, start_date, end_date, bucket, prefix):
    try:
        import boto3
        df_price = nse.get_historical_index(index_name, start_date, end_date)
        df_tri   = nse.get_tri(index_name, start_date, end_date)
        s3       = boto3.client("s3")
        safe     = index_name.replace(" ", "_").replace("&", "and")

        price_key = f"{prefix}niftyindices/price/{safe}_price_{start_date}_to_{end_date}.csv"
        s3.put_object(Bucket=bucket, Key=price_key,
                      Body=df_price.to_csv(index=False).encode("utf-8"))

        tri_key = f"{prefix}niftyindices/tri/{safe}_TRI_{start_date}_to_{end_date}.csv"
        s3.put_object(Bucket=bucket, Key=tri_key,
                      Body=df_tri.to_csv(index=False).encode("utf-8"))

        return {"status": "SUCCESS", "cloudflare_blocked": False,
                "rows": len(df_tri), "s3_uri": f"s3://{bucket}/{tri_key}"}
    except Exception as e:
        err     = str(e)
        blocked = "Cloudflare" in err or "403" in err
        return {"status": "FAILED", "cloudflare_blocked": blocked, "error": err[:200]}


def _is_monthly(cat, sub, ds):
    try:
        return get_config(cat, sub, ds).date_type == "monthly"
    except Exception:
        return False


def _month_name(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b")


def _to_ddmonyyyy(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%b-%Y")
