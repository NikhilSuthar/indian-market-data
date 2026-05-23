"""
nse-data public API — clean, hierarchical interface.

Usage:
    from nsedata import nse

    # Get as DataFrame
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
    df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
    df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")
    df = nse.get("debt", "tri_party_repo", "trm_bc", "2026-05-22")

    # Download raw file (local)
    path = nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22",
                        output_dir="./data")

    # Download raw file to S3 (IAM role — no credentials needed in Lambda)
    s3_uri = nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
                          s3_bucket="my-bucket", s3_prefix="raw/nse/")

    # List all available datasets
    nse.list_datasets()
    nse.list_datasets(category="capital_market")
    nse.list_datasets(category="derivatives", subcategory="equity")
"""

from typing import Optional
import pandas as pd

from nsedata.registry import REGISTRY, DatasetConfig, get_config, list_datasets
from nsedata.fetcher import (
    _build_session, _format_url, fetch_bytes, parse_to_df, save_file
)


def get(
    category: str,
    subcategory: str,
    dataset: str,
    date: str,
    **kwargs,
) -> pd.DataFrame:
    """
    Download and return a dataset as a pandas DataFrame.

    Args:
        category:    Top-level category.
                     Options: "capital_market", "derivatives", "debt", "egr"
        subcategory: Sub-section within the category.
                     Examples: "equities_sme", "indices", "slb", "equity", "commodity",
                               "currency", "interest_rate", "corporate", "debt_segment",
                               "tri_party_repo", "mutual_fund"
        dataset:     Dataset key.
                     See list_datasets() for all available keys.
        date:        Date string.
                     - "YYYY-MM-DD" for daily datasets (e.g. "2026-05-22")
                     - "YYYY-MM" for monthly datasets (e.g. "2026-05")
        **kwargs:    Extra params for specific datasets:
                     - snapshot=1..6 for cvar1 (VaR margin file snapshots)
                     - settno=<settlement_no> for auction_buy

    Returns:
        pandas.DataFrame

    Raises:
        ValueError: If dataset is download-only (use download() instead)
        RuntimeError: If download fails (non-trading day, NSE unavailable)

    Examples:
        >>> df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
        >>> df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
        >>> df = nse.get("capital_market", "equities_sme", "cmvolt", "2026-05-22")
        >>> df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")
        >>> df = nse.get("derivatives", "equity", "fo_contract", "2026-05-22")
        >>> df = nse.get("debt", "tri_party_repo", "trm_bc", "2026-05-22")
        >>> df = nse.get("debt", "corporate", "cbm_trd", "2026-05-22")
        >>> df = nse.get("capital_market", "slb", "slb_cli", "2026-05")  # monthly
    """
    cfg = get_config(category, subcategory, dataset)

    if cfg.download_only or not cfg.df_supported:
        raise ValueError(
            f"'{dataset}' does not support DataFrame output (format: {cfg.file_format}). "
            f"Use nse.download() to save the raw file."
        )

    url = _format_url(cfg, date, **kwargs)
    session = _build_session()
    content = fetch_bytes(url, session)
    return parse_to_df(content, cfg)


def download(
    category: str,
    subcategory: str,
    dataset: str,
    date: str,
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "",
    **kwargs,
) -> str:
    """
    Download a dataset and save to local disk or S3.

    Works for ALL dataset types including download-only ones (DAT, PDF, SPN, LST).
    By default, also works for all datasets that support DataFrame — DataFrame-supported
    datasets are always also downloadable.

    Args:
        category:    e.g. "capital_market", "derivatives", "debt"
        subcategory: e.g. "equities_sme", "equity", "slb"
        dataset:     e.g. "sec_bhavdata_full", "bhavcopy_pr", "cvar1"
        date:        "YYYY-MM-DD" or "YYYY-MM"
        output_dir:  Local directory (default: current). Ignored if s3_bucket is set.
        s3_bucket:   S3 bucket name. Uses IAM role — no credentials needed in Lambda.
        s3_prefix:   S3 key prefix (e.g. "raw/nse/equities/")
        **kwargs:    snapshot=1..6 for cvar1, settno=xxx for auction_buy

    Returns:
        str: Local file path or "s3://bucket/key"

    Examples:
        # Download to local disk
        >>> path = nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22",
        ...                     output_dir="./data")

        # Download to S3 (Lambda with IAM role)
        >>> uri = nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
        ...                    s3_bucket="my-bucket", s3_prefix="nse/equities/")
        ... # Returns: "s3://my-bucket/nse/equities/sec_bhavdata_full_22052026.csv"

        # Download-only dataset (VaR margin DAT file)
        >>> path = nse.download("capital_market", "equities_sme", "cvar1", "2026-05-22",
        ...                     snapshot=1, output_dir="./data")
    """
    cfg = get_config(category, subcategory, dataset)
    url = _format_url(cfg, date, **kwargs)
    session = _build_session()
    content = fetch_bytes(url, session)

    # Derive filename from URL
    filename = url.split("/")[-1]

    return save_file(content, filename, output_dir, s3_bucket, s3_prefix)


def download_all(
    date: str,
    categories: Optional[list] = None,
    output_dir: str = ".",
    s3_bucket: Optional[str] = None,
    s3_prefix: str = "nse/",
    df_only: bool = False,
) -> dict:
    """
    Download all (or a subset of) datasets for a given date.

    Args:
        date:       "YYYY-MM-DD"
        categories: List of categories to include, e.g. ["capital_market", "debt"].
                    None = all categories.
        output_dir: Local directory (ignored if s3_bucket is set)
        s3_bucket:  S3 bucket for uploads
        s3_prefix:  S3 key prefix
        df_only:    If True, only download datasets that support DataFrame

    Returns:
        dict with "uploaded" and "failed" lists.
    """
    import time
    results = {"uploaded": [], "failed": []}

    all_ds = list_datasets()
    if categories:
        all_ds = [d for d in all_ds if d["category"] in categories]
    if df_only:
        all_ds = [d for d in all_ds if d["df_supported"]]

    for ds in all_ds:
        cat, sub, key = ds["category"], ds["subcategory"], ds["dataset"]
        cfg = get_config(cat, sub, key)

        # Skip monthly datasets for a daily date call
        if cfg.date_type == "monthly" and len(date) == 10:
            continue
        # Skip static datasets — downloaded once
        if cfg.date_type == "static":
            date_arg = date  # use as-is, will be ignored
        else:
            date_arg = date

        try:
            prefix = f"{s3_prefix}{date}/{cat}/{sub}/" if s3_bucket else output_dir
            uri = download(cat, sub, key, date_arg,
                           output_dir=prefix,
                           s3_bucket=s3_bucket,
                           s3_prefix=f"{s3_prefix}{date}/{cat}/{sub}/" if s3_bucket else "")
            results["uploaded"].append({"dataset": f"{cat}/{sub}/{key}", "uri": uri})
            time.sleep(0.3)  # Gentle rate limiting
        except Exception as e:
            results["failed"].append({"dataset": f"{cat}/{sub}/{key}", "error": str(e)[:80]})

    return results


def list_datasets(category: str = None, subcategory: str = None) -> pd.DataFrame:
    """
    List all available datasets as a DataFrame.

    Args:
        category:    Filter by category (optional)
        subcategory: Filter by subcategory (optional)

    Returns:
        DataFrame with columns: category, subcategory, dataset, name, frequency,
                                df_supported, format, description

    Example:
        >>> nse.list_datasets()
        >>> nse.list_datasets(category="capital_market")
        >>> nse.list_datasets(category="derivatives", subcategory="equity")
    """
    from nsedata.registry import list_datasets as _list
    rows = _list(category, subcategory)
    # Add description
    for row in rows:
        cfg = get_config(row["category"], row["subcategory"], row["dataset"])
        row["description"] = cfg.description[:80]
        row["key_columns"] = cfg.columns[:60]
    return pd.DataFrame(rows)


def get_config_info(category: str, subcategory: str, dataset: str) -> dict:
    """
    Get full configuration info for a dataset.

    Returns:
        dict with all DatasetConfig fields
    """
    cfg = get_config(category, subcategory, dataset)
    return {
        "name": cfg.name,
        "description": cfg.description,
        "url_pattern": cfg.base_url + cfg.url_pattern,
        "file_pattern": cfg.file_pattern,
        "file_format": cfg.file_format,
        "date_type": cfg.date_type,
        "df_supported": cfg.df_supported and not cfg.download_only,
        "download_only": cfg.download_only,
        "skip_rows": cfg.skip_rows,
        "encoding": cfg.encoding,
        "frequency": cfg.frequency,
        "columns": cfg.columns,
    }
