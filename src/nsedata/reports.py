"""
NSE Daily Reports — download market data from nsearchives.nseindia.com.

Data source: https://www.nseindia.com/all-reports

This module downloads reports as direct file URLs from nsearchives.nseindia.com.
Works reliably from AWS Lambda, Snowflake, and any cloud/serverless environment.

Functions:
    get(report_type, date) → DataFrame          # Returns parsed DataFrame
    download_report(report_type, date, ...) → Path or str  # Saves raw file (local or S3)
    get_bhavcopy(date) → DataFrame              # Convenience aliases
    get_sec_bhavdata(date) → DataFrame
    get_ind_close_all(date) → DataFrame
    get_market_activity(date) → DataFrame
"""

import gzip
import io
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from nsedata.session import create_nse_session

NSE_ARCHIVES = "https://nsearchives.nseindia.com"

# ---------------------------------------------------------------------------
# Report registry: type → URL pattern
# Date placeholders:
#   {ddmmyy}     → 170426
#   {ddmmyyyy}   → 17042026
#   {yyyymmdd}   → 20260417
#   {MON}        → APR (uppercase 3-letter month)
#   {mon}        → apr (lowercase 3-letter month)
#   {ddMONyyyy}  → 17APR2026
#   {YYYY}       → 2026
# ---------------------------------------------------------------------------
REPORT_PATTERNS = {
    # ===== Capital Market: Prices (CONFIRMED WORKING v0.3.2) =====
    "pr": "/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip",
    "sec_bhavdata_full": "/products/content/sec_bhavdata_full_{ddmmyyyy}.csv",
    "bhav_udiff": "/content/cm/BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip",

    # ===== Capital Market: Indices (CONFIRMED WORKING v0.3.2) =====
    "ind_close_all": "/content/indices/ind_close_all_{ddmmyyyy}.csv",

    # ===== Capital Market: Activity & Deals (CONFIRMED WORKING v0.3.2) =====
    "market_activity": "/archives/equities/mkt/MA{ddmmyy}.csv",
    "short_selling": "/archives/equities/shortSelling/shortselling_{ddmmyyyy}.csv",

    # ===== Capital Market: Reference & Master (CONFIRMED WORKING v0.3.2) =====
    "security_master": "/content/cm/NSE_CM_security_{ddmmyyyy}.csv.gz",

    # ===== Capital Market: Risk & Margin (CONFIRMED WORKING v0.3.2) =====
    "cmvolt": "/archives/nsccl/volt/CMVOLT_{ddmmyyyy}.CSV",
    "mto": "/archives/equities/mto/MTO_{ddmmyyyy}.DAT",

    # ===== Derivatives: Equity F&O (CONFIRMED WORKING v0.3.2) =====
    "fo_secban": "/archives/fo/sec_ban/fo_secban_{ddmmyyyy}.csv",
    "fovolt": "/archives/nsccl/volt/FOVOLT_{ddmmyyyy}.csv",
    "fo_bhav_udiff": "/content/fo/BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
    "fo_contract": "/content/fo/NSE_FO_contract_{ddmmyyyy}.csv.gz",

    # ===== Derivatives: Commodity (CONFIRMED WORKING v0.3.2) =====
    "co_bhav_udiff": "/content/com/BhavCopy_NSE_CO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
    "co_contract": "/content/com/NSE_COM_contract_{ddmmyyyy}.csv.gz",

    # ===== Derivatives: Currency (CONFIRMED WORKING v0.3.2) =====
    "cd_contract": "/content/cd/NSE_CD_contract_{ddmmyyyy}.csv.gz",

    # ===== NEW in v0.4.0 — Capital Market: Indices =====
    "pe": "/archives/equities/mkt/PE_{ddmmyy}.csv",
    "reg_ind": "/archives/equities/mkt/REG_IND{ddmmyy}.csv",
    "reg1_ind": "/archives/equities/mkt/REG1_IND{ddmmyy}.csv",

    # ===== NEW in v0.4.0 — Capital Market: Deals & Activity =====
    "block_deals": "/content/equities/block.csv",
    "bulk_deals": "/content/equities/bulk.csv",
    "eq_band_changes": "/archives/equities/eq_band_changes_{ddmmyyyy}.csv",
    "sec_list": "/archives/equities/sec_list_{ddmmyyyy}.csv",
    "appsec_collval": "/archives/nsccl/collval/APPSEC_COLLVAL_{ddmmyyyy}.csv",
    "mf_var": "/archives/nsccl/mf_var/MF_VAR_{ddmmyyyy}.csv",
    "c_stt_ind": "/archives/nsccl/stt/C_STT_IND_{ddmmyyyy}.csv",
    "csqr": "/archives/nsccl/csqr/CSQR_M_{ddmmyyyy}.csv",
    "ael": "/archives/nsccl/ael/ael_{ddmmyyyy}.csv",

    # ===== NEW in v0.4.0 — Derivatives: Equity F&O =====
    "fo_sett": "/archives/nsccl/fao/FOSett_prce_{ddmmyyyy}.csv",
    "fo_spdcontract": "/content/fo/NSE_FO_spdcontract_{ddmmyyyy}.csv.gz",
    "fao_participant_oi": "/archives/fo/fao_participant_oi_{ddmmyyyy}.csv",
    "fao_participant_vol": "/archives/fo/fao_participant_vol_{ddmmyyyy}.csv",
    "ewpl": "/archives/fo/EWPL_{ddmmyyyy}.CSV",
    "ncloi": "/archives/fo/ncloi_{ddmmyyyy}.csv",
    "combineoi_deleq": "/archives/fo/combineoi_deleq_{ddmmyyyy}.csv",
    "fo_daily": "/content/historical/DERIVATIVES/{YYYY}/{MON}/fo{ddmmyyyy}bhav.csv.zip",

    # ===== NEW in v0.4.0 — Derivatives: Commodity =====
    "co_volt": "/archives/nsccl/volt/CO_VOLT_{ddmmyyyy}.csv",
    "co_sett": "/archives/nsccl/com/CO_sett_prce_{ddmmyyyy}.csv",
    "co_spdcontract": "/content/com/NSE_COM_spdcontract_{ddmmyyyy}.csv.gz",

    # ===== NEW in v0.4.0 — Derivatives: Currency =====
    "x_volt": "/archives/nsccl/volt/X_VOLT_{ddmmyyyy}.CSV",
    "cd_sett": "/archives/nsccl/cd/CDSett_prce_{ddmmyyyy}.csv",
    "cd_spdcontract": "/content/cd/NSE_CD_spdcontract_{ddmmyyyy}.csv.gz",
    "cd_bhav_udiff": "/content/cd/BhavCopy_NSE_CD_0_0_0_{yyyymmdd}_F_0000.csv.zip",

    # ===== NEW in v0.4.0 — Debt =====
    "trm_bc": "/archives/trep/TRM_BC{ddmmyyyy}.csv",

    # ===== NEW in v0.4.0 — Clearing/Risk: DAT/fixed-width =====
    "cvar1": "/archives/nsccl/var/C_VAR1_{ddmmyyyy}_1.DAT",
    "fcm_bc": "/archives/nsccl/fcm/FCM_INTRM_BC{ddmmyyyy}.DAT",
    "slbm_bc": "/archives/nsccl/slb/SLBM_BC_{ddmmyyyy}.DAT",
    "c_catg": "/archives/nsccl/cs/C_CATG_{MON}{YYYY}.T01",
    "slb_var": "/archives/nsccl/slb/C_VAR1_SLB_{ddmmyyyy}_1.DAT",
}

# Reports that require NSE portal API (not direct archive URLs)
# These will be supported in a future version via /api/reports endpoint
_NSEINDIA_PATTERNS = {}

# Report types that are binary/non-parseable
_BINARY_TYPES = set()

_DAT_TYPES = {"mto"}


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def get(report_type: str, date: str) -> pd.DataFrame:
    """
    Universal report getter — downloads any report type and returns a DataFrame.

    Works from AWS Lambda, Snowflake, or any cloud environment.
    Not available for PDF report types (use download_report instead).

    Args:
        report_type: One of the keys in REPORT_PATTERNS
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        pandas.DataFrame with the report data.

    Raises:
        ValueError: If report_type is unknown or is a PDF type.
        RuntimeError: If the download fails (HTTP error, non-trading day, etc.)

    Example:
        >>> from nsedata import reports
        >>> df = reports.get("cmvolt", "2026-04-17")
        >>> df = reports.get("security_master", "2026-04-17")
    """
    if report_type in _BINARY_TYPES:
        raise ValueError(
            f"'{report_type}' is a PDF/binary file and cannot be parsed as DataFrame. "
            f"Use download_report('{report_type}', '{date}', output_dir) instead."
        )

    all_patterns = {**REPORT_PATTERNS, **_NSEINDIA_PATTERNS}
    if report_type not in all_patterns:
        raise ValueError(
            f"Unknown report type: '{report_type}'. "
            f"Available: {sorted(all_patterns.keys())}"
        )

    content, url = _fetch_raw(report_type, date)

    # Parse based on file type
    if url.endswith(".csv.zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            csv_name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
            df = pd.read_csv(io.BytesIO(zf.read(csv_name)))
    elif url.endswith(".csv.gz"):
        decompressed = gzip.decompress(content)
        df = pd.read_csv(io.BytesIO(decompressed))
    elif url.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            csv_files = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not csv_files:
                raise RuntimeError(f"No CSV found in ZIP from {url}")
            # For PR bundle, prefer the pr{DDMMYYYY}.csv file (main price data)
            pr_file = [
                n for n in csv_files
                if n.lower().startswith("pr") and not n.lower().startswith("pre")
            ]
            target = pr_file[0] if pr_file else csv_files[0]
            df = pd.read_csv(io.BytesIO(zf.read(target)))
    elif url.endswith(".DAT") or url.endswith(".T01"):
        df = pd.read_csv(io.StringIO(content.decode("utf-8", errors="replace")),
                         sep=None, engine="python", on_bad_lines="skip")
    else:
        # Handle potential encoding issues (some NSE files use latin-1)
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                text = content.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = content.decode("utf-8", errors="replace")
        df = pd.read_csv(io.StringIO(text), on_bad_lines="skip")

    df.columns = [c.strip() for c in df.columns]
    return df


def download_report(
    report_type: str,
    date: str,
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "",
) -> str:
    """
    Download any report type and save to local disk or S3.

    For S3, uses boto3 with IAM role-based access (no credentials needed in Lambda).
    Ensure your Lambda/EC2 role has s3:PutObject permission on the target bucket.

    Args:
        report_type: One of the keys in REPORT_PATTERNS
        date: Date string in YYYY-MM-DD format
        output_dir: Local directory to save (ignored if s3_bucket is set)
        s3_bucket: S3 bucket name (e.g. "my-nse-data-bucket"). If set, uploads to S3.
        s3_prefix: S3 key prefix/folder (e.g. "raw/nse/" → "raw/nse/filename.csv")

    Returns:
        Local file path (str) or S3 URI (str) e.g. "s3://bucket/prefix/file.csv"

    Examples:
        # Save to local disk
        >>> path = download_report("sec_bhavdata_full", "2026-04-17", "./data")

        # Save to S3 (uses IAM role, no credentials needed)
        >>> s3_uri = download_report("sec_bhavdata_full", "2026-04-17",
        ...                          s3_bucket="my-bucket", s3_prefix="nse/raw/")

        # Download PDF to S3
        >>> s3_uri = download_report("index_dashboard_pdf", "2026-04-17",
        ...                          s3_bucket="my-bucket", s3_prefix="nse/pdfs/")
    """
    content, url = _fetch_raw(report_type, date)
    filename = url.split("/")[-1]

    if s3_bucket:
        # Upload to S3 using boto3 (IAM role-based, no credentials needed)
        try:
            import boto3
        except ImportError:
            raise ImportError(
                "boto3 is required for S3 uploads. Install with: pip install boto3"
            )

        s3_client = boto3.client("s3")
        s3_key = f"{s3_prefix}{filename}" if s3_prefix else filename
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=content)
        return f"s3://{s3_bucket}/{s3_key}"
    else:
        # Save to local disk
        os.makedirs(output_dir, exist_ok=True)
        out_path = Path(output_dir) / filename
        with open(out_path, "wb") as f:
            f.write(content)
        return str(out_path)


# ---------------------------------------------------------------------------
# Convenience functions (backward-compatible)
# ---------------------------------------------------------------------------


def get_bhavcopy(date: str) -> pd.DataFrame:
    """Download and parse the PR bhavcopy zip. Returns main price data."""
    return get("pr", date)


def get_sec_bhavdata(date: str) -> pd.DataFrame:
    """Download sec_bhavdata_full — full bhavcopy with delivery data."""
    return get("sec_bhavdata_full", date)


def get_ind_close_all(date: str) -> pd.DataFrame:
    """Download ind_close_all — closing values for all 147+ indices."""
    return get("ind_close_all", date)


def get_market_activity(date: str) -> pd.DataFrame:
    """Download Market Activity report (turnover, advances/declines)."""
    return get("market_activity", date)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _fetch_raw(report_type: str, date: str) -> tuple:
    """Fetch raw bytes for a report. Returns (content_bytes, url)."""
    dt = _parse_date(date)

    all_patterns = {**REPORT_PATTERNS, **_NSEINDIA_PATTERNS}

    if report_type not in all_patterns:
        raise ValueError(
            f"Unknown report type: '{report_type}'. "
            f"Available: {sorted(all_patterns.keys())}"
        )

    pattern = all_patterns[report_type]

    # Build URL — nsearchives patterns are relative, nseindia patterns are absolute
    if pattern.startswith("http"):
        url = pattern
    else:
        url = NSE_ARCHIVES + pattern

    url = url.format(
        ddmmyy=dt.strftime("%d%m%y"),
        ddmmyyyy=dt.strftime("%d%m%Y"),
        yyyymmdd=dt.strftime("%Y%m%d"),
        ddMONyyyy=dt.strftime("%d%b%Y").upper(),
        MON=dt.strftime("%b").upper(),
        mon=dt.strftime("%b"),
        mm=dt.strftime("%m"),
        YYYY=dt.strftime("%Y"),
    )

    session = create_nse_session()
    resp = session.get(url, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to download {report_type}: HTTP {resp.status_code} for {url}"
        )

    return resp.content, url


def _parse_date(date: str) -> datetime:
    """Parse YYYY-MM-DD date string."""
    return datetime.strptime(date, "%Y-%m-%d")
