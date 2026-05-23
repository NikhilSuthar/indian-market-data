"""
nse-data — Download NSE India market data as pandas DataFrames.

Quick Start:
    from nsedata import nse

    # Get any dataset as DataFrame
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
    df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
    df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

    # Download to disk or S3
    nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22",
                 output_dir="./data")

    # List all available datasets
    nse.list_datasets()

See: https://NikhilSuthar.github.io/nse-data for full documentation.
"""

__version__ = "0.5.0"

from nsedata import nse
