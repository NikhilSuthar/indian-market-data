"""
bse-index-data public API.

Usage:
    from bsedata import bse

    # Historical index OHLC
    df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")
    df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")
    df = bse.get_index("BANKEX", "2026-01-01", "2026-05-22")

    # All indices for one date (single API call)
    df = bse.get_all_indices("2026-05-22")

    # Live SENSEX quote
    df = bse.get_live_sensex()

    # List all 50+ supported indices
    bse.list_indices()

    # Download to local file or S3
    bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                       output_dir="./data")
    bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                       s3_bucket="my-bucket", s3_prefix="raw/bse/")
"""

import os
import re
from datetime import datetime
from typing import Optional

import pandas as pd

from bsedata.fetcher import (
    fetch_index_history,
    fetch_all_indices_by_date,
    fetch_index_names,
    fetch_live_sensex,
    _to_yyyymmdd,
)
from bsedata.registry import BSE_INDICES, get_index_config, list_all_indices


# ── Public API ────────────────────────────────────────────────────────────────

def list_indices(category: str = None) -> pd.DataFrame:
    """
    List all supported BSE indices.

    Args:
        category: Optional filter — "Broad Market", "Sectoral", "Thematic",
                  "Strategy", "Global"

    Returns:
        DataFrame — api_key, name, category, description

    Example:
        bse.list_indices()
        bse.list_indices(category="Sectoral")
    """
    rows = list_all_indices()
    if category:
        rows = [r for r in rows if r["category"].lower() == category.lower()]
    return pd.DataFrame(rows)


def get_index(index_name: str, from_date: str, to_date: str) -> pd.DataFrame:
    """
    Get historical OHLC for a BSE index over a date range.

    Returns Date, Open, High, Low, Close from the BSE CSV API.
    For full columns (P/E, P/B, Volume, Turnover) use get_all_indices() per date.

    Args:
        index_name: BSE index API key e.g. "SENSEX", "BSE500", "BANKEX"
                    Use list_indices() to see all supported keys.
        from_date:  Start date — "YYYY-MM-DD" or "YYYYMMDD"
        to_date:    End date   — "YYYY-MM-DD" or "YYYYMMDD"

    Returns:
        DataFrame — Index Name, Date, Open, High, Low, Close

    Example:
        df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")
        df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")
    """
    cfg  = get_index_config(index_name)
    fd   = _to_yyyymmdd(from_date)
    td   = _to_yyyymmdd(to_date)
    return fetch_index_history(cfg.api_key, fd, td)


def get_all_indices(date: str) -> pd.DataFrame:
    """
    Get all BSE indices' closing values for a single date.

    Args:
        date: "YYYY-MM-DD" or "YYYYMMDD"

    Returns:
        DataFrame — Index Name, Date, Open, High, Low, Close, Change, Change %

    Example:
        df = bse.get_all_indices("2026-05-22")
    """
    return fetch_all_indices_by_date(_to_yyyymmdd(date))


def get_live_sensex() -> pd.DataFrame:
    """
    Get live SENSEX quote (real-time, no date param needed).

    Returns:
        DataFrame — Index, LTP, Change, Change %, Open, High, Low, Prev Close, DateTime

    Example:
        df = bse.get_live_sensex()
        print(f"SENSEX: {df['LTP'].iloc[0]:,.2f}")
    """
    return fetch_live_sensex()


def get_index_names_from_api() -> list:
    """
    Fetch the live list of index names directly from BSE API.
    Useful to discover new indices not yet in the registry.

    Returns:
        List of index name strings from BSE API
    """
    return fetch_index_names()


def download_index(
    index_name: str,
    from_date: str,
    to_date: str,
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "bse-index-data/",
) -> str:
    """
    Download BSE index historical data to local file or S3.

    Args:
        index_name: BSE index key e.g. "SENSEX", "BSE500"
        from_date:  "YYYY-MM-DD" or "YYYYMMDD"
        to_date:    "YYYY-MM-DD" or "YYYYMMDD"
        output_dir: Local directory (default: current dir)
        s3_bucket:  S3 bucket name (if saving to S3)
        s3_prefix:  S3 key prefix (default: "bse-index-data/")

    Returns:
        Local file path or "s3://bucket/key"

    Example:
        # Local
        path = bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                                   output_dir="./data")

        # S3 (Lambda with IAM role)
        uri = bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                                  s3_bucket="my-bucket", s3_prefix="raw/bse/")
    """
    df = get_index(index_name, from_date, to_date)

    # Build filename
    fd    = re.sub(r"[^0-9]", "", from_date)
    td    = re.sub(r"[^0-9]", "", to_date)
    fname = f"BSE_{index_name}_{fd}_{td}.csv"

    if s3_bucket:
        import boto3
        key = f"{s3_prefix.rstrip('/')}/{fname}"
        boto3.client("s3").put_object(
            Bucket=s3_bucket,
            Key=key,
            Body=df.to_csv(index=False).encode("utf-8"),
            ContentType="text/csv",
        )
        uri = f"s3://{s3_bucket}/{key}"
        print(f"✓ {index_name} → {uri}")
        return uri
    else:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, fname)
        df.to_csv(path, index=False)
        print(f"✓ {index_name} → {path}")
        return path


def download_all_indices(
    date: str,
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "bse-index-data/",
) -> str:
    """
    Download all BSE indices for a single date to local file or S3.

    Args:
        date:       "YYYY-MM-DD" or "YYYYMMDD"
        output_dir: Local directory
        s3_bucket:  S3 bucket name
        s3_prefix:  S3 key prefix

    Returns:
        Local file path or "s3://bucket/key"
    """
    df    = get_all_indices(date)
    d     = re.sub(r"[^0-9]", "", date)
    fname = f"BSE_all_indices_{d}.csv"

    if s3_bucket:
        import boto3
        key = f"{s3_prefix.rstrip('/')}/{fname}"
        boto3.client("s3").put_object(
            Bucket=s3_bucket,
            Key=key,
            Body=df.to_csv(index=False).encode("utf-8"),
            ContentType="text/csv",
        )
        uri = f"s3://{s3_bucket}/{key}"
        print(f"✓ BSE all indices {date} → {uri}")
        return uri
    else:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, fname)
        df.to_csv(path, index=False)
        print(f"✓ BSE all indices {date} → {path}")
        return path
