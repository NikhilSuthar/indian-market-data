"""
Optional Polars conversion utility for mcx-data.
See nsedata.dataframe for full documentation.

Usage:
    import os
    os.environ["IMD_DATAFRAME"] = "polars"
    from mcxdata import mcx
    df = mcx.get_spot_recent()   # returns polars.DataFrame
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def _use_polars() -> bool:
    return os.environ.get("IMD_DATAFRAME", "pandas").lower() == "polars"


def to_output_frame(df: "pd.DataFrame") -> object:
    if not _use_polars():
        return df

    # Import polars first — only this should raise the "not installed" error.
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "polars is not installed. Install it with: pip install mcx-data[polars]"
        )

    if df is None:
        return pl.DataFrame()
    if hasattr(df, "empty") and df.empty:
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
