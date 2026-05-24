"""
Local test script for mcx-data package.

Tests MCX spot market data — Recent and Archive.

Usage:
    python test_mcx_local.py
    python test_mcx_local.py --commodity GOLD
    python test_mcx_local.py --from 01/05/2026 --to 22/05/2026
    python test_mcx_local.py --from 01/05/2026 --to 22/05/2026 --commodity GOLD

Requirements (install once):
    pip install html5lib lxml requests pandas openpyxl

Optionally (helps bypass Akamai WAF):
    pip install cloudscraper
"""

import argparse
import sys
import time
from pathlib import Path

# ── Load mcx-data from local source ─────────────────────────────────────────
_root = Path(__file__).parent.parent
_mcx_src = _root / "packages" / "mcx-data" / "src"
if _mcx_src.exists():
    sys.path.insert(0, str(_mcx_src))
    print(f"✓ Using local mcx-data from: {_mcx_src}")
else:
    print("Using installed mcx-data (local source not found)")

from mcxdata import mcx


def run_tests(commodity: str = "ALL", from_date: str = None, to_date: str = None):
    """Run all MCX local tests."""

    print("\n" + "=" * 60)
    print("MCX DATA LOCAL TEST")
    print("=" * 60)

    # ── 1. list_datasets ──────────────────────────────────────────
    print("\n[1] list_datasets()")
    df_list = mcx.list_datasets()
    print(df_list[["category", "subcategory", "dataset", "date_type", "df_supported"]].to_string(index=False))

    # ── 2. list_commodities ───────────────────────────────────────
    print("\n[2] list_commodities()  — fetches live from MCX")
    try:
        comms = mcx.list_commodities()
        print(f"  ✓ {len(comms)} commodities: {comms[:8]}{'...' if len(comms) > 8 else ''}")
    except Exception as e:
        print(f"  ✗ {e}")

    time.sleep(2)

    # ── 3. spot_recent ────────────────────────────────────────────
    print(f"\n[3] get_spot_recent(commodity='{commodity}')")
    try:
        df_recent = mcx.get_spot_recent(commodity=commodity)
        print(f"  ✓ {len(df_recent)} rows × {len(df_recent.columns)} cols")
        print(f"  Columns: {list(df_recent.columns)}")
        print(df_recent.head(5).to_string(index=False))
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")

    time.sleep(2)

    # ── 4. spot_archive ───────────────────────────────────────────
    _from = from_date or "01/05/2026"
    _to   = to_date   or "22/05/2026"
    # Archive requires a specific commodity — MCX returns 0 rows for "ALL"
    _comm_arch = commodity if commodity != "ALL" else "GOLD"
    print(f"\n[4] get_spot_archive('{_from}', '{_to}', commodity='{_comm_arch}')")
    try:
        df_arch = mcx.get_spot_archive(_from, _to, commodity=_comm_arch)
        print(f"  ✓ {len(df_arch)} rows × {len(df_arch.columns)} cols")
        print(f"  Columns: {list(df_arch.columns)}")
        print(df_arch.head(5).to_string(index=False))
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")

    time.sleep(2)

    # ── 5. generic get() ──────────────────────────────────────────
    print(f"\n[5] Generic get('spot', 'market', 'spot_archive', from_date=..., to_date=...)")
    try:
        df_gen = mcx.get("spot", "market", "spot_archive",
                         from_date=_from, to_date=_to, commodity=_comm_arch)
        print(f"  ✓ {len(df_gen)} rows")
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")

    time.sleep(2)

    # ── 6. download to local file ──────────────────────────────────
    print(f"\n[6] download() → ./mcx_test_output/")
    try:
        path = mcx.download("spot", "market", "spot_recent",
                            commodity=commodity,
                            output_dir="./mcx_test_output")
        print(f"  ✓ Saved: {path}")
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test mcx-data locally")
    parser.add_argument("--commodity", default="ALL",
                        help="Commodity filter: ALL, GOLD, SILVER, CRUDEOIL etc.")
    parser.add_argument("--from", dest="from_date", default=None,
                        help="Archive from date DD/MM/YYYY (default: 01/05/2026)")
    parser.add_argument("--to", dest="to_date", default=None,
                        help="Archive to date DD/MM/YYYY (default: 22/05/2026)")
    args = parser.parse_args()

    run_tests(commodity=args.commodity, from_date=args.from_date, to_date=args.to_date)
