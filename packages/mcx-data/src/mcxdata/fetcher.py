"""
MCX Data Fetcher — calls the two known MCX backpage.aspx endpoints.

Endpoints (confirmed from browser devtools):
  Recent:  POST https://www.mcxindia.com/backpage.aspx/GetSpotMarketPrice
           Body: ""  (empty string)

  Archive: POST https://www.mcxindia.com/backpage.aspx/GetSpotMarketArchive
           Body: {"Product":"GOLD","Location":"ALL","Fromdate":"20260524","Session":"0","Todate":"20260524"}

Response format:
  {"d": "[{\"Symbol\":\"GOLD\",\"Unit\":\"10 GRMS\",\"Location\":\"AHMEDABAD\",
            \"TodaysSpotPrice\":\"157549.00\",\"Change\":\"Down\"}]"}
  i.e. JSON where .d is a JSON-encoded string of the data array.
"""

import json
import io
from typing import Optional

import pandas as pd

from mcxdata.session import get_session, reset_session, MCX_BASE

# ── Endpoint URLs ─────────────────────────────────────────────────────────────
_URL_RECENT  = f"{MCX_BASE}/backpage.aspx/GetSpotMarketPrice"
_URL_ARCHIVE = f"{MCX_BASE}/backpage.aspx/GetSpotMarketArchive"

_POST_HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{MCX_BASE}/market-data/spot-market-price",
    "Origin": MCX_BASE,
}


def fetch_recent(commodity: str = "ALL", location: str = "ALL",
                 session_val: str = "0") -> pd.DataFrame:
    """
    POST GetSpotMarketPrice — returns today's spot prices for all commodities.

    Args:
        commodity:   Not used by MCX for Recent (always returns all). Kept for API symmetry.
        location:    Not used by MCX for Recent.
        session_val: "0"=Both, "1"=Session1, "2"=Session2

    Returns:
        DataFrame with columns: Symbol, Unit, Location, Spot Price (Rs.), Change
    """
    raw = _post(_URL_RECENT, body="")
    return _parse_response(raw)


def fetch_archive(from_date: str, to_date: str,
                  commodity: str = "ALL", location: str = "ALL",
                  session_val: str = "0") -> pd.DataFrame:
    """
    POST GetSpotMarketArchive — returns historical spot prices.

    Args:
        from_date:   YYYYMMDD e.g. "20260501"
        to_date:     YYYYMMDD e.g. "20260522"
        commodity:   "ALL" or commodity name e.g. "GOLD", "SILVER"
        location:    "ALL" or location name
        session_val: "0"=Both, "1"=Session1, "2"=Session2

    Returns:
        DataFrame with columns: Symbol, Unit, Location, Date, Spot Price (Rs.), Change
    """
    payload = {
        "Product":  commodity if commodity and commodity != "ALL" else "ALL",
        "Location": location  if location  and location  != "ALL" else "ALL",
        "Fromdate": from_date,
        "Session":  session_val,
        "Todate":   to_date,
    }
    raw = _post(_URL_ARCHIVE, body=json.dumps(payload))
    return _parse_response(raw)


def _post(url: str, body: str) -> dict:
    """
    POST to MCX backpage endpoint. Returns parsed JSON dict.

    Retry strategy on 403:
      - Attempt 1: retry after 3s with same session (cookies preserved)
      - Attempt 2: rebuild session (fresh warmup) and retry after 5s
    Never destroy cookies on first 403 — Akamai uses session state.
    """
    session, stype = get_session()

    for attempt in range(3):
        try:
            if stype == "curl_cffi":
                r = session.post(url, data=body, headers=_POST_HEADERS, timeout=25)
            else:
                session.headers.update(_POST_HEADERS)
                r = session.post(url, data=body, timeout=25)

            if r.status_code == 403:
                if attempt == 0:
                    # First 403 — same session, just wait longer
                    time.sleep(3)
                    continue
                elif attempt == 1:
                    # Second 403 — rebuild session with fresh warmup
                    reset_session()
                    time.sleep(5)
                    session, stype = get_session()
                    continue
                else:
                    raise RuntimeError(f"HTTP 403: {url} (Akamai WAF blocking — ensure curl_cffi is installed)")

            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {url}")

            return r.json()

        except RuntimeError:
            raise
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            raise

    raise RuntimeError(f"Failed after 3 attempts: {url}")


def _parse_response(raw: dict) -> pd.DataFrame:
    """
    Parse MCX backpage response.

    MCX returns:
      {"d": {"Summary": {"AsOn": ..., "Count": 28}, "Data": [{...}, ...]}}
    or for archive:
      {"d": {"Summary": {...}, "Data": [{...}, ...]}}
    """
    if "d" not in raw:
        raise RuntimeError(f"Unexpected response format: {list(raw.keys())}")

    inner = raw["d"]

    # inner can be a dict with "Data" key, a list, or a JSON string
    if isinstance(inner, str):
        if not inner.strip():
            return pd.DataFrame()
        inner = json.loads(inner)

    if isinstance(inner, dict):
        data = inner.get("Data", inner.get("data", []))
    elif isinstance(inner, list):
        data = inner
    else:
        raise RuntimeError(f"Cannot parse .d of type {type(inner)}: {str(inner)[:100]}")

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    return _clean_df(df)


def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise MCX response DataFrame."""
    if df.empty:
        return df

    # Drop internal ASP.NET type field and junk columns
    drop_cols = [c for c in df.columns if c.startswith("__")
                 or c in ("ExtensionData", "EnSymbol", "Enlocation")]
    df = df.drop(columns=drop_cols, errors="ignore")

    # Rename MCX field names → readable column names
    rename = {
        "Symbol":          "Commodity",
        "TodaysSpotPrice": "Spot Price (Rs.)",
        "Change":          "Up/Down",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})

    # Clean price — remove commas, convert to float
    price_col = "Spot Price (Rs.)"
    if price_col in df.columns:
        df[price_col] = (
            df[price_col].astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[price_col] = pd.to_numeric(df[price_col], errors="coerce")

    # Parse .NET JSON Date: /Date(milliseconds)/ → datetime
    if "Date" in df.columns:
        import re as _re
        def _parse_net_date(val):
            m = _re.search(r'/Date\((\d+)\)/', str(val))
            if m:
                return pd.to_datetime(int(m.group(1)), unit="ms")
            return pd.NaT
        df["Date"] = df["Date"].apply(_parse_net_date)
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")  # ISO: "2026-05-22 12:33:11"

    # Reorder columns sensibly
    preferred_order = ["Commodity", "Unit", "Location", "Spot Price (Rs.)", "Up/Down", "Date"]
    cols = [c for c in preferred_order if c in df.columns]
    extra = [c for c in df.columns if c not in cols]
    df = df[cols + extra]

    return df.reset_index(drop=True)
