"""
msci-data — Download MSCI index levels as pandas DataFrames.

Pulls end-of-day index levels from MSCI's public levels API (the same
one that powers the charts on https://www.msci.com/indexes). No API key.

Quick Start:
    from mscidata import msci

    # Single index, date range — Net Total Return in USD
    df = msci.get_levels("990100", "2026-01-01", "2026-07-01")

    # Price Return variant
    df = msci.get_levels("990100", "2026-01-01", "2026-07-01", variant="price")

    # Gross Total Return
    df = msci.get_levels("990100", "2026-01-01", "2026-07-01", variant="gross")

    # Multiple index codes in one call
    df = msci.get_levels(["990100", "664185"], "2026-01-01", "2026-07-01")

    # Single date
    df = msci.get_levels("990100", "2026-07-03")

    # List supported variants
    msci.list_variants()

    # Download to local file or S3
    msci.download("990100", "2026-01-01", "2026-07-01", output_dir="./data")

Columns returned:
    INDEX_CODE, VARIANT, RETURN_TYPE, CURRENCY, DATE, LEVEL

MSCI Index Code examples:
    990100  — MSCI World (USD)
    891800  — MSCI ACWI (USD)
    664185  — MSCI Emerging Markets (USD)
    106220  — MSCI India (USD)
    929887  — MSCI USA (USD)

See: https://NikhilSuthar.github.io/indian-market-data
"""

__version__ = "1.0.0"

from mscidata import msci
