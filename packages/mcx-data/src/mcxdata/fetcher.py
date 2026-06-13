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
import time
from typing import Optional

import pandas as pd

from mcxdata.session import get_session, reset_session, MCX_BASE

# ── Endpoint URLs (MCX moved these to root-level GET in 2026) ─────────────────
# Old (dead): POST /backpage.aspx/GetSpotMarketPrice  → now returns 404 HTML
# New:        GET  /GetSpotMarketPrice?culture=en
#             GET  /GetSpotMarketArchive?Product=..&Location=..&fromDate=..&toDate=..&Session=..&culture=en
_URL_RECENT  = f"{MCX_BASE}/GetSpotMarketPrice"
_URL_ARCHIVE = f"{MCX_BASE}/GetSpotMarketArchive"

_GET_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{MCX_BASE}/market-data/spot-market-price",
}


def fetch_recent(commodity: str = "ALL", location: str = "ALL",
                 session_val: str = "0") -> pd.DataFrame:
    """
    GET /GetSpotMarketPrice — today's spot prices for all commodities.

    Args:
        commodity:   Not used by MCX for Recent (always returns all). Kept for API symmetry.
        location:    Not used by MCX for Recent.
        session_val: Not used for Recent.

    Returns:
        DataFrame with columns: Commodity, Unit, Location, Spot Price (Rs.), Up/Down, Date
    """
    raw = _get(_URL_RECENT, params={"culture": "en"})
    return _parse_response(raw)


def fetch_archive(from_date: str, to_date: str,
                  commodity: str = "ALL", location: str = "ALL",
                  session_val: str = "0") -> pd.DataFrame:
    """
    GET /GetSpotMarketArchive — historical spot prices.

    Args:
        from_date:   DD/MM/YYYY e.g. "01/05/2026"
        to_date:     DD/MM/YYYY e.g. "22/05/2026"
        commodity:   "ALL" or commodity name e.g. "GOLD", "SILVER"
        location:    "ALL" or location name
        session_val: "0"=Both, "1"=Session1, "2"=Session2

    Returns:
        DataFrame with columns: Commodity, Unit, Location, Date, Spot Price (Rs.), Up/Down
    """
    params = {
        "Product":  commodity if commodity and commodity != "ALL" else "ALL",
        "Location": location  if location  and location  != "ALL" else "ALL",
        "fromDate": from_date,
        "toDate":   to_date,
        "Session":  session_val,
        "culture":  "en",
    }
    raw = _get(_URL_ARCHIVE, params=params)
    return _parse_response(raw)


def _get(url: str, params: dict) -> dict:
    """
    GET an MCX market-data endpoint. Returns parsed JSON dict.

    MCX sits behind Akamai. Two failure modes are handled here:
      * HTTP 403         — hard block
      * HTTP 200 + HTML  — soft block / challenge page (body is not JSON)

    Retry strategy:
      - Attempt 1: same session, wait 3s (cookies preserved)
      - Attempt 2: rebuild session (fresh warmup), wait 5s
      - Attempt 3: give up with an informative error
    """
    session, stype = get_session()
    last_snippet = ""

    for attempt in range(3):
        try:
            if stype == "curl_cffi":
                r = session.get(url, params=params, headers=_GET_HEADERS, timeout=25)
            else:
                session.headers.update(_GET_HEADERS)
                r = session.get(url, params=params, timeout=25)

            # ── Hard block ───────────────────────────────────────────────
            if r.status_code == 403:
                if attempt < 2:
                    _rotate_session(attempt)
                    session, stype = get_session()
                    continue
                raise RuntimeError(
                    f"HTTP 403 from {url} — Akamai WAF is blocking this IP. "
                    f"Ensure curl_cffi is installed; cloud/VPS IPs are often blocked, "
                    f"AWS Lambda IPs usually work."
                )

            if r.status_code == 404:
                raise RuntimeError(
                    f"HTTP 404 from {url} — MCX endpoint not found. "
                    f"The MCX API URL may have changed again; please report this."
                )

            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code} from {url}")

            # ── Parse body defensively (do NOT trust r.json()) ───────────
            text = _response_text(r)
            parsed = _try_json(text)
            if parsed is not None:
                return parsed

            # 200 but not JSON → soft block / challenge page
            last_snippet = (text or "").strip()[:200]
            if attempt < 2:
                _rotate_session(attempt)
                session, stype = get_session()
                continue

            ctype = _response_header(r, "content-type")
            raise RuntimeError(
                f"MCX returned a non-JSON 200 response from {url} "
                f"(content-type: {ctype!r}, {len(text or '')} chars). "
                f"This is usually an Akamai challenge/HTML page. "
                f"First 200 chars: {last_snippet!r}"
            )

        except RuntimeError:
            raise
        except Exception:
            if attempt < 2:
                time.sleep(2)
                continue
            raise

    raise RuntimeError(f"Failed after 3 attempts: {url}")


def _rotate_session(attempt: int) -> None:
    """Wait, then on the second attempt rebuild the session with a fresh warmup."""
    if attempt == 0:
        time.sleep(3)
    else:
        reset_session()
        time.sleep(5)


def _response_text(r) -> str:
    """Return the decoded response body as text, regardless of session backend."""
    try:
        text = r.text
        if text:
            return text
    except Exception:
        pass
    try:
        content = r.content
        if isinstance(content, bytes):
            return content.decode("utf-8", errors="replace")
        return str(content)
    except Exception:
        return ""


def _response_header(r, name: str) -> str:
    try:
        return r.headers.get(name, "") or ""
    except Exception:
        return ""


def _try_json(text: str):
    """Parse JSON from a text body, tolerating a leading BOM/whitespace. None if not JSON."""
    if not text:
        return None
    cleaned = text.lstrip("\ufeff \t\r\n")
    if not cleaned or cleaned[0] not in "{[":
        return None
    try:
        return json.loads(cleaned)
    except (ValueError, json.JSONDecodeError):
        return None


def _parse_response(raw: dict) -> pd.DataFrame:
    """
    Parse MCX market-data response (2026 schema).

    Recent:  {"IsSuccess": true, "Data": {"Summary": {...}, "Data": [ {...}, ... ]}}
    Archive: {"IsSuccess": true, "Data": [ {...}, ... ]}
    Empty:   {"IsSuccess": false, "Message": "No data found.", "Data": null}

    Field names are lowercase: symbol, unit, location, todaysSpotPrice,
    change, _changeSign, date (.NET /Date(ms)/), FormattedDate, FormattedTime.
    """
    if not isinstance(raw, dict):
        raise RuntimeError(f"Unexpected response type: {type(raw)}")

    # Legacy schema fallback ({"d": ...}) — kept for safety.
    if "d" in raw and "Data" not in raw and "IsSuccess" not in raw:
        inner = raw["d"]
        if isinstance(inner, str):
            inner = json.loads(inner) if inner.strip() else []
        data = inner.get("Data", inner.get("data", [])) if isinstance(inner, dict) else inner
        return _clean_df(pd.DataFrame(data or []))

    if raw.get("IsSuccess") is False:
        # No data for the requested range/commodity — return empty frame.
        return pd.DataFrame()

    data_node = raw.get("Data")
    if data_node is None:
        return pd.DataFrame()

    # Recent wraps the rows in Data.Data; archive returns Data as a list directly.
    if isinstance(data_node, dict):
        rows = data_node.get("Data", data_node.get("data", []))
    elif isinstance(data_node, list):
        rows = data_node
    else:
        raise RuntimeError(f"Cannot parse 'Data' of type {type(data_node)}")

    if not rows:
        return pd.DataFrame()

    return _clean_df(pd.DataFrame(rows))


def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise MCX response DataFrame (2026 lowercase field schema)."""
    if df.empty:
        return df

    # Drop internal ASP.NET / duplicate fields
    drop_cols = [c for c in df.columns if c.startswith("__")
                 or c in ("ExtensionData", "enSymbol", "enlocation",
                          "EnSymbol", "Enlocation", "_changeSign",
                          "FormattedDate", "FormattedTime")]
    df = df.drop(columns=drop_cols, errors="ignore")

    # Rename MCX field names → readable column names (handle both old + new casing)
    rename = {
        "symbol":          "Commodity",
        "Symbol":          "Commodity",
        "unit":            "Unit",
        "location":        "Location",
        "todaysSpotPrice": "Spot Price (Rs.)",
        "TodaysSpotPrice": "Spot Price (Rs.)",
        "change":          "Up/Down",
        "Change":          "Up/Down",
        "date":            "Date",
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

    # Parse .NET JSON Date: /Date(milliseconds)/ → datetime → ISO string
    if "Date" in df.columns:
        import re as _re
        def _parse_net_date(val):
            m = _re.search(r'/Date\((\d+)\)/', str(val))
            if m:
                return pd.to_datetime(int(m.group(1)), unit="ms")
            return pd.to_datetime(val, errors="coerce")
        df["Date"] = df["Date"].apply(_parse_net_date)
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Reorder columns sensibly
    preferred_order = ["Commodity", "Unit", "Location", "Spot Price (Rs.)", "Up/Down", "Date"]
    cols = [c for c in preferred_order if c in df.columns]
    extra = [c for c in df.columns if c not in cols]
    df = df[cols + extra]

    return df.reset_index(drop=True)
