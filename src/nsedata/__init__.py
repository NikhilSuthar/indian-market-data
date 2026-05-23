"""
nse-data — Python library to download market data from NSE India.

Primary API (v0.5.0+):
    from nsedata import nse

    # Get any dataset as DataFrame
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
    df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
    df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

    # Download to local disk or S3
    path   = nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22",
                           output_dir="./data")
    s3_uri = nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
                           s3_bucket="my-bucket", s3_prefix="raw/nse/")

    # List all available datasets
    nse.list_datasets()

Legacy API (v0.3.x/v0.4.x — still works):
    from nsedata import reports
    df = reports.get("sec_bhavdata_full", "2026-05-22")
"""

__version__ = "0.5.0"

# Primary API
from nsedata import nse

# Legacy compatibility
from nsedata import reports
