"""
mcx-data public API.

Usage:
    from mcxdata import mcx

    # Today's spot prices (all commodities)
    df = mcx.get_spot_recent()
    df = mcx.get_spot_recent(commodity="GOLD")

    # Historical spot prices
    df = mcx.get_spot_archive("2026-05-01", "2026-05-22")
    df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")

    # Generic API (mirrors nse-data pattern)
    df = mcx.get("spot", "market", "spot_recent")
    df = mcx.get("spot", "market", "spot_archive",
                 from_date="2026-05-01", to_date="2026-05-22", commodity="GOLD")

    # Download to local file or S3
    mcx.download("spot", "market", "spot_recent", output_dir="./data")
    mcx.download("spot", "market", "spot_archive",
                 from_date="2026-05-01", to_date="2026-05-22",
                 s3_bucket="my-bucket", s3_prefix="raw/mcx/")

    # List datasets / commodities
    mcx.list_datasets()
    mcx.list_commodities()
"""

import os
import re
from datetime import datetime
from typing import Optional

import pandas as pd

from mcxdata.registry import list_datasets as _list_datasets
from mcxdata.fetcher import fetch_recent, fetch_archive
from mcxdata.dataframe import to_output_frame


# ── Public API ────────────────────────────────────────────────────────────────

def list_datasets(category: str = None) -> pd.DataFrame:
    """List all available MCX datasets."""
    rows = _list_datasets(category)
    return to_output_frame(pd.DataFrame(rows))


def list_commodities() -> list:
    """Return the 28 MCX commodity names from the spot market data directly."""
    import pandas as pd
    df = fetch_recent()  # always pandas internally
    return sorted(df["Commodity"].unique().tolist())


# ── Spot recent ───────────────────────────────────────────────────────────────

def get_spot_recent(commodity: str = "ALL", location: str = "ALL") -> pd.DataFrame:
    """
    Get today's spot prices for all (or one) MCX commodity.

    Args:
        commodity: "ALL" or name e.g. "GOLD", "SILVER", "CRUDEOIL"
        location:  "ALL" or location name

    Returns:
        DataFrame — Commodity, Unit, Location, Spot Price (Rs.), Up/Down

    Example:
        df = mcx.get_spot_recent()
        df = mcx.get_spot_recent(commodity="GOLD")
    """
    df = fetch_recent()

    if commodity and commodity.upper() != "ALL":
        mask = df["Commodity"].str.upper() == commodity.upper()
        df = df[mask].reset_index(drop=True)
    if location and location.upper() != "ALL":
        mask = df["Location"].str.upper() == location.upper()
        df = df[mask].reset_index(drop=True)

    return to_output_frame(df)


# ── Spot archive ──────────────────────────────────────────────────────────────

def get_spot_archive(
    from_date: str,
    to_date: str,
    commodity: str = "ALL",
    location: str = "ALL",
) -> pd.DataFrame:
    """
    Get historical spot prices from MCX archives.

    Args:
        from_date: "YYYY-MM-DD" or "DD/MM/YYYY"  e.g. "2026-05-01"
        to_date:   "YYYY-MM-DD" or "DD/MM/YYYY"  e.g. "2026-05-22"
        commodity: "ALL" or name e.g. "GOLD", "SILVER"
        location:  "ALL"

    Returns:
        DataFrame — Commodity, Unit, Location, Date, Spot Price (Rs.), Up/Down

    Example:
        df = mcx.get_spot_archive("2026-05-01", "2026-05-22")
        df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
    """
    fd = _to_ddmmyyyy(from_date)
    td = _to_ddmmyyyy(to_date)
    return to_output_frame(fetch_archive(fd, td, commodity=commodity, location=location))


# ── Generic get() — mirrors nse-data API pattern ──────────────────────────────

def get(
    category: str,
    subcategory: str,
    dataset: str,
    date: str = None,
    *,
    from_date: str = None,
    to_date:   str = None,
    commodity: str = "ALL",
    location:  str = "ALL",
    **kwargs,
) -> pd.DataFrame:
    """
    Generic dataset getter — mirrors nse-data's nse.get() signature.

    For recent:
        df = mcx.get("spot", "market", "spot_recent")

    For archive:
        df = mcx.get("spot", "market", "spot_archive",
                     from_date="2026-05-01", to_date="2026-05-22")
    """
    from mcxdata.registry import get_config
    cfg = get_config(category, subcategory, dataset)

    if cfg.date_type == "recent":
        return get_spot_recent(commodity=commodity, location=location)

    elif cfg.date_type == "range":
        if not from_date or not to_date:
            if date:
                from_date = from_date or date
                to_date   = to_date   or date
            else:
                raise ValueError(
                    f"'{dataset}' requires from_date and to_date.\n"
                    "Example: mcx.get('spot','market','spot_archive', "
                    "from_date='2026-05-01', to_date='2026-05-22')"
                )
        return get_spot_archive(from_date, to_date,
                                commodity=commodity, location=location)

    raise ValueError(f"Unsupported date_type '{cfg.date_type}' for '{dataset}'")


# ── download() — save to file or S3 ──────────────────────────────────────────

def download(
    category: str,
    subcategory: str,
    dataset: str,
    date: str = None,
    *,
    from_date: str = None,
    to_date:   str = None,
    commodity: str = "ALL",
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "mcx-data/",
    **kwargs,
) -> str:
    """
    Download MCX dataset and save to local file or S3.
    Returns the saved path or S3 URI.
    """
    df = get(category, subcategory, dataset, date,
             from_date=from_date, to_date=to_date,
             commodity=commodity, **kwargs)

    # Build filename
    ts = (to_date or from_date or date or datetime.today().strftime("%Y-%m-%d"))
    ts = re.sub(r"[^0-9]", "", ts)         # keep digits only → "20260522"
    safe_comm = commodity.replace(" ", "_").upper()
    fname = f"MCX_{dataset}_{safe_comm}_{ts}.csv"

    if s3_bucket:
        import boto3
        key = f"{s3_prefix.rstrip('/')}/{fname}"
        boto3.client("s3").put_object(
            Bucket=s3_bucket, Key=key,
            Body=df.to_csv(index=False).encode("utf-8"),
            ContentType="text/csv",
        )
        uri = f"s3://{s3_bucket}/{key}"
        print(f"✓ {dataset} → {uri}")
        return uri
    else:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, fname)
        df.to_csv(path, index=False)
        print(f"✓ {dataset} → {path}")
        return path


# ── Internal helpers ──────────────────────────────────────────────────────────

def _to_ddmmyyyy(date_str: str) -> str:
    """
    Accept YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, or YYYYMMDD
    → return DD/MM/YYYY (the format the MCX archive GET endpoint expects).
    """
    s = date_str.strip()
    if re.match(r'^\d{2}/\d{2}/\d{4}$', s):        # already DD/MM/YYYY
        return s
    if re.match(r'^\d{4}-\d{2}-\d{2}$', s):        # YYYY-MM-DD
        return datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")
    if re.match(r'^\d{8}$', s):                    # YYYYMMDD
        return datetime.strptime(s, "%Y%m%d").strftime("%d/%m/%Y")
    if re.match(r'^\d{2}-\d{2}-\d{4}$', s):        # DD-MM-YYYY
        return datetime.strptime(s, "%d-%m-%Y").strftime("%d/%m/%Y")
    raise ValueError(
        f"Unrecognised date format: '{date_str}'. "
        "Use YYYY-MM-DD, DD/MM/YYYY, or YYYYMMDD."
    )
