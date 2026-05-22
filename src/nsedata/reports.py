"""
NSE Daily Reports — Bhavcopy and other daily files from nsearchives.nseindia.com.

Data source: https://www.nseindia.com/all-reports

This module downloads reports that are available as direct file URLs from
nsearchives.nseindia.com. These work reliably from any environment including
AWS Lambda, Snowflake, and other cloud platforms (no Cloudflare protection).

All get_* functions return pandas.DataFrame.
download_report() saves raw file to disk.

Functions:
    get(report_type, date) → DataFrame          # Universal getter
    get_bhavcopy(date) → DataFrame
    get_sec_bhavdata(date) → DataFrame
    get_ind_close_all(date) → DataFrame
    get_market_activity(date) → DataFrame
    download_report(report_type, date, output_dir) → Path
"""

import gzip
import io
import os
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

from nsedata.session import create_nse_session

NSE_ARCHIVES = "https://nsearchives.nseindia.com"

# URL patterns for various reports
# Date placeholders:
#   {ddmmyy}     → 170426
#   {ddmmyyyy}   → 17042026
#   {yyyymmdd}   → 20260417
#   {MON}        → APR (uppercase 3-letter month)
#   {ddMONyyyy}  → 17APR2026
REPORT_PATTERNS = {
    # --- Capital Market: Prices ---
    "pr": "/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip",
    "sec_bhavdata_full": "/products/content/sec_bhavdata_full_{ddmmyyyy}.csv",
    "bhav_udiff": "/content/cm/BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip",
    "sme": "/archives/sme/sme{ddmmyyyy}.csv",
    # --- Capital Market: Indices ---
    "ind_close_all": "/content/indices/ind_close_all_{ddmmyyyy}.csv",
    "pe": "/archives/equities/mkt/PE_{ddmmyy}.csv",
    "reg_ind": "/archives/equities/mkt/REG_IND{ddmmyy}.csv",
    # --- Capital Market: Activity & Deals ---
    "market_activity": "/archives/equities/mkt/MA{ddmmyy}.csv",
    "short_selling": "/archives/equities/shortSelling/shortselling_{ddmmyyyy}.csv",
    # --- Capital Market: Reference & Master ---
    "security_master": "/content/cm/NSE_CM_security_{ddmmyyyy}.csv.gz",
    "cm_52wk": "/content/equities/CM_52_wk_High_low_{ddmmyyyy}.csv",
    # --- Capital Market: Risk & Margin ---
    "cmvolt": "/archives/nsccl/volt/CMVOLT_{ddmmyyyy}.CSV",
    "mto": "/archives/equities/mto/MTO_{ddmmyyyy}.DAT",
    # --- Derivatives: F&O ---
    "fo_secban": "/archives/fo/sec_ban/fo_secban_{ddmmyyyy}.csv",
    "fovolt": "/archives/nsccl/volt/FOVOLT_{ddmmyyyy}.csv",
    "fo_sett": "/archives/nsccl/fao/FOSett_prce_{ddmmyyyy}.csv",
    # --- Derivatives: Commodity ---
    "co_volt": "/archives/nsccl/volt/CO_VOLT_{ddmmyyyy}.csv",
    # --- Derivatives: Currency ---
    "x_volt": "/archives/nsccl/volt/X_VOLT_{ddmmyyyy}.csv",
    "cd_sett": "/archives/nsccl/cd/CDSett_prce_{ddmmyyyy}.csv",
    # --- Debt ---
    "trm_bc": "/archives/trep/TRM_BC{ddmmyyyy}.csv",
}


def get(report_type: str, date: str) -> pd.DataFrame:
    """
    Universal report getter — downloads any report type and returns a DataFrame.

    Works from AWS Lambda, Snowflake, or any cloud environment.

    Args:
        report_type: One of the keys in REPORT_PATTERNS (e.g. "cmvolt", "sme", "pe")
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        pandas.DataFrame with the report data.

    Example:
        >>> from nsedata import reports
        >>> df = reports.get("cmvolt", "2026-04-17")
        >>> df = reports.get("fo_secban", "2026-04-17")
        >>> df = reports.get("security_master", "2026-04-17")
    """
    dt = _parse_date(date)
    session = create_nse_session()

    if report_type not in REPORT_PATTERNS:
        raise ValueError(
            f"Unknown report type: '{report_type}'. "
            f"Available: {sorted(REPORT_PATTERNS.keys())}"
        )

    pattern = REPORT_PATTERNS[report_type]
    url = NSE_ARCHIVES + pattern.format(
        ddmmyy=dt.strftime("%d%m%y"),
        ddmmyyyy=dt.strftime("%d%m%Y"),
        yyyymmdd=dt.strftime("%Y%m%d"),
        ddMONyyyy=dt.strftime("%d%b%Y").upper(),
        MON=dt.strftime("%b").upper(),
    )

    resp = session.get(url, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to download {report_type}: HTTP {resp.status_code} for {url}"
        )

    # Parse based on file type
    if url.endswith(".csv.zip"):
        # ZIP containing CSV
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            csv_name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
            df = pd.read_csv(io.BytesIO(zf.read(csv_name)))
    elif url.endswith(".csv.gz"):
        # Gzipped CSV
        decompressed = gzip.decompress(resp.content)
        df = pd.read_csv(io.BytesIO(decompressed))
    elif url.endswith(".zip"):
        # ZIP (PR bundle) — extract first CSV
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            csv_files = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not csv_files:
                raise RuntimeError(f"No CSV found in ZIP from {url}")
            df = pd.read_csv(io.BytesIO(zf.read(csv_files[0])))
    elif url.endswith(".DAT") or url.endswith(".T01"):
        # Fixed-width / pipe-delimited — try CSV parse with flexible separator
        df = pd.read_csv(io.StringIO(resp.text), sep=None, engine="python")
    else:
        # Plain CSV
        df = pd.read_csv(io.StringIO(resp.text))

    df.columns = [c.strip() for c in df.columns]
    return df


# --- Convenience functions (backward-compatible) ---


def get_bhavcopy(date: str) -> pd.DataFrame:
    """
    Download and parse the PR (Price Record) bhavcopy zip for a given date.

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with OHLC data for all securities.

    Example:
        >>> from nsedata import reports
        >>> df = reports.get_bhavcopy("2026-04-17")
    """
    return get("pr", date)


def get_sec_bhavdata(date: str) -> pd.DataFrame:
    """
    Download sec_bhavdata_full CSV — full security-wise bhavcopy with delivery data.

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with columns: SYMBOL, SERIES, OPEN_PRICE, HIGH_PRICE, LOW_PRICE,
        CLOSE_PRICE, LAST_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS,
        NO_OF_TRADES, DELIV_QTY, DELIV_PER, etc.

    Example:
        >>> from nsedata import reports
        >>> df = reports.get_sec_bhavdata("2026-04-17")
        >>> df[df["SYMBOL"] == "RELIANCE"]
    """
    return get("sec_bhavdata_full", date)


def get_ind_close_all(date: str) -> pd.DataFrame:
    """
    Download ind_close_all CSV — closing values for all indices on a given date.

    This is the recommended way to get index data (OHLC for all 147+ indices)
    in automated pipelines. Works from AWS Lambda, Snowflake, etc.

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with columns: Index Name, Index Date, Open Index Value,
        High Index Value, Low Index Value, Closing Index Value,
        Points Change, Change(%), Volume, Turnover (Rs. Cr.), P/E, P/B, Div Yield

    Example:
        >>> from nsedata import reports
        >>> df = reports.get_ind_close_all("2026-04-17")
        >>> df[df["Index Name"] == "Nifty 50"]
    """
    return get("ind_close_all", date)


def get_market_activity(date: str) -> pd.DataFrame:
    """
    Download Market Activity report (MA file).

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with market activity data (turnover, advances/declines, etc.)
    """
    return get("market_activity", date)


def download_report(report_type: str, date: str, output_dir: str = ".") -> Path:
    """
    Download any report type and save the raw file to disk.

    Args:
        report_type: One of the keys in REPORT_PATTERNS
        date: Date string in YYYY-MM-DD format
        output_dir: Directory to save the file (default: current directory)

    Returns:
        Path to the saved file.

    Example:
        >>> from nsedata import reports
        >>> path = reports.download_report("sec_bhavdata_full", "2026-04-17", "./data")
    """
    dt = _parse_date(date)
    session = create_nse_session()

    if report_type not in REPORT_PATTERNS:
        raise ValueError(
            f"Unknown report type: '{report_type}'. "
            f"Available: {sorted(REPORT_PATTERNS.keys())}"
        )

    pattern = REPORT_PATTERNS[report_type]
    url = NSE_ARCHIVES + pattern.format(
        ddmmyy=dt.strftime("%d%m%y"),
        ddmmyyyy=dt.strftime("%d%m%Y"),
        yyyymmdd=dt.strftime("%Y%m%d"),
        ddMONyyyy=dt.strftime("%d%b%Y").upper(),
        MON=dt.strftime("%b").upper(),
    )

    resp = session.get(url, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to download {report_type}: HTTP {resp.status_code} for {url}"
        )

    os.makedirs(output_dir, exist_ok=True)
    filename = url.split("/")[-1]
    out_path = Path(output_dir) / filename

    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path


def _parse_date(date: str) -> datetime:
    """Parse YYYY-MM-DD date string."""
    return datetime.strptime(date, "%Y-%m-%d")
