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

    if df is None or (hasattr(df, "empty") and df.empty):
        # Return empty polars DataFrame preserving columns if possible
        try:
            import polars as pl
            if hasattr(df, "columns"):
                return pl.DataFrame({c: [] for c in df.columns})
            return pl.DataFrame()
        except ImportError:
            return df

    try:
        import polars as pl
        return pl.from_pandas(df)
    except ImportError:
        raise ImportError(
            "polars is not installed. Install it with: pip install nse-archives[polars]"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to convert to polars DataFrame: {e}") from e
