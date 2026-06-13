"""
Optional Polars conversion utility for bse-index-data.
See nsedata.dataframe for full documentation.

Usage:
    import os
    os.environ["IMD_DATAFRAME"] = "polars"
    from bsedata import bse
    df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")   # returns polars.DataFrame
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
    if df is None or (hasattr(df, "empty") and df.empty):
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
            "polars is not installed. Install it with: pip install bse-index-data[polars]"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to convert to polars DataFrame: {e}") from e
