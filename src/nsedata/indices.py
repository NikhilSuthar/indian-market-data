"""
NSE Index Historical Data — Price Index and Total Return Index.

Data source: https://niftyindices.com/reports/historical-data

Functions:
    get_historical(index_name, start_date, end_date) → DataFrame
    get_tri(index_name, start_date, end_date) → DataFrame
"""

import json

import pandas as pd

from nsedata.session import create_niftyindices_session

BASE_URL = "https://niftyindices.com"
API_ENDPOINTS = {
    "price": f"{BASE_URL}/Backpage.aspx/getHistoricaldatatabletoString",
    "tri": f"{BASE_URL}/Backpage.aspx/getTotalReturnIndexString",
}


def get_historical(index_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical Price Index (OHLC) data for a given index.

    Args:
        index_name: Index name e.g. "NIFTY 50", "NIFTY BANK", "Nifty Auto"
        start_date: Start date in format dd-Mon-yyyy e.g. "01-Apr-2026"
        end_date:   End date in format dd-Mon-yyyy e.g. "15-May-2026"

    Returns:
        DataFrame with columns: Index Name, Date, Open, High, Low, Close

    Example:
        >>> from nsedata import indices
        >>> df = indices.get_historical("NIFTY 50", "01-Apr-2026", "15-May-2026")
        >>> df.head()
    """
    return _fetch(index_name, start_date, end_date, data_type="price")


def get_tri(index_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch Total Return Index (TRI) data for a given index.

    Args:
        index_name: Index name e.g. "NIFTY 50", "NIFTY BANK", "Nifty Auto"
        start_date: Start date in format dd-Mon-yyyy e.g. "01-Apr-2026"
        end_date:   End date in format dd-Mon-yyyy e.g. "15-May-2026"

    Returns:
        DataFrame with columns: Index Name, Date, Total Returns Index, Net Total Return Index

    Example:
        >>> from nsedata import indices
        >>> df = indices.get_tri("NIFTY 50", "01-Apr-2026", "15-May-2026")
        >>> df.head()
    """
    return _fetch(index_name, start_date, end_date, data_type="tri")


def _fetch(index_name: str, start_date: str, end_date: str, data_type: str) -> pd.DataFrame:
    """Internal: fetch data from niftyindices.com API."""
    session = create_niftyindices_session()
    api_url = API_ENDPOINTS[data_type]

    payload = {
        "cinfo": json.dumps({
            "name": index_name,
            "startDate": start_date,
            "endDate": end_date,
            "indexName": index_name,
        })
    }

    resp = session.post(api_url, json=payload, timeout=60)

    if resp.status_code != 200:
        raise RuntimeError(
            f"API returned HTTP {resp.status_code}: {resp.text[:300]}"
        )

    data = resp.json()
    if "d" not in data:
        raise RuntimeError(f"Unexpected response format: {str(data)[:200]}")

    records = json.loads(data["d"])
    df = pd.DataFrame(records)
    df.columns = [c.strip() for c in df.columns]

    # Column mapping
    col_map = {
        "indexName": "Index Name",
        "INDEX_NAME": "Index Name",
        "IndexName": "Index Name",
        "HistoricalDate": "Date",
        "OPEN": "Open",
        "HIGH": "High",
        "LOW": "Low",
        "CLOSE": "Close",
        "TotalReturnsIndex": "Total Returns Index",
        "NTR_Value": "Net Total Return Index",
    }
    df.rename(columns=col_map, inplace=True)

    # Drop junk columns
    for col in ["RequestNumber", "requestNumber"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Parse dates
    if "Date" in df.columns:
        df["Date"] = df["Date"].replace("", pd.NaT)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors="coerce")
        df = df.dropna(subset=["Date"])
        df.sort_values("Date", inplace=True)
        df.reset_index(drop=True, inplace=True)

    # Parse numeric columns
    numeric_cols = [
        "Open", "High", "Low", "Close",
        "Total Returns Index", "Net Total Return Index",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ""), errors="coerce"
            )

    # Keep only relevant columns
    possible_cols = [
        "Index Name", "Date", "Open", "High", "Low", "Close",
        "Total Returns Index", "Net Total Return Index",
    ]
    keep_cols = [c for c in possible_cols if c in df.columns]
    df = df[keep_cols]

    return df
