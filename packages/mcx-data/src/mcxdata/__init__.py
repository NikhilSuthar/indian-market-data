"""
mcx-data — Python library to download market data from MCX India.

MCX (Multi Commodity Exchange) is India's largest commodity derivatives exchange.

Quick Start:
    from mcxdata import mcx

    # Get any dataset as DataFrame
    df = mcx.get("commodity", "bhavcopy", "2026-05-22")

    # Download to S3
    mcx.download("commodity", "bhavcopy", "2026-05-22",
                  s3_bucket="my-bucket", s3_prefix="raw/mcx/")

    # List all available datasets
    mcx.list_datasets()

See: https://NikhilSuthar.github.io/india-market-data/mcx
"""

__version__ = "0.1.0"

from mcxdata import mcx
