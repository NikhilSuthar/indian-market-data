"""
indian-market-data — NSE + MCX India market data as pandas DataFrames.

Umbrella package that installs and re-exports both nse-data and mcx-data.
Works on AWS Lambda and Snowflake.

Quick Start:
    from indianmarketdata import nse, mcx

    # NSE — 91 datasets: equities, F&O, debt, indices, EGR
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
    df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
    df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")

    # MCX — commodity spot prices
    df = mcx.get_spot_recent()                                           # all 28 commodities
    df = mcx.get_spot_recent(commodity="GOLD")                          # single commodity
    df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")

    # Download to S3
    nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
                 s3_bucket="my-bucket", s3_prefix="raw/nse/")
    mcx.download("spot", "market", "spot_recent",
                 s3_bucket="my-bucket", s3_prefix="raw/mcx/")

Or use individually:
    from nsedata import nse      # pip install nse-data
    from mcxdata import mcx      # pip install mcx-data

See: https://NikhilSuthar.github.io/indian-market-data
"""

__version__ = "1.1.1"

try:
    from nsedata import nse
except ImportError:
    nse = None  # type: ignore

try:
    from bsedata import bse
except ImportError:
    bse = None  # type: ignore

try:
    from mcxdata import mcx
except ImportError:
    mcx = None  # type: ignore

__all__ = ["nse", "bse", "mcx"]
