"""
Shared HTTP session for bse-data.

BSE India API (api.bseindia.com) requires:
  - A valid Referer header pointing to bseindia.com
  - Session cookies acquired via warmup on bseindia.com
  - Chrome TLS fingerprint (curl_cffi) to pass BSE's bot check

Priority:
  1. curl_cffi  — Chrome TLS impersonation, bypasses BSE bot check
  2. requests   — fallback (may fail on BseIndiaAPI historical endpoints)

The RealTimeBseIndiaAPI (live quotes) works without curl_cffi.
The BseIndiaAPI (historical data) requires curl_cffi for reliable access.
"""

import time
from typing import Optional, Tuple

BSE_BASE     = "https://www.bseindia.com"
BSE_API_BASE = "https://api.bseindia.com"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
    "Referer":         BSE_BASE + "/",
    "Origin":          BSE_BASE,
}

_SESSION      = None
_SESSION_TYPE: Optional[str] = None


def get_session() -> Tuple[object, str]:
    """Return (session, type_str). Builds on first call."""
    global _SESSION, _SESSION_TYPE
    if _SESSION is None:
        _SESSION, _SESSION_TYPE = _build_session()
    return _SESSION, _SESSION_TYPE


def reset_session() -> None:
    """Force a fresh session."""
    global _SESSION, _SESSION_TYPE
    _SESSION      = None
    _SESSION_TYPE = None


def _build_session() -> Tuple[object, str]:
    """
    Build the best available session and warm it up.

    curl_cffi impersonates Chrome's TLS fingerprint — this is what allows
    BSE's bot check to pass and sets the required session cookies.
    """
    # 1. curl_cffi — best (Chrome TLS fingerprint)
    try:
        from curl_cffi.requests import Session as CurlSession
        s = CurlSession(impersonate="chrome124")
        s.headers.update(_HEADERS)
        _warmup(s)
        return s, "curl_cffi"
    except ImportError:
        pass
    except Exception as e:
        print(f"curl_cffi init failed: {e}")

    # 2. Plain requests fallback
    import requests
    s = requests.Session()
    s.headers.update(_HEADERS)
    _warmup(s)
    return s, "requests"


def _warmup(session) -> None:
    """
    Warm up the session by visiting BSE pages to acquire cookies.
    BSE sets ASP.NET_SessionId + sessid on these pages.
    """
    warmup_pages = [
        f"{BSE_BASE}/sensex/code/16/",           # sets ASP.NET_SessionId + sessid
        f"{BSE_BASE}/indices/IndexArchiveData.aspx",  # indices page
    ]
    for url in warmup_pages:
        try:
            session.get(url, timeout=15)
            time.sleep(0.5)
        except Exception:
            pass


def bse_get(url: str, params: dict = None, timeout: int = 20):
    """
    GET a BSE API endpoint with proper session.
    Retries once with a fresh session on failure.
    """
    session, stype = get_session()

    for attempt in range(2):
        try:
            r = session.get(url, params=params, timeout=timeout,
                            allow_redirects=False)

            # 302 to error_Bse.html = session invalid — reset and retry
            if r.status_code in (301, 302) and attempt == 0:
                reset_session()
                time.sleep(2)
                session, stype = get_session()
                continue

            if r.status_code == 200:
                return r

            r.raise_for_status()

        except Exception as e:
            if attempt == 0:
                reset_session()
                time.sleep(2)
                session, stype = get_session()
                continue
            raise RuntimeError(f"BSE API request failed: {url} — {e}") from e

    raise RuntimeError(f"BSE API failed after 2 attempts: {url}")
