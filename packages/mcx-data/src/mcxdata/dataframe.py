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
            "polars is not installed. Install it with: pip install mcx-data[polars]"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to convert to polars DataFrame: {e}") from e
