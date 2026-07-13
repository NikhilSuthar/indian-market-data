"""
MSCI Data Fetcher — public JSON levels API.

Endpoint (confirmed from browser devtools on https://www.msci.com/indexes):

    GET https://app2.msci.com/products/service/index/indexmaster/getLevelDataForGraph
        ?index_codes=<code>
        &currency_symbol=USD
        &index_variant=NETR          # STRD / NETR / GRTR
        &data_frequency=DAILY
        &start_date=YYYYMMDD
        &end_date=YYYYMMDD

The API returns ONE index per request. For multiple index codes, we loop
and concatenate all results into one flat DataFrame.

Response shape:
    {
        "ISO_currency_symbol": "USD",
        "indexes": {
            "INDEX_LEVELS": [
                {"calc_date": "20260703", "level_eod": 3812.45},
                ...
            ]
        }
    }

Fixed parameters (not configurable — never vary):
    currency  = USD
    frequency = DAILY

Output columns:
    INDEX_CODE, VARIANT, RETURN_TYPE, CURRENCY, DATE, LEVEL
"""

from __future__ import annotations

import datetime as dt
import time
from typing import Union

import pandas as pd
import requests


# ── Constants ─────────────────────────────────────────────────────────────────

API_URL = (
    "https://app2.msci.com/products/service/index/"
    "indexmaster/getLevelDataForGraph"
)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.msci.com/",
}

# API variant codes → human-readable return type label
VARIANT_LABEL: dict[str, str] = {
    "STRD": "Price Return",
    "NETR": "Net Total Return",
    "GRTR": "Gross Total Return",
}

# Friendly aliases (case-insensitive) → API variant code
VARIANT_ALIAS: dict[str, str] = {
    "STRD": "STRD", "PRICE": "STRD", "PR": "STRD",
    "NETR": "NETR", "NET": "NETR", "NTR": "NETR",
    "GRTR": "GRTR", "GROSS": "GRTR", "TR": "GRTR",
    "GTR": "GRTR", "TOTAL RETURN": "GRTR",
}

# The MSCI levels API refuses start_date before this floor
API_DATE_FLOOR = dt.date(2000, 1, 1)

_CURRENCY  = "USD"
_FREQUENCY = "DAILY"

# Output column order
OUTPUT_COLS = ["INDEX_CODE", "VARIANT", "RETURN_TYPE", "CURRENCY", "DATE", "LEVEL"]


# ── Public helpers ────────────────────────────────────────────────────────────

def norm_variant(variant: str) -> str:
    """
    Normalise a variant string to an API variant code.

    Accepts: STRD, NETR, GRTR, price, net, gross, tr, ntr, gtr, etc.
    Returns: "STRD", "NETR", or "GRTR"

    Raises:
        ValueError: if the alias is not recognised
    """
    key = str(variant).strip().upper()
    if key in VARIANT_ALIAS:
        return VARIANT_ALIAS[key]
    raise ValueError(
        f"Unknown variant '{variant}'. "
        f"Valid options: {sorted(set(VARIANT_ALIAS.keys()))}"
    )


# ── Core fetch ────────────────────────────────────────────────────────────────

def fetch_levels(
    index_codes: Union[str, list[str]],
    start_date: dt.date,
    end_date: dt.date,
    variant: str = "NETR",
    sleep: float = 0.4,
    retries: int = 4,
    timeout: int = 60,
) -> pd.DataFrame:
    """
    Fetch end-of-day index levels from MSCI's public API.

    Args:
        index_codes: Single code string or list of MSCI numeric index codes.
                     e.g. "990100" or ["990100", "664185"]
        start_date:  Start date (datetime.date)
        end_date:    End date (datetime.date)
        variant:     Return variant — "STRD"/"NETR"/"GRTR" or friendly alias
                     ("price"/"net"/"gross"). Default "NETR".
        sleep:       Seconds to wait between consecutive index requests.
        retries:     HTTP retry attempts per index.
        timeout:     HTTP request timeout in seconds.

    Returns:
        DataFrame with columns: INDEX_CODE, VARIANT, RETURN_TYPE,
                                 CURRENCY, DATE, LEVEL

    Raises:
        ValueError:   Unknown variant or empty index_codes.
        RuntimeError: All retries exhausted for an index.
    """
    if isinstance(index_codes, str):
        index_codes = [index_codes]
    index_codes = [str(c).strip() for c in index_codes if str(c).strip()]
    if not index_codes:
        raise ValueError("index_codes must not be empty.")

    api_variant = norm_variant(variant)

    # Clamp start_date to API floor
    if start_date < API_DATE_FLOOR:
        start_date = API_DATE_FLOOR

    session = requests.Session()
    all_rows: list[dict] = []

    for code in index_codes:
        rows = _fetch_single(
            code=code,
            variant=api_variant,
            start=start_date,
            end=end_date,
            session=session,
            retries=retries,
            timeout=timeout,
        )
        all_rows.extend(rows)
        if len(index_codes) > 1:
            time.sleep(sleep)

    if not all_rows:
        return pd.DataFrame(columns=OUTPUT_COLS)

    df = pd.DataFrame(all_rows)
    df["LEVEL"] = pd.to_numeric(df["LEVEL"], errors="coerce")
    return df[OUTPUT_COLS].reset_index(drop=True)


# ── Internal ──────────────────────────────────────────────────────────────────

def _fetch_single(
    code: str,
    variant: str,
    start: dt.date,
    end: dt.date,
    session: requests.Session,
    retries: int,
    timeout: int,
) -> list[dict]:
    """
    Fetch levels for ONE index code. Returns list of row dicts.
    Retries on transient errors with exponential back-off.
    """
    params = {
        "currency_symbol": _CURRENCY,
        "index_variant":   variant,
        "start_date":      start.strftime("%Y%m%d"),
        "end_date":        end.strftime("%Y%m%d"),
        "data_frequency":  _FREQUENCY,
        "index_codes":     code,
    }

    last_exc: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            r = session.get(API_URL, params=params, headers=_HEADERS, timeout=timeout)
            r.raise_for_status()

            data = r.json()

            # API-level error
            if "error_message" in data:
                err = str(data["error_message"]).strip()
                if err and err.lower() not in ("", "null", "none"):
                    raise ValueError(f"MSCI API error for {code}: {err}")

            levels = (data.get("indexes") or {}).get("INDEX_LEVELS") or []
            iso_ccy = data.get("ISO_currency_symbol", _CURRENCY)

            rows = []
            for item in levels:
                calc_date = str(item.get("calc_date", ""))
                if len(calc_date) != 8:
                    continue
                rows.append({
                    "INDEX_CODE":  code,
                    "VARIANT":     variant,
                    "RETURN_TYPE": VARIANT_LABEL.get(variant, variant),
                    "CURRENCY":    iso_ccy,
                    "DATE":        f"{calc_date[:4]}-{calc_date[4:6]}-{calc_date[6:8]}",
                    "LEVEL":       item.get("level_eod"),
                })

            return rows

        except (requests.RequestException, ValueError, KeyError) as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(2 * attempt)

    raise RuntimeError(
        f"MSCI fetch failed for index {code!r} / variant {variant!r} "
        f"after {retries} attempts: {last_exc}"
    )
