"""
nse-data — Python library to download market data from NSE India.

Module:
    reports  — Daily reports from nsearchives.nseindia.com

Quick Start:
    from nsedata import reports

    # Get any report as DataFrame
    df = reports.get("sec_bhavdata_full", "2026-05-19")
    df = reports.get("ind_close_all", "2026-05-19")
    df = reports.get("cmvolt", "2026-05-19")

    # Download raw file to S3
    uri = reports.download_report("security_master", "2026-05-19",
                                  s3_bucket="my-bucket", s3_prefix="nse/")
"""

__version__ = "0.3.1"

from nsedata.reports import (
    REPORT_PATTERNS,
    download_report,
    get,
    get_bhavcopy,
    get_ind_close_all,
    get_market_activity,
    get_sec_bhavdata,
)
