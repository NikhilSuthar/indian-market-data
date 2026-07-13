"""
msci-data public API.

Usage:
    from mscidata import msci

    # Single index, date range (Net Total Return by default)
    df = msci.get_levels("990100", "2026-01-01", "2026-07-01")

    # Choose return variant
    df = msci.get_levels("990100", "2026-01-01", "2026-07-01", variant="price")
    df = msci.get_levels("990100", "2026-01-01", "2026-07-01", variant="gross")

    # Multiple index codes — concatenated into one DataFrame
    df = msci.get_levels(["990100", "664185"], "2026-01-01", "2026-07-01")

    # Single date
    df = msci.get_levels("990100", "2026-07-03")

    # List supported variants
    msci.list_variants()

    # Download to local file or S3
    msci.download("990100", "2026-01-01", "2026-07-01", output_dir="./data")
    msci.download(["990100", "664185"], "2026-01-01", "2026-07-01",
                  s3_bucket="my-bucket", s3_prefix="raw/msci/")

Common MSCI index codes:
    990100 — MSCI World          (Developed Markets)
    891800 — MSCI ACWI           (All Country World)
    664185 — MSCI Emerging Markets
    106220 — MSCI India
    929887 — MSCI USA
    990300 — MSCI EAFE           (Europe, Australasia, Far East)
"""

from __future__ import annotations

import datetime as dt
import os
import re
from typing import Optional, Union

import pandas as pd

from mscidata.fetcher import fetch_levels, VARIANT_LABEL, VARIANT_ALIAS, norm_variant


# ── Public API ────────────────────────────────────────────────────────────────

def list_variants() -> pd.DataFrame:
    """
    List all supported return variants.

    Returns:
        DataFrame — variant_code, return_type, aliases

    Example:
        msci.list_variants()
    """
    alias_map: dict[str, list[str]] = {}
    for alias, code in VARIANT_ALIAS.items():
        alias_map.setdefault(code, []).append(alias)

    rows = []
    for code, label in VARIANT_LABEL.items():
        aliases = sorted(a for a in alias_map.get(code, []) if a != code)
        rows.append({
            "variant_code": code,
            "return_type":  label,
            "aliases":      ", ".join(aliases),
        })
    return pd.DataFrame(rows)


def get_levels(
    index_codes: Union[str, list[str]],
    from_date: str,
    to_date: str = None,
    variant: str = "NETR",
) -> pd.DataFrame:
    """
    Get end-of-day index levels for one or more MSCI index codes.

    Args:
        index_codes: Single MSCI numeric index code or list of codes.
                     e.g. "990100" (MSCI World) or ["990100", "664185"]
        from_date:   Start date — "YYYY-MM-DD" or "YYYYMMDD"
        to_date:     End date   — "YYYY-MM-DD" or "YYYYMMDD".
                     Defaults to from_date (single day).
        variant:     Return variant (default "NETR"):
                       "STRD" / "price" / "pr"    → Price Return
                       "NETR" / "net"  / "ntr"    → Net Total Return  (default)
                       "GRTR" / "gross"/ "tr"     → Gross Total Return

    Returns:
        DataFrame — INDEX_CODE, VARIANT, RETURN_TYPE, CURRENCY, DATE, LEVEL

    Raises:
        ValueError:   Unknown variant or empty index_codes.
        RuntimeError: API fetch failed after retries.

    Examples:
        # MSCI World — net return, date range
        df = msci.get_levels("990100", "2026-01-01", "2026-07-01")

        # MSCI India — price return
        df = msci.get_levels("106220", "2026-01-01", "2026-07-01", variant="price")

        # Multiple indices — all net return
        df = msci.get_levels(["990100", "664185"], "2026-01-01", "2026-07-01")

        # Single date
        df = msci.get_levels("990100", "2026-07-03")
    """
    start = _parse_date(from_date)
    end   = _parse_date(to_date) if to_date else start

    if end < start:
        raise ValueError(f"to_date ({to_date}) must be >= from_date ({from_date})")

    return fetch_levels(
        index_codes=index_codes,
        start_date=start,
        end_date=end,
        variant=variant,
    )


def download(
    index_codes: Union[str, list[str]],
    from_date: str,
    to_date: str = None,
    variant: str = "NETR",
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "msci-data/",
) -> str:
    """
    Download MSCI index levels to a local CSV or S3.

    Args:
        index_codes: Single code or list of MSCI numeric index codes.
        from_date:   "YYYY-MM-DD" or "YYYYMMDD"
        to_date:     "YYYY-MM-DD" or "YYYYMMDD". Defaults to from_date.
        variant:     Return variant — "NETR" (default), "STRD", "GRTR"
        output_dir:  Local directory (used when s3_bucket is None).
        s3_bucket:   S3 bucket name (if saving to S3).
        s3_prefix:   S3 key prefix (default "msci-data/").

    Returns:
        Local file path or "s3://bucket/key"

    Examples:
        # Local CSV
        path = msci.download("990100", "2026-01-01", "2026-07-01")

        # S3 (Lambda with IAM role)
        uri = msci.download(["990100", "664185"], "2026-01-01", "2026-07-01",
                             s3_bucket="my-bucket", s3_prefix="raw/msci/")
    """
    df = get_levels(index_codes, from_date, to_date, variant)

    api_variant = norm_variant(variant)
    if isinstance(index_codes, str):
        code_str = index_codes
    else:
        code_str = "_".join(str(c) for c in index_codes)

    fd    = re.sub(r"[^0-9]", "", from_date)
    td    = re.sub(r"[^0-9]", "", to_date or from_date)
    fname = f"MSCI_{code_str}_{api_variant}_{fd}_{td}.csv"

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
        print(f"✓ MSCI {code_str} {api_variant} → {uri}")
        return uri
    else:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, fname)
        df.to_csv(path, index=False)
        print(f"✓ MSCI {code_str} {api_variant} → {path}")
        return path


# ── Internal helpers ──────────────────────────────────────────────────────────

def _parse_date(date_str: str) -> dt.date:
    """Accept YYYY-MM-DD or YYYYMMDD → return datetime.date."""
    s = date_str.strip().replace("-", "")
    if len(s) == 8 and s.isdigit():
        return dt.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    raise ValueError(
        f"Unrecognised date format: '{date_str}'. Use YYYY-MM-DD or YYYYMMDD."
    )
