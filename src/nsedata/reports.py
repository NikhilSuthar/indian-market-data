"""
NSE Daily Reports — Bhavcopy and other daily files from nseindia.com/all-reports.

Data source: https://www.nseindia.com/all-reports

Functions:
    get_bhavcopy(date) → DataFrame
    get_sec_bhavdata(date) → DataFrame
    get_ind_close_all(date) → DataFrame
    get_market_activity(date) → DataFrame
    download_report(report_type, date, output_dir) → Path
"""

import io
import os
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

from nsedata.session import create_nse_session

NSE_ARCHIVES = "https://nsearchives.nseindia.com"

# URL patterns for various reports
REPORT_PATTERNS = {
    "pr": "/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip",
    "sec_bhavdata_full": "/products/content/sec_bhavdata_full_{ddmmyyyy}.csv",
    "bhav_copy": "/content/historical/EQUITIES/2026/{MON}/cm{ddMONyyyy}bhav.csv.zip",
    "ind_close_all": "/content/indices/ind_close_all_{ddmmyyyy}.csv",
    "market_activity": "/archives/equities/market-activity/MA{ddmmyy}.csv",
}


def get_bhavcopy(date: str) -> pd.DataFrame:
    """
    Download and parse the PR (Price Record) bhavcopy zip for a given date.

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with OHLC data for all securities.

    Example:
        >>> from nsedata import reports
        >>> df = reports.get_bhavcopy("2026-04-17")
        >>> df.head()
    """
    dt = _parse_date(date)
    session = create_nse_session()

    url = NSE_ARCHIVES + REPORT_PATTERNS["pr"].format(ddmmyy=dt.strftime("%d%m%y"))
    resp = session.get(url, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to download PR file: HTTP {resp.status_code} for {url}")

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
        df = pd.read_csv(io.BytesIO(zf.read(csv_name)))

    df.columns = [c.strip() for c in df.columns]
    return df


def get_sec_bhavdata(date: str) -> pd.DataFrame:
    """
    Download sec_bhavdata_full CSV — full security-wise bhavcopy with delivery data.

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with columns: SYMBOL, SERIES, OPEN_PRICE, HIGH_PRICE, LOW_PRICE,
        CLOSE_PRICE, LAST_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS,
        NO_OF_TRADES, DELIV_QTY, DELIV_PER, etc.

    Example:
        >>> from nsedata import reports
        >>> df = reports.get_sec_bhavdata("2026-04-17")
        >>> df[df["SYMBOL"] == "RELIANCE"]
    """
    dt = _parse_date(date)
    session = create_nse_session()

    url = NSE_ARCHIVES + REPORT_PATTERNS["sec_bhavdata_full"].format(
        ddmmyyyy=dt.strftime("%d%m%Y")
    )
    resp = session.get(url, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to download sec_bhavdata: HTTP {resp.status_code} for {url}")

    df = pd.read_csv(io.StringIO(resp.text))
    df.columns = [c.strip() for c in df.columns]
    return df


def get_pr_file(date: str) -> pd.DataFrame:
    """Alias for get_bhavcopy — downloads the PR zip file."""
    return get_bhavcopy(date)


def get_ind_close_all(date: str) -> pd.DataFrame:
    """
    Download ind_close_all CSV — closing values for all indices on a given date.

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with columns: Index Name, Index Date, Open Index Value,
        High Index Value, Low Index Value, Closing Index Value, etc.

    Example:
        >>> from nsedata import reports
        >>> df = reports.get_ind_close_all("2026-04-17")
        >>> df[df["Index Name"] == "Nifty 50"]
    """
    dt = _parse_date(date)
    session = create_nse_session()

    url = NSE_ARCHIVES + REPORT_PATTERNS["ind_close_all"].format(
        ddmmyyyy=dt.strftime("%d%m%Y")
    )
    resp = session.get(url, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to download ind_close_all: HTTP {resp.status_code} for {url}")

    df = pd.read_csv(io.StringIO(resp.text))
    df.columns = [c.strip() for c in df.columns]
    return df


def get_market_activity(date: str) -> pd.DataFrame:
    """
    Download Market Activity report (MA file).

    Args:
        date: Date string in YYYY-MM-DD format e.g. "2026-04-17"

    Returns:
        DataFrame with market activity data.
    """
    dt = _parse_date(date)
    session = create_nse_session()

    url = NSE_ARCHIVES + REPORT_PATTERNS["market_activity"].format(
        ddmmyy=dt.strftime("%d%m%y")
    )
    resp = session.get(url, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to download MA file: HTTP {resp.status_code} for {url}")

    df = pd.read_csv(io.StringIO(resp.text))
    df.columns = [c.strip() for c in df.columns]
    return df


def download_report(report_type: str, date: str, output_dir: str = ".") -> Path:
    """
    Download any report type and save the raw file to disk.

    Args:
        report_type: One of "pr", "sec_bhavdata_full", "ind_close_all", "market_activity"
        date: Date string in YYYY-MM-DD format
        output_dir: Directory to save the file (default: current directory)

    Returns:
        Path to the saved file.

    Example:
        >>> from nsedata import reports
        >>> path = reports.download_report("sec_bhavdata_full", "2026-04-17", "./data")
    """
    dt = _parse_date(date)
    session = create_nse_session()

    if report_type not in REPORT_PATTERNS:
        raise ValueError(
            f"Unknown report type: {report_type}. "
            f"Available: {list(REPORT_PATTERNS.keys())}"
        )

    pattern = REPORT_PATTERNS[report_type]
    url = NSE_ARCHIVES + pattern.format(
        ddmmyy=dt.strftime("%d%m%y"),
        ddmmyyyy=dt.strftime("%d%m%Y"),
        ddMONyyyy=dt.strftime("%d%b%Y").upper(),
        MON=dt.strftime("%b").upper(),
    )

    resp = session.get(url, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to download {report_type}: HTTP {resp.status_code} for {url}"
        )

    os.makedirs(output_dir, exist_ok=True)
    filename = url.split("/")[-1]
    out_path = Path(output_dir) / filename

    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path


def _parse_date(date: str) -> datetime:
    """Parse YYYY-MM-DD date string."""
    return datetime.strptime(date, "%Y-%m-%d")
