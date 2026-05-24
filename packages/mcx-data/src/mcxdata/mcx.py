"""
mcx-data public API — mirrors nse-data pattern.

Usage:
    from mcxdata import mcx

    df = mcx.get("commodity", "bhavcopy", "2026-05-22")
    mcx.download("commodity", "bhavcopy", "2026-05-22", output_dir="./data")
    mcx.list_datasets()
"""

from typing import Optional
import pandas as pd

from mcxdata.registry import REGISTRY, get_config, list_datasets as _list_datasets


def get(category: str, subcategory: str, dataset: str, date: str, **kwargs) -> pd.DataFrame:
    """
    Download and return a MCX dataset as a pandas DataFrame.

    Args:
        category:    e.g. "commodity"
        subcategory: e.g. "futures", "options"
        dataset:     Dataset key — see list_datasets()
        date:        "YYYY-MM-DD" or "YYYY-MM"

    Returns:
        pandas.DataFrame
    """
    raise NotImplementedError(
        "mcx-data is under construction. MCX dataset URLs are being verified. "
        "Please check back in the next release."
    )


def download(category: str, subcategory: str, dataset: str, date: str,
             output_dir: str = ".", s3_bucket: Optional[str] = None,
             s3_prefix: str = "", **kwargs) -> str:
    """
    Download a MCX dataset to local disk or S3.
    """
    raise NotImplementedError(
        "mcx-data is under construction. MCX dataset URLs are being verified."
    )


def list_datasets(category: str = None) -> pd.DataFrame:
    """List all available MCX datasets."""
    rows = _list_datasets(category)
    if not rows:
        print("mcx-data: No datasets registered yet. MCX URLs are being verified.")
        return pd.DataFrame(columns=["category", "subcategory", "dataset", "name",
                                     "frequency", "df_supported", "format"])
    return pd.DataFrame(rows)
