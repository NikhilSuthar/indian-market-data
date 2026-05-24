"""
india-market-data — Umbrella package for NSE and MCX India market data.

Installs and re-exports both nse-data and mcx-data.

Usage:
    from indiamarketdata import nse, mcx

    # NSE data
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")

    # MCX data (coming soon)
    df = mcx.get("commodity", "bhavcopy", "2026-05-22")

Or use packages individually:
    from nsedata import nse      # pip install nse-data
    from mcxdata import mcx      # pip install mcx-data
"""

__version__ = "0.9.0"

# Re-export both sub-packages
try:
    from nsedata import nse
except ImportError:
    nse = None  # type: ignore

try:
    from mcxdata import mcx
except ImportError:
    mcx = None  # type: ignore

__all__ = ["nse", "mcx"]
