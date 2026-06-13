"""
bse-data — Download BSE India market data as pandas DataFrames.

BSE (Bombay Stock Exchange) is India's oldest stock exchange.
This library provides historical and live data for all BSE indices
including SENSEX, BSE500, BANKEX and 50+ more.

Quick Start:
    from bsedata import bse

    # Historical SENSEX OHLC
    df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")

    # Historical BSE500
    df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")

    # All indices for one date (single call)
    df = bse.get_all_indices("2026-05-22")

    # Live SENSEX quote
    df = bse.get_live_sensex()

    # Download to S3 (Lambda with IAM role)
    bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                       s3_bucket="my-bucket", s3_prefix="raw/bse/")

    # List all 50+ supported indices
    bse.list_indices()
    bse.list_indices(category="Sectoral")

See: https://NikhilSuthar.github.io/indian-market-data
"""

__version__ = "1.1.1"

from bsedata import bse
