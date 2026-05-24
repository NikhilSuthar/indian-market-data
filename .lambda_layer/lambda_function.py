"""
AWS Lambda function — nse-data + mcx-data
==========================================
Downloads NSE and MCX datasets to S3.

S3 Structure:
    s3://bucket/nse-data/
    ├── Capital Market/Equities & SME/Daily/
    ├── Capital Market/Indices/Daily/
    ├── Derivatives/Equity Derivative/Daily|Monthly/
    ├── Debt/Corporate Segment/Daily/
    └── ...

    s3://bucket/mcx-data/
    ├── Spot Market/Recent/
    │   └── MCX_spot_recent_ALL_20260522.csv
    └── Spot Market/Archive/
        ├── MCX_spot_archive_GOLD_20260501_20260522.csv
        └── MCX_spot_archive_SILVER_20260501_20260522.csv

Runtime:  Python 3.12+
Layer:    nse-data-lambda-layer.zip
Memory:   512 MB | Timeout: 300s

Event examples:
    # NSE — all datasets
    { "date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket", "download_all": true }

    # NSE — defaults only (5 core datasets)
    { "date": "2026-05-22", "bucket": "my-bucket" }

    # MCX — spot recent (all commodities, today)
    { "date": "2026-05-22", "bucket": "my-bucket", "mcx_spot": true }

    # MCX — spot archive for specific commodities
    { "date": "2026-05-22", "bucket": "my-bucket",
      "mcx_archive": true,
      "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
      "mcx_commodities": ["GOLD", "SILVER", "CRUDEOIL"] }

    # MCX — archive for ALL 28 commodities
    { "date": "2026-05-22", "bucket": "my-bucket",
      "mcx_archive": true,
      "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22" }

    # NSE + MCX together
    { "date": "2026-05-22", "month": "2026-05", "bucket": "my-bucket",
      "download_all": true, "mcx_spot": true, "mcx_archive": true,
      "mcx_from_date": "2026-05-01", "mcx_to_date": "2026-05-22",
      "mcx_commodities": ["GOLD", "SILVER", "CRUDEOIL", "NATURALGAS"] }

    # TRI only
    { "date": "2026-05-22", "bucket": "my-bucket", "tri_only": true,
      "tri_start": "01-May-2026", "tri_end": "22-May-2026" }
"""

import json
import os
import time
from datetime import datetime

from nsedata import nse
from nsedata.registry import get_config

# MCX — import with graceful fallback (in case layer not updated yet)
try:
    from mcxdata import mcx as _mcx
    MCX_AVAILABLE = True
except ImportError:
    MCX_AVAILABLE = False
    print("⚠️  mcx-data not in layer — MCX downloads will be skipped")

# All 28 MCX commodities (as of May 2026)
ALL_MCX_COMMODITIES = [
    "ALUMINI", "ALUMINIUM", "CARDAMOM", "COPPER", "COTTON", "COTTONOIL",
    "CPO", "CRUDEOIL", "CRUDEOILM", "ELECDMBL", "GOLD", "GOLDGUINEA",
    "GOLDM", "GOLDPETAL", "GOLDTEN", "KAPAS", "LEAD", "LEADMINI",
    "MENTHAOIL", "NATGASMINI", "NATURALGAS", "NICKEL", "SILVER", "SILVERM",
    "SILVERMIC", "STEELREBAR", "ZINC", "ZINCMINI",
]

# ─── Folder mapping — mirrors local download structure ───────────────────────
FOLDER_MAP = {
    ("capital_market", "equities_sme"):  ("Capital Market", "Equities & SME"),
    ("capital_market", "indices"):       ("Capital Market", "Indices"),
    ("capital_market", "mutual_fund"):   ("Capital Market", "Mutual Fund"),
    ("capital_market", "slb"):           ("Capital Market", "Securities Lending & Borrowing"),
    ("derivatives",    "equity"):        ("Derivatives",    "Equity Derivative"),
    ("derivatives",    "commodity"):     ("Derivatives",    "Commodity Derivative"),
    ("derivatives",    "currency"):      ("Derivatives",    "Currency Derivative"),
    ("derivatives",    "interest_rate"): ("Derivatives",    "Interest Rate Derivative"),
    ("debt",           "corporate"):     ("Debt",           "Corporate Segment"),
    ("debt",           "debt_segment"):  ("Debt",           "Debt Segment"),
    ("debt",           "tri_party_repo"):("Debt",           "Tri-Party Repo"),
    ("egr",            "egr"):           ("EGR",            "EGR"),
}

FREQ_FOLDER = {
    "Daily": "Daily", "Monthly": "Monthly",
    "Weekly/Monthly": "Weekly", "Monthly (static)": "Monthly",
    "Daily (static)": "Daily", "Daily (6 intraday snapshots)": "Daily",
    "Archive/Daily": "Daily", "Weekly": "Weekly",
    "Monthly (static file, always current)": "Monthly",
}

# ─── All confirmed working datasets (from local + Lambda test run) ────────────
# Daily datasets
ALL_DAILY = [
    # Capital Market — Equities & SME (confirmed working)
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
    ("capital_market", "equities_sme", "auction_buy"),    # settno auto-calculated
    ("capital_market", "equities_sme", "csqr"),           # settno auto-calculated
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
    # Debt — Corporate (use T-1 date for settlement files)
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

# Monthly datasets
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

# Default (5 most important for quick run)
DEFAULT_DATASETS = [
    ("capital_market", "equities_sme", "sec_bhavdata_full"),
    ("capital_market", "indices",      "ind_close_all"),
    ("capital_market", "equities_sme", "cmvolt"),
    ("derivatives",    "equity",       "fo_secban"),
    ("capital_market", "equities_sme", "security_master"),
]


def lambda_handler(event, context):
    """Main Lambda handler."""

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
    tri_only          = event.get("tri_only", False)  # download ONLY TRI, skip all NSE datasets

    # MCX params
    mcx_spot          = event.get("mcx_spot", False)       # download today's spot prices
    mcx_archive       = event.get("mcx_archive", False)    # download historical archive
    mcx_from_date     = event.get("mcx_from_date", None)   # YYYY-MM-DD
    mcx_to_date       = event.get("mcx_to_date", date)     # YYYY-MM-DD, defaults to today
    mcx_commodities   = event.get("mcx_commodities", None) # list or None = all 28
    mcx_prefix        = event.get("mcx_prefix") or os.environ.get("MCX_S3_PREFIX", "mcx-data/")

    # Determine which datasets to download
    if tri_only:
        # Skip all NSE datasets — only run TRI test
        daily_list   = []
        monthly_list = []
        test_tri     = True  # force TRI test on
    elif specific:
        daily_list   = [(c, s, d) for c, s, d in specific if not _is_monthly(c, s, d)]
        monthly_list = [(c, s, d) for c, s, d in specific if _is_monthly(c, s, d)]
    elif download_all_flag:
        daily_list   = ALL_DAILY
        monthly_list = ALL_MONTHLY
    else:
        daily_list   = DEFAULT_DATASETS
        monthly_list = []

    results = {
        "uploaded": [], "failed": [],
        "date": date, "month": month, "bucket": bucket,
    }

    # ─── Daily datasets ───────────────────────────────────────────────────
    for cat, sub, ds in daily_list:
        _do_download(cat, sub, ds, date, bucket, prefix, results)
        time.sleep(0.3)

    # ─── VaR snapshots 1-6 ───────────────────────────────────────────────
    if download_all_flag and not tri_only:
        for snap in range(1, 7):
            _do_download("capital_market", "equities_sme", "cvar1", date,
                         bucket, prefix, results, snapshot=snap)
            time.sleep(0.2)

    # ─── Monthly datasets ─────────────────────────────────────────────────
    for cat, sub, ds in monthly_list:
        _do_download(cat, sub, ds, month, bucket, prefix, results)
        time.sleep(0.3)

    # ─── TRI test (niftyindices.com — tests Cloudflare) ───────────────────
    if test_tri:
        import boto3
        import time as _time

        # All indices to download TRI for (when no specific index passed)
        ALL_TRI_INDICES = [
            # Broad Market
            "NIFTY 50", "NIFTY NEXT 50", "NIFTY 100", "NIFTY 200",
            "NIFTY 500", "NIFTY MIDCAP 50", "NIFTY MIDCAP 100",
            "NIFTY MIDCAP 150", "NIFTY SMALLCAP 50", "NIFTY SMALLCAP 100",
            "NIFTY SMALLCAP 250",
            # Sectoral
            "NIFTY BANK", "NIFTY IT", "NIFTY AUTO", "NIFTY PHARMA",
            "NIFTY FMCG", "NIFTY METAL", "NIFTY ENERGY", "NIFTY REALTY",
            "NIFTY MEDIA", "NIFTY PSE", "NIFTY PSU BANK", "NIFTY PVT BANK",
            "NIFTY FIN SERVICE", "NIFTY OIL & GAS", "NIFTY INFRA",
            "NIFTY MNC", "NIFTY CONSUMPTION", "NIFTY SERVICES",
            "NIFTY COMMODITIES",
        ]

        # If specific index requested, only do that one; else do all
        indices_to_run = [event["tri_index"]] if event.get("tri_index") else ALL_TRI_INDICES

        tri_start = event.get("tri_start", f"01-{_month_name(date)}-{date[:4]}")
        tri_end   = event.get("tri_end",   _to_ddmonyyyy(date))

        tri_results = {"uploaded": [], "failed": []}

        for idx_name in indices_to_run:
            r = _download_tri(idx_name, tri_start, tri_end, bucket, prefix)
            if r["status"] == "SUCCESS":
                tri_results["uploaded"].append({"index": idx_name, "s3_uri": r["s3_uri"]})
                print(f"✓ TRI {idx_name}: {r['rows']} rows → {r['s3_uri'].split('/')[-1]}")
            else:
                tri_results["failed"].append({"index": idx_name, "error": r.get("error","")[:60]})
                print(f"✗ TRI {idx_name}: {r.get('error','')[:60]}")
                # If Cloudflare blocks, stop trying — all will fail
                if r.get("cloudflare_blocked"):
                    print("Cloudflare blocking detected — stopping TRI downloads")
                    break
            _time.sleep(2)  # polite delay for niftyindices.com

        tri_results["summary"] = {
            "total": len(indices_to_run),
            "uploaded": len(tri_results["uploaded"]),
            "failed": len(tri_results["failed"]),
        }
        results["tri_results"] = tri_results
        print(f"\n=== TRI: {tri_results['summary']['uploaded']} uploaded, "
              f"{tri_results['summary']['failed']} failed ===")

    # ─── MCX Spot Recent ─────────────────────────────────────────────────
    if mcx_spot:
        mcx_results = _download_mcx_recent(bucket, mcx_prefix, date)
        results["mcx_spot"] = mcx_results

    # ─── MCX Spot Archive ─────────────────────────────────────────────────
    if mcx_archive:
        if not mcx_from_date:
            print("⚠️  mcx_archive=true but mcx_from_date not set — using first day of month")
            mcx_from_date = date[:7] + "-01"
        commodities = mcx_commodities if mcx_commodities else ALL_MCX_COMMODITIES
        mcx_arch_results = _download_mcx_archive(
            bucket, mcx_prefix, mcx_from_date, mcx_to_date, commodities
        )
        results["mcx_archive"] = mcx_arch_results

    results["summary"] = {
        "total":    len(results["uploaded"]) + len(results["failed"]),
        "uploaded": len(results["uploaded"]),
        "failed":   len(results["failed"]),
    }

    print(f"=== {results['summary']['uploaded']} uploaded, "
          f"{results['summary']['failed']} failed ===")

    return {"statusCode": 200, "body": json.dumps(results, default=str)}


def _s3_path(cat, sub, cfg, prefix, date_val):
    """Build S3 key prefix matching local folder structure."""
    folder = FOLDER_MAP.get((cat, sub), (cat.title(), sub.title()))
    freq   = FREQ_FOLDER.get(cfg.frequency, "Daily")
    return f"{prefix}{folder[0]}/{folder[1]}/{freq}/"


def _do_download(cat, sub, ds, date_val, bucket, prefix, results, **kwargs):
    """Download one dataset to S3."""
    # Skip portal-only and settno-required datasets
    try:
        cfg = get_config(cat, sub, ds)
    except Exception:
        return

    if getattr(cfg, "portal_only", False) or not cfg.url_pattern:
        return  # silently skip

    s3_prefix = _s3_path(cat, sub, cfg, prefix, date_val)

    try:
        uri = nse.download(cat, sub, ds, date_val,
                           s3_bucket=bucket, s3_prefix=s3_prefix, **kwargs)
        results["uploaded"].append({"dataset": f"{cat}/{sub}/{ds}", "s3_uri": uri})
        print(f"✓ {cat}/{sub}/{ds} → {uri.split('/')[-1]}")
    except Exception as e:
        results["failed"].append({"dataset": f"{cat}/{sub}/{ds}", "error": str(e)[:80]})
        print(f"✗ {cat}/{sub}/{ds}: {str(e)[:60]}")


def _download_tri(index_name, start_date, end_date, bucket, prefix):
    """Download TRI for one index and save to S3. Returns status dict."""
    try:
        # Price index
        df_price = nse.get_historical_index(index_name, start_date, end_date)
        # TRI
        df_tri = nse.get_tri(index_name, start_date, end_date)

        import boto3
        s3_client = boto3.client("s3")
        safe_name = index_name.replace(" ", "_").replace("&", "and")

        # Upload price
        price_key = f"{prefix}niftyindices/price/{safe_name}_price_{start_date}_to_{end_date}.csv"
        s3_client.put_object(
            Bucket=bucket, Key=price_key,
            Body=df_price.to_csv(index=False).encode("utf-8")
        )

        # Upload TRI
        tri_key = f"{prefix}niftyindices/tri/{safe_name}_TRI_{start_date}_to_{end_date}.csv"
        s3_client.put_object(
            Bucket=bucket, Key=tri_key,
            Body=df_tri.to_csv(index=False).encode("utf-8")
        )

        return {
            "status": "SUCCESS",
            "cloudflare_blocked": False,
            "rows": len(df_tri),
            "s3_uri": f"s3://{bucket}/{tri_key}",
        }
    except Exception as e:
        err = str(e)
        blocked = "Cloudflare" in err or "timeout" in err.lower() or "403" in err
        return {
            "status": "FAILED",
            "cloudflare_blocked": blocked,
            "error": err[:200],
        }


def _download_mcx_recent(bucket: str, prefix: str, date: str) -> dict:
    """Download MCX spot recent (today's prices) to S3."""
    if not MCX_AVAILABLE:
        return {"status": "SKIPPED", "reason": "mcx-data not in layer"}

    try:
        # Log which HTTP backend is active — helps diagnose WAF issues
        from mcxdata.session import get_session as _get_sess
        _, stype = _get_sess()
        print(f"MCX session type: {stype} (curl_cffi=best, requests=may 403)")

        df = _mcx.get_spot_recent()
        if df.empty:
            return {"status": "EMPTY", "rows": 0}

        date_compact = date.replace("-", "")
        key = f"{prefix}Spot Market/Recent/MCX_spot_recent_ALL_{date_compact}.csv"

        import boto3
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


def _download_mcx_archive(bucket: str, prefix: str, from_date: str,
                           to_date: str, commodities: list) -> dict:
    """Download MCX spot archive for a list of commodities to S3."""
    if not MCX_AVAILABLE:
        return {"status": "SKIPPED", "reason": "mcx-data not in layer"}

    import boto3
    import time as _time

    s3 = boto3.client("s3")
    uploaded, failed = [], []

    # Compact date range for filename
    fd = from_date.replace("-", "")
    td = to_date.replace("-", "")

    for commodity in commodities:
        try:
            df = _mcx.get_spot_archive(from_date, to_date, commodity=commodity)
            if df.empty:
                print(f"  MCX archive {commodity}: no data for {from_date}→{to_date}")
                failed.append({"commodity": commodity, "error": "empty response"})
                _time.sleep(1)
                continue

            key = f"{prefix}Spot Market/Archive/MCX_spot_archive_{commodity}_{fd}_{td}.csv"
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

        _time.sleep(1.5)  # polite delay between commodities

    summary = {
        "total":    len(commodities),
        "uploaded": len(uploaded),
        "failed":   len(failed),
    }
    print(f"=== MCX archive: {summary['uploaded']} uploaded, {summary['failed']} failed ===")
    return {"summary": summary, "uploaded": uploaded, "failed": failed}


def _is_monthly(cat, sub, ds):
    try:
        return get_config(cat, sub, ds).date_type == "monthly"
    except Exception:
        return False


def _month_name(date_str):
    """'2026-05-22' → 'May'"""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b")


def _to_ddmonyyyy(date_str):
    """'2026-05-22' → '22-May-2026'"""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d-%b-%Y")
