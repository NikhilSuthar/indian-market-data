"""
BSE Data Fetcher — calls BSE India JSON API endpoints.

All endpoints are on api.bseindia.com — no WAF, plain requests works.
Session warmup (GET bseindia.com) is required to acquire cookies.
curl_cffi Chrome TLS impersonation is needed to pass BSE's bot check.

Confirmed endpoints (from browser devtools + BseIndiaApi reference):

  Historical index OHLC (CSV download):
    GET https://api.bseindia.com/BseIndiaAPI/api/ProduceCSVForDate/w
        ?strIndex=SENSEX&dtFromDate=DD/MM/YYYY&dtToDate=DD/MM/YYYY&period=D

  All indices for one date:
    GET https://api.bseindia.com/BseIndiaAPI/api/IndexArchDailyAll/w
        ?fmdt=DD/MM/YYYY&todt=DD/MM/YYYY&index=All&period=D

  Index names list:
    GET https://api.bseindia.com/BseIndiaAPI/api/FillddlIndex/w
        ?fmdt=&todt=

  Live SENSEX quote (no session needed):
    GET https://api.bseindia.com/RealTimeBseIndiaAPI/api/GetSensexData/w

Response format: CSV (historical) or JSON (all others).
"""

import re
from datetime import datetime
from typing import Optional

import pandas as pd

from bsedata.session import bse_get, BSE_API_BASE

# ── Endpoint URLs ─────────────────────────────────────────────────────────────
# Source: BseIndiaApi (BennyThadikaran) — GPL-3.0 reference only
# Our implementation is independent MIT-licensed code

_URL_INDEX_HISTORY   = f"{BSE_API_BASE}/BseIndiaAPI/api/ProduceCSVForDate/w"
_URL_ALL_INDICES_DAY = f"{BSE_API_BASE}/BseIndiaAPI/api/IndexArchDailyAll/w"
_URL_INDEX_NAMES     = f"{BSE_API_BASE}/BseIndiaAPI/api/FillddlIndex/w"
_URL_LIVE_SENSEX     = f"{BSE_API_BASE}/RealTimeBseIndiaAPI/api/GetSensexData/w"
_URL_INDEX_META      = f"{BSE_API_BASE}/BseIndiaAPI/api/Indexarchive_filedownload/w"


# ── Public fetch functions ────────────────────────────────────────────────────

def fetch_index_history(index_name: str, from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch historical OHLC for a BSE index over a date range.
    Uses ProduceCSVForDate endpoint — returns CSV file content.

    Args:
        index_name: BSE index name e.g. "SENSEX", "BSE500"
        from_date:  YYYYMMDD e.g. "20260101"
        to_date:    YYYYMMDD e.g. "20260522"

    Returns:
        DataFrame — Date, Open, High, Low, Close, Index Name
    """
    # Convert YYYYMMDD → DD/MM/YYYY (BSE format for this endpoint)
    fd_bse = f"{from_date[6:8]}/{from_date[4:6]}/{from_date[:4]}"
    td_bse = f"{to_date[6:8]}/{to_date[4:6]}/{to_date[:4]}"

    r = bse_get(_URL_INDEX_HISTORY, params={
        "strIndex":   index_name,
        "dtFromDate": fd_bse,
        "dtToDate":   td_bse,
        "period":     "D",
    })

    # Response is a CSV file
    import io
    text = r.text.strip()
    if not text:
        return pd.DataFrame()

    try:
        df = pd.read_csv(io.StringIO(text))
    except Exception:
        return pd.DataFrame()

    return _clean_index_history(df, index_name)


def fetch_all_indices_by_date(date: str) -> pd.DataFrame:
    """
    Fetch all BSE indices' closing values for a single date.
    Uses IndexArchDailyAll endpoint.

    Args:
        date: YYYYMMDD e.g. "20260522"

    Returns:
        DataFrame — Index Name, Date, Open, High, Low, Close, Change, Change %
    """
    # Convert YYYYMMDD → DD/MM/YYYY
    dt_bse = f"{date[6:8]}/{date[4:6]}/{date[:4]}"

    r = bse_get(_URL_ALL_INDICES_DAY, params={
        "fmdt":   dt_bse,
        "todt":   dt_bse,
        "index":  "All",
        "period": "D",
    })

    data = _parse_json(r)
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    return _clean_all_indices(df, date)


def fetch_index_names() -> list:
    """
    Fetch the list of all BSE index names available via the API.
    Uses FillddlIndex endpoint.

    Returns:
        List of index name strings
    """
    r    = bse_get(_URL_INDEX_NAMES, params={"fmdt": "", "todt": ""})
    data = _parse_json(r)
    if not data:
        return []

    names = []
    for item in data:
        if isinstance(item, dict):
            name = (item.get("IndexName") or item.get("indexName")
                    or item.get("Text") or item.get("Value") or "")
            if name:
                names.append(str(name).strip())
        elif isinstance(item, str):
            names.append(item.strip())

    return sorted(set(n for n in names if n))


def fetch_live_sensex() -> pd.DataFrame:
    """
    Fetch live SENSEX quote (real-time, no session needed).

    Returns:
        DataFrame — Index, LTP, Change, Change %, Open, High, Low, Prev Close, DateTime
    """
    r    = bse_get(_URL_LIVE_SENSEX)
    data = _parse_json(r)
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data if isinstance(data, list) else [data])
    return _clean_live_sensex(df)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _parse_json(response, context: str = "") -> list:
    """Parse JSON response — handles list, dict with Data key, or empty."""
    try:
        data = response.json()
    except Exception as e:
        raise RuntimeError(
            f"BSE API returned non-JSON response"
            + (f" for {context}" if context else "")
            + f": {response.text[:200]}"
        ) from e

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # Try common wrapper keys
        for key in ("Data", "data", "Table", "Table1", "Result"):
            if key in data and isinstance(data[key], list):
                return data[key]
        # Single object — wrap in list
        return [data]
    return []


def _to_yyyymmdd(date_str: str) -> str:
    """Accept YYYY-MM-DD or YYYYMMDD → return YYYYMMDD."""
    s = date_str.strip().replace("-", "")
    if len(s) == 8 and s.isdigit():
        return s
    raise ValueError(f"Unrecognised date format: '{date_str}'. Use YYYY-MM-DD or YYYYMMDD.")


def _parse_bse_date(val) -> Optional[str]:
    """
    Parse BSE date formats:
      - "20260522"          → "2026-05-22"
      - "22/05/2026"        → "2026-05-22"
      - "22 May 2026"       → "2026-05-22"
      - "/Date(1748...)/"   → "2026-05-22"
    """
    s = str(val).strip()
    if not s or s in ("None", "nan", "NaT"):
        return None

    # .NET /Date(ms)/
    m = re.search(r'/Date\((\d+)\)/', s)
    if m:
        return pd.to_datetime(int(m.group(1)), unit="ms").strftime("%Y-%m-%d")

    # YYYYMMDD
    if re.match(r'^\d{8}$', s):
        return f"{s[:4]}-{s[4:6]}-{s[6:]}"

    # DD/MM/YYYY
    if re.match(r'^\d{2}/\d{2}/\d{4}$', s):
        return datetime.strptime(s, "%d/%m/%Y").strftime("%Y-%m-%d")

    # DD Mon YYYY  or  D-Mon-YYYY  or  D-Month-YYYY
    for fmt in ("%d %b %Y", "%d %B %Y", "%d-%b-%Y", "%-d-%b-%Y",
                "%d-%B-%Y", "%-d-%B-%Y", "%d %B, %Y"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Try pandas as last resort
    try:
        return pd.to_datetime(s, dayfirst=True).strftime("%Y-%m-%d")
    except Exception:
        pass

    return s  # return as-is if unrecognised


def _clean_index_history(df: pd.DataFrame, index_name: str) -> pd.DataFrame:
    """Standardise historical index DataFrame — keep all columns BSE returns."""
    if df.empty:
        return df

    df.columns = [str(c).strip() for c in df.columns]

    # Rename only the columns we know — leave everything else as-is
    rename = {
        "Date": "Date", "date": "Date", "DT": "Date", "Dt": "Date",
        "TradingDate": "Date",
        "Open": "Open", "open": "Open", "OPEN": "Open",
        "High": "High", "high": "High", "HIGH": "High",
        "Low":  "Low",  "low":  "Low",  "LOW":  "Low",
        "Close": "Close", "close": "Close", "CLOSE": "Close",
        "CloseIndex": "Close", "Closing": "Close",
        "Change": "Change", "change": "Change",
        "PerChange": "Change %", "perchange": "Change %", "PChange": "Change %",
        "Change(%)": "Change %",
        "Points Change": "Points Change",
        "Volume(Cr.)": "Volume (Cr.)",
        "Turnover (Rs.Cr.)": "Turnover (Rs. Cr.)",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    # Parse dates
    if "Date" in df.columns:
        df["Date"] = df["Date"].apply(_parse_bse_date)

    # Convert numeric columns
    numeric_cols = ["Open", "High", "Low", "Close", "Change", "Change %",
                    "Points Change", "Volume (Cr.)", "Turnover (Rs. Cr.)",
                    "P/E", "P/B", "Div Yield"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False).str.strip(),
                errors="coerce"
            )

    # Add index name column
    df.insert(0, "Index Name", index_name)

    # Put key columns first, keep all remaining columns after
    preferred = ["Index Name", "Date", "Open", "High", "Low", "Close",
                 "Points Change", "Change %", "Volume (Cr.)", "Turnover (Rs. Cr.)",
                 "P/E", "P/B", "Div Yield"]
    cols  = [c for c in preferred if c in df.columns]
    extra = [c for c in df.columns if c not in cols]
    df    = df[cols + extra]

    return df.dropna(subset=["Date"]).reset_index(drop=True)


def _clean_all_indices(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Standardise all-indices-by-date DataFrame."""
    if df.empty:
        return df

    df.columns = [str(c).strip() for c in df.columns]

    rename = {
        "IndxName": "Index Name", "IndexName": "Index Name",
        "indexName": "Index Name", "index_name": "Index Name",
        "Open": "Open", "High": "High", "Low": "Low",
        "Close": "Close", "Closing": "Close",
        "Change": "Change", "PerChange": "Change %", "PChange": "Change %",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    # Add date
    parsed_date = _parse_bse_date(date) or date
    df["Date"] = parsed_date

    for col in ["Open", "High", "Low", "Close", "Change", "Change %"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False).str.strip(),
                errors="coerce"
            )

    preferred = ["Index Name", "Date", "Open", "High", "Low", "Close", "Change", "Change %"]
    cols  = [c for c in preferred if c in df.columns]
    extra = [c for c in df.columns if c not in cols]
    return df[cols + extra].reset_index(drop=True)


def _clean_live_sensex(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise live SENSEX quote DataFrame."""
    if df.empty:
        return df

    df.columns = [str(c).strip() for c in df.columns]

    rename = {
        "indxnm":    "Index",
        "ltp":       "LTP",
        "chg":       "Change",
        "perchg":    "Change %",
        "I_open":    "Open",
        "High":      "High",
        "Low":       "Low",
        "Prev_Close":"Prev Close",
        "dttm":      "DateTime",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    for col in ["LTP", "Change", "Change %", "Open", "High", "Low", "Prev Close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", "", regex=False).str.strip(),
                errors="coerce"
            )

    preferred = ["Index", "LTP", "Change", "Change %", "Open", "High", "Low", "Prev Close", "DateTime"]
    cols  = [c for c in preferred if c in df.columns]
    extra = [c for c in df.columns if c not in cols]
    return df[cols + extra].reset_index(drop=True)
