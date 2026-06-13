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
from nsedata.dataframe import to_output_frame
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
    return to_output_frame(parse_to_df(content, cfg))


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
    return to_output_frame(pd.DataFrame(rows))


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


# ─── niftyindices.com — Historical Index + TRI ────────────────────────────

def get_historical_index(
    index_name: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Fetch historical Price Index (OHLC) from niftyindices.com.

    Date format: "dd-Mon-yyyy" e.g. "01-Apr-2026"

    NOTE: niftyindices.com uses Cloudflare protection. Works reliably from
    residential IPs. May be blocked from AWS Lambda / cloud IPs.
    If blocked from Lambda, fetch locally → upload to S3 → Lambda reads from S3.

    Args:
        index_name: Index name e.g. "NIFTY 50", "NIFTY BANK"
                    Or shorthand: "nifty50", "niftybank", "niftyit"
        start_date: "dd-Mon-yyyy" e.g. "01-Apr-2026"
        end_date:   "dd-Mon-yyyy" e.g. "30-Apr-2026"

    Returns:
        DataFrame: Index Name, Date, Open, High, Low, Close

    Example:
        >>> from nsedata import nse
        >>> df = nse.get_historical_index("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
        >>> df = nse.get_historical_index("nifty50", "01-Jan-2026", "31-Mar-2026")
    """
    from nsedata.niftyindices import get_historical
    return to_output_frame(get_historical(index_name, start_date, end_date))


def get_tri(
    index_name: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Fetch Total Return Index (TRI) from niftyindices.com.

    TRI = Price Index + reinvested dividends. Essential for AMC benchmarking.

    Date format: "dd-Mon-yyyy" e.g. "01-Apr-2026"

    NOTE: niftyindices.com uses Cloudflare protection. Works reliably from
    residential IPs. May be blocked from AWS Lambda / cloud IPs.

    Args:
        index_name: Index name e.g. "NIFTY 50", "NIFTY BANK"
                    Or shorthand: "nifty50", "niftybank"
        start_date: "dd-Mon-yyyy"
        end_date:   "dd-Mon-yyyy"

    Returns:
        DataFrame: Index Name, Date, Total Returns Index, Net Total Return Index

    Columns:
        Total Returns Index    — Gross TRI (pre-tax dividend reinvestment)
        Net Total Return Index — Net TRI (post-15%-tax dividend reinvestment)

    Example:
        >>> from nsedata import nse
        >>> df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
        >>> df = nse.get_tri("niftybank", "01-Apr-2026", "30-Apr-2026")
    """
    from nsedata.niftyindices import get_tri as _get_tri
    return to_output_frame(_get_tri(index_name, start_date, end_date))


def derive_tri(
    price_df: pd.DataFrame,
    dividends: pd.DataFrame = None,
    base_date: str = None,
    base_value: float = 1000.0,
) -> pd.DataFrame:
    """
    Derive an approximate TRI from price index data.

    Use this when niftyindices.com is unavailable (e.g. from Lambda).
    Provide actual dividend records for accuracy, or it uses a 1.5%
    annual yield estimate.

    Formula:
        TRI(t) = TRI(t-1) × (Price(t) + Div(t)) / Price(t-1)

    Args:
        price_df:   DataFrame from get_historical_index() or ind_close_all()
                    Must have Date and Close (or Closing Index Value) columns.
        dividends:  Optional DataFrame with Date and Dividend columns.
                    Use corporate action records (bc{date}.csv from PR bundle).
        base_date:  Starting date (default: first date in price_df)
        base_value: Starting TRI value (default: 1000)

    Returns:
        DataFrame: Date, Close, Price_Return, Div_Return, Total_Return, Derived_TRI

    Example:
        >>> price_df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
        >>> nifty = price_df[price_df["Index Name"] == "Nifty 50"].rename(
        ...     columns={"Closing Index Value": "Close"})
        >>> tri_df = nse.derive_tri(nifty)
    """
    from nsedata.niftyindices import derive_tri as _derive_tri
    if "Closing Index Value" in price_df.columns and "Close" not in price_df.columns:
        price_df = price_df.rename(columns={"Closing Index Value": "Close"})
    return to_output_frame(_derive_tri(price_df, dividends, base_date, base_value))


def list_index_names() -> pd.DataFrame:
    """
    List all available index names for get_historical_index() and get_tri().

    Returns:
        DataFrame: shorthand, full_name
    """
    from nsedata.niftyindices import list_indices
    rows = list_indices()
    return pd.DataFrame(rows, columns=["shorthand", "full_name"])


def get_settlement_number(date: str) -> str:
    """
    Get the NSE settlement number for a given trading date.

    Settlement number = YYYY + 3-digit count of NSE trading days from Jan 1.
    This is used internally by auction_buy and csqr datasets.

    Args:
        date: "YYYY-MM-DD" e.g. "2026-05-22"

    Returns:
        str: Settlement number e.g. "2026094"

    Example:
        >>> nse.get_settlement_number("2026-05-22")
        '2026094'
        >>> nse.get_settlement_number("2026-04-17")
        '2026070'
    """
    from nsedata.calendar import get_settno_str
    return get_settno_str(date)
