"""
nse-data — Python library to download market data from NSE India.

Modules:
    indices  — Historical index data (Price + TRI) from niftyindices.com
    reports  — Daily reports from nseindia.com/all-reports (bhavcopy, bhav, etc.)

Quick Start:
    from nsedata import indices, reports

    # Get NIFTY 50 historical OHLC
    df = indices.get_historical("NIFTY 50", "01-Apr-2026", "15-May-2026")

    # Get NIFTY 50 Total Return Index
    df = indices.get_tri("NIFTY 50", "01-Apr-2026", "15-May-2026")

    # Download bhavcopy for a date
    df = reports.get_bhavcopy("2026-04-17")

    # Download sec_bhavdata_full
    df = reports.get_sec_bhavdata("2026-04-17")
"""

__version__ = "0.1.0"

from nsedata.indices import get_historical, get_tri
from nsedata.reports import (
    get_bhavcopy,
    get_ind_close_all,
    get_market_activity,
    get_sec_bhavdata,
)
