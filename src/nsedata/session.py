"""
Session management for NSE websites.
Handles Cloudflare bypass and cookie warming.
"""

import time

import cloudscraper
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


def create_niftyindices_session() -> cloudscraper.CloudScraper:
    """
    Create a session for niftyindices.com with Cloudflare bypass.
    Warms up cookies by visiting the historical data page.
    """
    session = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    session.headers.update({
        **BROWSER_HEADERS,
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://niftyindices.com/reports/historical-data",
        "Origin": "https://niftyindices.com",
    })
    session.get("https://niftyindices.com/reports/historical-data", timeout=30)
    time.sleep(2)
    return session


def create_nse_session() -> requests.Session:
    """
    Create a session for nseindia.com.
    Warms up cookies by visiting the main page and reports page.
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
