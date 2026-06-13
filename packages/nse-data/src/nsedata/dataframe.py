"""
Optional Polars conversion utility for nse-data.

By default all functions return pandas DataFrames.
Set the environment variable IMD_DATAFRAME=polars to get polars DataFrames instead.

Usage:
    import os
    os.environ["IMD_DATAFRAME"] = "polars"   # set before importing

    from nsedata import nse
    df = nse.get(...)   # returns polars.DataFrame

Requirements:
    pip install nse-archives[polars]   # installs polars
    pip install nse-archives           # pandas only (default)
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def _use_polars() -> bool:
    """Return True if polars output is requested via IMD_DATAFRAME env var."""
    return os.environ.get("IMD_DATAFRAME", "pandas").lower() == "polars"


def to_output_frame(df: "pd.DataFrame") -> object:
    """
    Convert a pandas DataFrame to the configured output format.

    If IMD_DATAFRAME=polars and polars is installed → returns polars.DataFrame
    Otherwise → returns pandas.DataFrame unchanged

    This is called as the LAST step in every public get() function.
    All internal logic stays in pandas.
    """
    if not _use_polars():
        return df

    # Import polars first — only this should raise the "not installed" error.
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "polars is not installed. Install it with: pip install nse-archives[polars]"
        )

    if df is None:
        return pl.DataFrame()
    if hasattr(df, "empty") and df.empty:
        # Return empty polars DataFrame preserving columns if possible
        if hasattr(df, "columns"):
            return pl.DataFrame({c: [] for c in df.columns})
        return pl.DataFrame()

    return _pandas_to_polars(pl, df)


def _pandas_to_polars(pl, df: "pd.DataFrame") -> object:
    """
    Convert a pandas DataFrame to polars without requiring pyarrow.

    polars.from_pandas() needs pyarrow whenever the frame has non-numpy
    columns (object/string, datetime, nullable extension dtypes). To keep
    the package dependency-light we try the fast path first, then fall back
    to a pyarrow-free conversion via a plain dict of Python lists.
    """
    try:
        return pl.from_pandas(df)
    except (ImportError, ModuleNotFoundError):
        data = {str(col): df[col].tolist() for col in df.columns}
        return pl.DataFrame(data)
    except Exception as e:
        raise RuntimeError(f"Failed to convert to polars DataFrame: {e}") from e
