"""
NSE Data - Full Dataset Downloader
===================================
Downloads all supported datasets into a folder structure mirroring
.data/NSE Data Download-Sample/:

    output/
    ├── Capital Market/
    │   ├── Equities & SME/
    │   │   ├── Daily/
    │   │   │   ├── sec_bhavdata_full_22052026.csv
    │   │   │   └── ...
    │   │   └── Monthly/
    │   │       └── C_CATG_MAY2026.T01
    │   ├── Indices/
    │   │   └── Daily/
    │   │       └── ind_close_all_22052026.csv
    │   ├── Mutual Fund/
    │   ├── Securities Lending & Borrowing/
    ├── Derivatives/
    │   ├── Equity Derivative/
    │   ├── Commodity Derivative/
    │   ├── Currency Derivative/
    │   └── Interest Rate Derivative/
    ├── Debt/
    │   ├── Corporate Segment/
    │   ├── Debt Segment/
    │   └── Tri-Party Repo/
    └── EGR/

Portal-only datasets (require NSE portal session) are SKIPPED automatically.
They must be downloaded manually from nseindia.com/all-reports.

Usage:
    python download_all.py --date 2026-05-22 --month 2026-05 --out ./nse_data
    python download_all.py --date 2026-05-22 --month 2026-05 --out ./nse_data --tri

Requirements:
    pip install nse-archives openpyxl
    pip install cloudscraper  # only needed for --tri
"""

import argparse
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# ─── Add package source to path if running from repo ─────────────────────────
_script_dir = Path(__file__).parent
_project_root = _script_dir.parent
# Canonical source lives under packages/nse-data/src (the published copy).
_pkg_src = _project_root / "packages" / "nse-data" / "src"
if _pkg_src.exists():
    sys.path.insert(0, str(_pkg_src))
elif (_project_root / "src").exists():
    sys.path.insert(0, str(_project_root / "src"))

from nsedata import nse
from nsedata.registry import get_config

# ─── Folder mapping: (internal_category, internal_subcategory) → output path parts
FOLDER_MAP = {
    ("capital_market", "equities_sme"):  ("Capital Market", "Equities & SME"),
    ("capital_market", "indices"):       ("Capital Market", "Indices"),
    ("capital_market", "mutual_fund"):   ("Capital Market", "Mutual Fund"),
    ("capital_market", "slb"):           ("Capital Market", "Securities Lending & Borrowing"),
    ("derivatives",    "equity"):        ("Derivatives",    "Equity Derivative"),
    ("derivatives",    "commodity"):     ("Derivatives",    "Commodity Derivative"),
    ("derivatives",    "currency"):      ("Derivatives",    "Currency Derivative"),
    ("derivatives",    "interest_rate"): ("Derivatives",    "Interest Rate Derivative"),
    ("debt",           "corporate"):     ("Debt",           "Corporate Segment"),
    ("debt",           "debt_segment"):  ("Debt",           "Debt Segment"),
    ("debt",           "tri_party_repo"):("Debt",           "Tri-Party Repo"),
    ("egr",            "egr"):           ("EGR",            "EGR"),
}

FREQ_FOLDER = {
    "Daily":             "Daily",
    "Monthly":           "Monthly",
    "Weekly/Monthly":    "Weekly",
    "Monthly (static)":  "Monthly",
    "Daily (static)":    "Daily",
    "Daily (6 intraday snapshots)": "Daily",
    "Archive/Daily":     "Daily",
    "Weekly":            "Weekly",
}


class DownloadLogger:
    """Structured download logger."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        self.results = []
        self._fh = open(log_path, "w", encoding="utf-8")
        self._write_header()

    def _write_header(self):
        self._fh.write("=" * 100 + "\n")
        self._fh.write("NSE DATA DOWNLOADER — Full Dataset Run\n")
        self._fh.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self._fh.write("=" * 100 + "\n\n")

    def log(self, cat, sub, dataset, date_used, cmd, status, output, error="", rows=0, cols=0):
        line = (
            f"[{status}] {cat}/{sub}/{dataset}\n"
            f"  Date:   {date_used}\n"
            f"  CMD:    {cmd}\n"
            f"  Output: {output}\n"
        )
        if rows: line += f"  Rows:   {rows} × {cols}\n"
        if error: line += f"  Error:  {error}\n"
        line += "\n"

        print(line.rstrip())
        self._fh.write(line)
        self._fh.flush()

        self.results.append({
            "category": cat, "subcategory": sub, "dataset": dataset,
            "date": date_used, "command": cmd, "status": status,
            "output": output, "error": error, "rows": rows, "cols": cols,
        })

    def log_section(self, title):
        sep = f"\n{'─' * 80}\n{title}\n{'─' * 80}\n"
        print(sep)
        self._fh.write(sep)

    def close(self, output_dir):
        ok   = sum(1 for r in self.results if r["status"] == "OK")
        fail = sum(1 for r in self.results if r["status"] == "FAIL")
        skip = sum(1 for r in self.results if r["status"] == "SKIP")
        total = ok + fail + skip

        # Separate portal-only skips from other skips
        portal_skips = [r for r in self.results
                        if r["status"] == "SKIP" and "Portal-only" in r.get("error", "")]
        other_skips  = [r for r in self.results
                        if r["status"] == "SKIP" and "Portal-only" not in r.get("error", "")]

        summary = (
            f"\n{'=' * 100}\n"
            f"SUMMARY\n"
            f"{'=' * 100}\n"
            f"  Total datasets:  {total}\n"
            f"  ✅ OK:           {ok}\n"
            f"  ❌ FAIL:         {fail}\n"
            f"  ⏭  SKIP:         {skip}\n"
        )

        if portal_skips:
            summary += (
                f"\n  PORTAL-ONLY (skipped — {len(portal_skips)} datasets):\n"
                f"  These require an NSE portal session and cannot be downloaded via direct URL.\n"
                f"  Download manually from: https://www.nseindia.com/all-reports\n"
            )
            for r in portal_skips:
                summary += f"    - {r['category']}/{r['subcategory']}/{r['dataset']}\n"

        if fail:
            summary += f"\n  Failed datasets:\n"
            for r in self.results:
                if r["status"] == "FAIL":
                    summary += f"    - {r['category']}/{r['subcategory']}/{r['dataset']}: {r['error'][:80]}\n"

        summary += f"\n  Output dir: {output_dir}\n"
        summary += f"  Log file:   {self.log_path}\n"
        summary += f"{'=' * 100}\n"

        print(summary)
        self._fh.write(summary)
        self._fh.close()


def get_output_path(base_dir: str, cat: str, sub: str, freq: str) -> Path:
    """Build the output folder path matching NSE Data Download-Sample structure."""
    folder_parts = FOLDER_MAP.get((cat, sub), (cat.replace("_", " ").title(),
                                                sub.replace("_", " ").title()))
    freq_folder = FREQ_FOLDER.get(freq, "Daily")
    path = Path(base_dir) / folder_parts[0] / folder_parts[1] / freq_folder
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_command_string(cat, sub, dataset, date_used, is_download_only, out_path):
    """Build the Python command string for logging."""
    if is_download_only:
        return (f'nse.download("{cat}", "{sub}", "{dataset}", "{date_used}", '
                f'output_dir="{out_path}")')
    else:
        return (f'nse.download("{cat}", "{sub}", "{dataset}", "{date_used}", '
                f'output_dir="{out_path}")')


def download_dataset(cat, sub, dataset, date_str, month_str, out_dir, logger):
    """Download a single dataset and return True on success. Returns None if skipped (portal-only)."""
    cfg = get_config(cat, sub, dataset)

    # Skip portal-only datasets — require NSE portal session, no direct URL
    if getattr(cfg, "portal_only", False) or not cfg.url_pattern:
        logger.log(cat, sub, dataset, "-", "-", "SKIP",
                   "", "Portal-only — must be downloaded manually from nseindia.com/all-reports")
        return None

    freq = cfg.frequency

    # Determine date param
    if cfg.date_type == "monthly":
        date_used = month_str
    elif cfg.date_type == "static":
        date_used = date_str  # passed but ignored in URL
    else:
        date_used = date_str

    # Get output folder
    out_path = get_output_path(out_dir, cat, sub, freq)

    # Build kwargs for special datasets
    kwargs = {}

    # VaR snapshots — download all 6
    if dataset == "cvar1":
        all_ok = True
        for snap in range(1, 7):
            cmd = (f'nse.download("{cat}", "{sub}", "cvar1", "{date_used}", '
                   f'snapshot={snap}, output_dir="{out_path}")')
            try:
                result = nse.download(cat, sub, dataset, date_used,
                                      output_dir=str(out_path), snapshot=snap)
                fname = Path(result).name
                logger.log(cat, sub, f"cvar1 (snapshot {snap})", date_used, cmd,
                           "OK", result)
                time.sleep(0.3)
            except Exception as e:
                logger.log(cat, sub, f"cvar1 (snapshot {snap})", date_used, cmd,
                           "FAIL", "", str(e)[:120])
                all_ok = False
        return all_ok

    is_download_only = cfg.download_only or not cfg.df_supported

    cmd = build_command_string(cat, sub, dataset, date_used, is_download_only, out_path)

    try:
        # Always use download() to save actual file to disk
        result = nse.download(cat, sub, dataset, date_used,
                              output_dir=str(out_path), **kwargs)
        fname = Path(result).name
        fsize = Path(result).stat().st_size if Path(result).exists() else 0

        # Also parse as DataFrame if supported (to verify and log row count)
        rows, cols = 0, 0
        if not is_download_only:
            try:
                df = nse.get(cat, sub, dataset, date_used, **kwargs)
                rows, cols = len(df), len(df.columns)
            except Exception:
                pass  # download succeeded, df parse failed — still OK

        logger.log(cat, sub, dataset, date_used, cmd, "OK", result, rows=rows, cols=cols)
        return True

    except Exception as e:
        err = str(e)
        logger.log(cat, sub, dataset, date_used, cmd, "FAIL", "", err[:120])
        return False


def download_all(date: str, month: str, out_dir: str, include_tri: bool = False,
                 delay: float = 0.5):
    """Main download function."""
    all_datasets = nse.list_datasets()
    log_path = str(Path(out_dir) / "download_log.txt")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    logger = DownloadLogger(log_path)

    print(f"\nNSE Data Downloader")
    print(f"Daily date:   {date}")
    print(f"Monthly date: {month}")
    print(f"Output dir:   {out_dir}")
    print(f"Datasets:     {len(all_datasets)}")
    print(f"Log:          {log_path}\n")

    # ─── Group by category for organized output ───────────────────────
    from itertools import groupby
    cats = sorted(all_datasets["category"].unique())

    # Track downloaded (date, sub) combinations to avoid re-warming session
    for cat in cats:
        cat_ds = all_datasets[all_datasets["category"] == cat]
        subs = sorted(cat_ds["subcategory"].unique())

        for sub in subs:
            sub_ds = cat_ds[cat_ds["subcategory"] == sub]
            logger.log_section(f"{cat.upper()} / {sub.upper()} ({len(sub_ds)} datasets)")

            for _, row in sub_ds.iterrows():
                dataset = row["dataset"]
                success = download_dataset(cat, sub, dataset, date, month, out_dir, logger)
                time.sleep(delay)

    # ─── Historical Index + TRI (niftyindices.com) ────────────────────
    if include_tri:
        logger.log_section("NIFTY INDICES — Historical Price Index & TRI (niftyindices.com)")
        print("\n⚠️  Testing niftyindices.com (Cloudflare-protected — may fail from cloud IPs)\n")

        indices_to_test = [
            "NIFTY 50",
            "NIFTY BANK",
            "NIFTY IT",
            "NIFTY MIDCAP 50",
        ]
        # Use the date's month range for TRI
        dt = datetime.strptime(date, "%Y-%m-%d")
        start_dd_mon = f"01-{dt.strftime('%b-%Y')}"
        end_dd_mon   = dt.strftime("%d-%b-%Y")

        out_path = Path(out_dir) / "Capital Market" / "Indices" / "Historical (niftyindices.com)"
        out_path.mkdir(parents=True, exist_ok=True)

        for idx_name in indices_to_test:
            shorthand = idx_name.lower().replace(" ", "")

            # Price Index
            cmd = f'nse.get_historical_index("{idx_name}", "{start_dd_mon}", "{end_dd_mon}")'
            try:
                df = nse.get_historical_index(idx_name, start_dd_mon, end_dd_mon)
                fname = f"{shorthand}_price_{dt.strftime('%b%Y')}.csv"
                out_file = out_path / fname
                df.to_csv(out_file, index=False)
                logger.log("niftyindices", idx_name, "price", f"{start_dd_mon} to {end_dd_mon}",
                           cmd, "OK", str(out_file), rows=len(df), cols=len(df.columns))
            except Exception as e:
                logger.log("niftyindices", idx_name, "price", f"{start_dd_mon} to {end_dd_mon}",
                           cmd, "FAIL", "", str(e)[:120])
            time.sleep(2)

            # TRI
            cmd = f'nse.get_tri("{idx_name}", "{start_dd_mon}", "{end_dd_mon}")'
            try:
                df = nse.get_tri(idx_name, start_dd_mon, end_dd_mon)
                fname = f"{shorthand}_tri_{dt.strftime('%b%Y')}.csv"
                out_file = out_path / fname
                df.to_csv(out_file, index=False)
                logger.log("niftyindices", idx_name, "tri", f"{start_dd_mon} to {end_dd_mon}",
                           cmd, "OK", str(out_file), rows=len(df), cols=len(df.columns))
            except Exception as e:
                logger.log("niftyindices", idx_name, "tri", f"{start_dd_mon} to {end_dd_mon}",
                           cmd, "FAIL", "", str(e)[:120])
            time.sleep(2)

        # Derived TRI (always works — no Cloudflare)
        logger.log_section("DERIVED TRI (from ind_close_all — works everywhere)")
        try:
            ind_df = nse.get("capital_market", "indices", "ind_close_all", date)
            nifty = ind_df[ind_df["Index Name"] == "Nifty 50"].rename(
                columns={"Index Date": "Date", "Closing Index Value": "Close"})
            nifty["Date"] = __import__("pandas").to_datetime(nifty["Date"])
            tri_df = nse.derive_tri(nifty)
            fname = f"NIFTY50_derived_tri_{date}.csv"
            out_file = out_path / fname
            tri_df.to_csv(out_file, index=False)
            cmd = f"nse.derive_tri(ind_close_all_df[index=='Nifty 50'])"
            logger.log("derived", "Nifty 50", "derive_tri", date, cmd, "OK",
                       str(out_file), rows=len(tri_df), cols=len(tri_df.columns))
        except Exception as e:
            logger.log("derived", "Nifty 50", "derive_tri", date,
                       "nse.derive_tri(...)", "FAIL", "", str(e)[:120])

    logger.close(out_dir)
    return logger.results


# ─── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download all NSE datasets to a local folder structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_all.py --date 2026-05-22 --month 2026-05 --out ./nse_data
  python download_all.py --date 2026-05-22 --month 2026-05 --out ./nse_data --tri
  python download_all.py --date 2026-05-22 --month 2026-05 --out ./nse_data --delay 1.0
        """,
    )
    parser.add_argument("--date",  required=True, help="Daily date YYYY-MM-DD (e.g. 2026-05-22)")
    parser.add_argument("--month", required=True, help="Monthly date YYYY-MM (e.g. 2026-05)")
    parser.add_argument("--out",   default="./nse_data", help="Output directory (default: ./nse_data)")
    parser.add_argument("--tri",   action="store_true", help="Also download from niftyindices.com (TRI + historical prices)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between downloads in seconds (default: 0.5)")

    args = parser.parse_args()

    # Validate dates
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: --date must be YYYY-MM-DD, got: {args.date}")
        sys.exit(1)
    try:
        datetime.strptime(args.month + "-01", "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: --month must be YYYY-MM, got: {args.month}")
        sys.exit(1)

    results = download_all(
        date=args.date,
        month=args.month,
        out_dir=args.out,
        include_tri=args.tri,
        delay=args.delay,
    )
