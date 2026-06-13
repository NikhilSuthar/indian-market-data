"""
nse-data — Download NSE India market data as pandas DataFrames.

Quick Start:
    from nsedata import nse

    # Daily NSE reports (works from Lambda/cloud)
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
    df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

    # Historical index data from niftyindices.com (works from residential IP)
    df = nse.get_historical_index("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
    df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")

    # Derive TRI from price data (works everywhere, approximate)
    tri_df = nse.derive_tri(price_df)

    # Download to S3
    nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
                 s3_bucket="my-bucket", s3_prefix="raw/nse/")

    # List all datasets
    nse.list_datasets()

See: https://NikhilSuthar.github.io/nse-data
"""

__version__ = "1.1.1"

from nsedata import nse
