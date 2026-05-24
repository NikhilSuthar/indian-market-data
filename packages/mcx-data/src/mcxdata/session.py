"""
Shared HTTP session for mcx-data.

MCX India uses Akamai WAF which blocks plain Python requests.
Solution: curl_cffi with Chrome TLS fingerprint impersonation (same approach that
works for niftyindices.com TRI in nse-data).

Priority:
  1. curl_cffi  — Chrome TLS impersonation, bypasses Akamai
  2. cloudscraper — partial Akamai bypass
  3. requests    — fallback (may 403 on Akamai-blocked IPs)
"""

import time
from typing import Optional, Tuple

MCX_BASE = "https://www.mcxindia.com"
MCX_SPOT_PAGE = f"{MCX_BASE}/market-data/spot-market-price"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
}

# Module-level session cache
_SESSION = None
_SESSION_TYPE: Optional[str] = None


def get_session() -> Tuple[object, str]:
    """Return (session, type_str). Builds session on first call."""
    global _SESSION, _SESSION_TYPE
    if _SESSION is None:
        _SESSION, _SESSION_TYPE = _build_session()
    return _SESSION, _SESSION_TYPE


def reset_session() -> None:
    """Force a fresh session (e.g. after 403)."""
    global _SESSION, _SESSION_TYPE
    _SESSION = None
    _SESSION_TYPE = None


def _build_session() -> Tuple[object, str]:
    """Build the best available session and warm it up with the MCX page."""

    # 1. curl_cffi — best for Akamai (exact Chrome TLS fingerprint)
    try:
        from curl_cffi.requests import Session as CurlSession
        s = CurlSession(impersonate="chrome124")
        s.headers.update(_HEADERS)
        _warmup(s, "curl_cffi")
        return s, "curl_cffi"
    except ImportError as e:
        print(f"curl_cffi not available: {e}")
    except Exception as e:
        print(f"curl_cffi failed to init: {e}")

    # 2. cloudscraper — JS challenge solver
    try:
        import cloudscraper
        s = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        s.headers.update(_HEADERS)
        _warmup(s, "cloudscraper")
        return s, "cloudscraper"
    except ImportError:
        pass
    except Exception as e:
        print(f"cloudscraper failed: {e}")

    # 3. Plain requests fallback
    print("WARNING: falling back to plain requests — MCX may return 403 (Akamai WAF)")
    import requests
    s = requests.Session()
    s.headers.update(_HEADERS)
    _warmup(s, "requests")
    return s, "requests"


def _warmup(session, stype: str) -> None:
    """
    GET the MCX spot page to acquire session cookies.
    Also call the recent endpoint once to fully warm up the session state.
    """
    try:
        session.get(MCX_SPOT_PAGE, timeout=15)
        time.sleep(1.5)  # Akamai needs time to recognise the session
    except Exception:
        pass
