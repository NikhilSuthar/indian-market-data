"""
indian-market-data — Umbrella package for NSE and MCX India market data.

Download NSE bhavcopy, Nifty indices, F&O, equity, debt, commodity, currency
derivatives as pandas DataFrames. Installs and re-exports both nse-data and mcx-data.
Works on AWS Lambda and Snowflake.

Keywords: nse, mcx, nifty, india, bhavcopy, nse-india, mcx-india, stock-market,
commodity, equity, derivatives, market-data, financial-data, pandas, nifty50,
nseindia, trading, historical-data, aws-lambda, s3, snowflake

Usage:
    from indianmarketdata import nse, mcx

    # NSE data
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")

    # MCX data (coming soon)
    df = mcx.get("commodity", "bhavcopy", "2026-05-22")

Or use packages individually:
    from nsedata import nse      # pip install nse-data
    from mcxdata import mcx      # pip install mcx-data
"""

__version__ = "0.9.0"

# Re-export both sub-packages
try:
    from nsedata import nse
except ImportError:
    nse = None  # type: ignore

try:
    from mcxdata import mcx
except ImportError:
    mcx = None  # type: ignore

__all__ = ["nse", "mcx"]
