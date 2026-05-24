"""
niftyindices.com data fetcher — Historical Index Data and Total Return Index.

Data source: https://niftyindices.com/reports/historical-data

NOTE ON CLOUD/LAMBDA:
    niftyindices.com is protected by Cloudflare. This works reliably from
    residential IPs (desktop, laptop). AWS Lambda / GCP / Azure IP ranges
    may be blocked by Cloudflare. If it fails from Lambda, use the
    S3-handoff pattern: run this locally → upload to S3 → Lambda reads from S3.

Functions:
    get_historical(index_name, start_date, end_date) → DataFrame   # Price OHLC
    get_tri(index_name, start_date, end_date) → DataFrame          # Total Return Index
    derive_tri(price_df, div_df) → DataFrame                       # Derive TRI from price + dividends
    list_indices() → list                                          # All available index names
"""

import json
import time
import warnings
from datetime import datetime

import pandas as pd

try:
    import cloudscraper
    _HAS_CLOUDSCRAPER = True
except ImportError:
    _HAS_CLOUDSCRAPER = False

BASE_URL = "https://niftyindices.com"
API_PRICE = f"{BASE_URL}/Backpage.aspx/getHistoricaldatatabletoString"
API_TRI   = f"{BASE_URL}/Backpage.aspx/getTotalReturnIndexString"

# Browser headers for Cloudflare bypass
_HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://niftyindices.com/reports/historical-data",
    "Origin": "https://niftyindices.com",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

# ─── Known NSE Index names ────────────────────────────────────────────────
# Full list available at https://niftyindices.com/reports/historical-data
INDEX_NAMES = {
    # Broad Market
    "nifty50": "NIFTY 50",
    "nifty100": "NIFTY 100",
    "nifty200": "NIFTY 200",
    "nifty500": "NIFTY 500",
    "niftymidcap50": "NIFTY MIDCAP 50",
    "niftymidcap100": "NIFTY MIDCAP 100",
    "niftymidcap150": "NIFTY MIDCAP 150",
    "niftysmallcap50": "NIFTY SMALLCAP 50",
    "niftysmallcap100": "NIFTY SMALLCAP 100",
    "niftysmallcap250": "NIFTY SMALLCAP 250",
    "niftynext50": "NIFTY NEXT 50",
    # Sectoral
    "niftybank": "NIFTY BANK",
    "niftyit": "NIFTY IT",
    "niftyauto": "NIFTY AUTO",
    "niftypharma": "NIFTY PHARMA",
    "niftyfmcg": "NIFTY FMCG",
    "niftymetal": "NIFTY METAL",
    "niftyenergy": "NIFTY ENERGY",
    "niftyrealty": "NIFTY REALTY",
    "niftymedia": "NIFTY MEDIA",
    "niftypse": "NIFTY PSE",
    "niftypsubank": "NIFTY PSU BANK",
    "niftypvtbank": "NIFTY PVT BANK",
    "niftyfinservice": "NIFTY FIN SERVICE",
    "niftyoilgas": "NIFTY OIL & GAS",
    "niftyinfra": "NIFTY INFRA",
    "niftymnc": "NIFTY MNC",
    "niftyconsumption": "NIFTY CONSUMPTION",
    "niftyservices": "NIFTY SERVICES",
    # Thematic
    "niftycommodities": "NIFTY COMMODITIES",
    "nifty100quality30": "NIFTY100 QUALITY 30",
    "niftydividendopps50": "NIFTY DIVIDEND OPPORTUNITIES 50",
    "niftymidliquid15": "NIFTY MIDCAP LIQ 15",
    # Fixed Income
    "nifty8_13yrgsec": "Nifty 8-13 yr G-Sec",
    "nifty10yrbenchgsec": "Nifty 10 yr Benchmark G-Sec",
    "nifty4_8yrgsec": "Nifty 4-8 yr G-Sec Index",
}


def _create_session():
    """Create a cloudscraper session for niftyindices.com."""
    if not _HAS_CLOUDSCRAPER:
        raise ImportError(
            "cloudscraper is required for niftyindices.com data.\n"
            "Install with: pip install cloudscraper"
        )
    session = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    session.headers.update(_HEADERS)
    # Warmup request to get Cloudflare cookies
    session.get("https://niftyindices.com/reports/historical-data", timeout=30)
    time.sleep(2)
    return session


def _fetch(index_name: str, start_date: str, end_date: str, api_url: str) -> pd.DataFrame:
    """
    Internal: POST to niftyindices.com API and return parsed DataFrame.

    Args:
        index_name: Exact index name as on niftyindices.com
        start_date: "dd-Mon-yyyy" e.g. "01-Apr-2026"
        end_date:   "dd-Mon-yyyy" e.g. "30-Apr-2026"
        api_url:    API_PRICE or API_TRI
    """
    session = _create_session()

    payload = {
        "cinfo": json.dumps({
            "name":      index_name,
            "startDate": start_date,
            "endDate":   end_date,
            "indexName": index_name,
        })
    }

    resp = session.post(api_url, json=payload, timeout=60)

    if resp.status_code != 200:
        raise RuntimeError(
            f"HTTP {resp.status_code} from niftyindices.com: {resp.text[:200]}\n"
            f"This may be a Cloudflare block (common from AWS Lambda / datacenter IPs).\n"
            f"Try running from a residential IP or use the S3-handoff pattern."
        )

    data = resp.json()
    if "d" not in data:
        raise RuntimeError(f"Unexpected response format: {str(data)[:200]}")

    records = json.loads(data["d"])
    if not records:
        raise RuntimeError(
            f"No data returned for '{index_name}' between {start_date} and {end_date}.\n"
            f"Verify the index name exactly matches niftyindices.com spelling."
        )

    df = pd.DataFrame(records)
    df.columns = [c.strip() for c in df.columns]

    # Normalize column names
    col_map = {
        "indexName": "Index Name", "INDEX_NAME": "Index Name", "IndexName": "Index Name",
        "HistoricalDate": "Date",
        "OPEN": "Open", "HIGH": "High", "LOW": "Low", "CLOSE": "Close",
        "TotalReturnsIndex": "Total Returns Index",
        "NTR_Value": "Net Total Return Index",
    }
    df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

    # Drop junk columns
    for col in ["RequestNumber", "requestNumber"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Parse dates
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"].replace("", pd.NaT), format="%d %b %Y", errors="coerce")
        df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    # Parse numeric columns
    for col in ["Open", "High", "Low", "Close", "Total Returns Index", "Net Total Return Index"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")

    # Keep only relevant columns
    keep = [c for c in ["Index Name", "Date", "Open", "High", "Low", "Close",
                         "Total Returns Index", "Net Total Return Index"] if c in df.columns]
    return df[keep]


def get_historical(index_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical Price Index (OHLC) for a given index.

    Args:
        index_name: Index name exactly as on niftyindices.com
                    e.g. "NIFTY 50", "NIFTY BANK", "Nifty Auto"
                    Or use shorthand: "nifty50", "niftybank" (auto-expanded)
        start_date: "dd-Mon-yyyy" e.g. "01-Apr-2026"
        end_date:   "dd-Mon-yyyy" e.g. "30-Apr-2026"

    Returns:
        DataFrame: Index Name, Date, Open, High, Low, Close

    Note:
        Works from residential IPs. May be blocked from AWS Lambda by Cloudflare.

    Example:
        >>> from nsedata import nse
        >>> df = nse.get_historical_index("NIFTY 50", "01-Apr-2026", "30-Apr-2026")
        >>> df = nse.get_historical_index("nifty50", "01-Apr-2026", "30-Apr-2026")  # shorthand
    """
    resolved = INDEX_NAMES.get(index_name.lower().replace(" ", ""), index_name)
    return _fetch(resolved, start_date, end_date, API_PRICE)


def get_tri(index_name: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch Total Return Index (TRI) for a given index.

    TRI = Price Index + reinvested dividends. Essential for AMC performance
    benchmarking as it reflects actual investor returns including dividends.

    Args:
        index_name: Index name (same as get_historical)
        start_date: "dd-Mon-yyyy"
        end_date:   "dd-Mon-yyyy"

    Returns:
        DataFrame: Index Name, Date, Total Returns Index, Net Total Return Index

    Columns:
        Total Returns Index    — Gross TRI (pre-tax dividend reinvestment)
        Net Total Return Index — NTR (post-tax dividend reinvestment, ~15% tax on dividends)

    Note:
        Works from residential IPs. May be blocked from AWS Lambda by Cloudflare.

    Example:
        >>> from nsedata import nse
        >>> df = nse.get_tri("NIFTY 50", "01-Apr-2026", "30-Apr-2026")
    """
    resolved = INDEX_NAMES.get(index_name.lower().replace(" ", ""), index_name)
    return _fetch(resolved, start_date, end_date, API_TRI)


def list_indices() -> list:
    """Return list of (shorthand, full_name) for all known indices."""
    return [(k, v) for k, v in INDEX_NAMES.items()]


# ─── TRI Derivation ──────────────────────────────────────────────────────────

def derive_tri(
    price_df: pd.DataFrame,
    dividends: pd.DataFrame = None,
    base_date: str = None,
    base_value: float = 1000.0,
) -> pd.DataFrame:
    """
    Derive an approximate Total Return Index from price index + dividend data.

    FORMULA:
        TRI(t) = TRI(t-1) × [1 + (Price(t) - Price(t-1) + Div(t)) / Price(t-1)]

    Which simplifies to:
        TRI(t) = TRI(t-1) × [Price(t) / Price(t-1)] + TRI(t-1) × [Div(t) / Price(t-1)]

    Or equivalently (reinvestment assumption):
        TRI(t) = TRI(t-1) × (Price(t) + Div(t)) / Price(t-1)

    IMPORTANT CAVEAT:
        This is an APPROXIMATION. The official NSE TRI uses:
        1. Constituent-level dividends on ex-date weighted by index weight
        2. Exact dividend amounts from corporate action records
        3. Historical index weights that change at rebalancing
        The approximation here uses a simplified dividend yield assumption.

    Args:
        price_df:   DataFrame from get_historical() with Date and Close columns
        dividends:  Optional DataFrame with Date and Dividend columns (per-unit dividend).
                    If None, uses rolling dividend yield from P/E, P/B data to estimate.
        base_date:  Starting date for TRI series (default: first date in price_df)
        base_value: Starting TRI value (default: 1000)

    Returns:
        DataFrame: Date, Close (price index), Derived_TRI, Daily_Return, Dividend_Return

    Example:
        >>> from nsedata import nse
        >>> price_df = nse.get_historical_index("NIFTY 50", "01-Jan-2025", "31-Dec-2025")
        >>> tri_df = nse.derive_tri(price_df)
        >>> print(tri_df[["Date", "Close", "Derived_TRI"]].tail())
    """
    df = price_df.copy()
    df = df.sort_values("Date").reset_index(drop=True)

    if "Close" not in df.columns:
        raise ValueError("price_df must have a 'Close' column")

    # Handle base date
    if base_date:
        bd = pd.to_datetime(base_date)
        df = df[df["Date"] >= bd].reset_index(drop=True)

    if len(df) == 0:
        raise ValueError("No data after base_date filter")

    # Calculate daily price return
    df["Price_Return"] = df["Close"].pct_change().fillna(0)

    # Dividend return per day
    if dividends is not None:
        # Merge provided dividend data
        div = dividends.copy()
        div["Date"] = pd.to_datetime(div["Date"])
        div = div.rename(columns={"Dividend": "Div_Amount"})
        df = df.merge(div[["Date", "Div_Amount"]], on="Date", how="left")
        df["Div_Amount"] = df["Div_Amount"].fillna(0)
        # Dividend return = dividend per unit / previous close price
        df["Div_Return"] = df["Div_Amount"] / df["Close"].shift(1).fillna(df["Close"].iloc[0])
    else:
        # Estimate using simplified annual dividend yield (~1.5% for Nifty 50 historically)
        # Distributed proportionally across trading days (~252/year)
        # This is a rough approximation — use actual dividends for accurate TRI
        warnings.warn(
            "No dividend data provided. Using estimated 1.5% annual yield distributed daily.\n"
            "This is approximate. For accurate TRI, provide actual dividend records.",
            UserWarning
        )
        annual_yield = 0.015  # ~1.5% — Nifty 50 historical average
        daily_div_return = annual_yield / 252
        df["Div_Return"] = daily_div_return
        df.loc[0, "Div_Return"] = 0  # No dividend on base day

    # Total daily return = price return + dividend return
    df["Total_Return"] = df["Price_Return"] + df["Div_Return"]

    # Compound TRI
    df["Derived_TRI"] = base_value * (1 + df["Total_Return"]).cumprod()
    df.loc[0, "Derived_TRI"] = base_value

    # Keep relevant columns
    cols = ["Date", "Close", "Price_Return", "Div_Return", "Total_Return", "Derived_TRI"]
    if "Index Name" in df.columns:
        cols = ["Index Name"] + cols

    return df[[c for c in cols if c in df.columns]].round(4)
