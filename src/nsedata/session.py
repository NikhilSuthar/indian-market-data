"""
Session management for NSE websites.
Handles cookie warming for nsearchives.nseindia.com.
"""

import time

import requests

# Common browser headers
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}


def create_nse_session() -> requests.Session:
    """
    Create a session for nseindia.com / nsearchives.nseindia.com.
    Warms up cookies by visiting the main page and reports page.

    This works reliably from any environment including AWS Lambda,
    Snowflake external functions, and other cloud/serverless platforms.
    """
    session = requests.Session()
    session.headers.update({
        **BROWSER_HEADERS,
        "Referer": "https://www.nseindia.com/all-reports",
    })
    session.get("https://www.nseindia.com", timeout=10)
    time.sleep(1)
    session.get("https://www.nseindia.com/all-reports", timeout=10)
    time.sleep(1)
    return session
