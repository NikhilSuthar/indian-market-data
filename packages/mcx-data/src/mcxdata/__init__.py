"""
mcx-data — Download MCX India commodity market data as pandas DataFrames.

MCX (Multi Commodity Exchange of India) is India's largest commodity exchange,
trading futures and options on metals, energy, and agri commodities.

Quick Start:
    from mcxdata import mcx

    # Today's spot prices (all commodities + locations)
    df = mcx.get_spot_recent()

    # Today's spot price for GOLD only
    df = mcx.get_spot_recent(commodity="GOLD")

    # Historical spot prices for a date range
    df = mcx.get_spot_archive("01/05/2026", "22/05/2026")
    df = mcx.get_spot_archive("01/05/2026", "22/05/2026", commodity="GOLD")

    # Generic API (mirrors nse-data pattern)
    df = mcx.get("spot", "market", "spot_recent")
    df = mcx.get("spot", "market", "spot_archive",
                 from_date="01/05/2026", to_date="22/05/2026", commodity="GOLD")

    # Download to S3
    mcx.download("spot", "market", "spot_recent",
                 s3_bucket="my-bucket", s3_prefix="raw/mcx/")

    # List all available datasets
    mcx.list_datasets()

    # List available commodity names
    mcx.list_commodities()

See: https://NikhilSuthar.github.io/indian-market-data
"""

__version__ = "1.1.1"

from mcxdata import mcx
