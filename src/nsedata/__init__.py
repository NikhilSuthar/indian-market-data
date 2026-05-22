"""
nse-data — Python library to download market data from NSE India.

Module:
    reports  — Daily reports from nsearchives.nseindia.com (bhavcopy, bhav, indices, etc.)

Quick Start:
    from nsedata import reports

    # Download bhavcopy for a date
    df = reports.get_bhavcopy("2026-04-17")

    # Download sec_bhavdata_full
    df = reports.get_sec_bhavdata("2026-04-17")

    # All index closing values
    df = reports.get_ind_close_all("2026-04-17")

    # Market activity
    df = reports.get_market_activity("2026-04-17")
"""

__version__ = "0.2.2"

from nsedata.reports import (
    REPORT_PATTERNS,
    download_report,
    get,
    get_bhavcopy,
    get_ind_close_all,
    get_market_activity,
    get_sec_bhavdata,
)
