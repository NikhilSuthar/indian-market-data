"""
Command-line interface for nse-data.

Usage:
    nse-data reports --type bhavcopy --date 2026-04-17
    nse-data reports --type sec_bhavdata --date 2026-04-17
    nse-data reports --type ind_close_all --date 2026-04-17
    nse-data download --type cmvolt --date 2026-04-17 --out ./data
"""

import argparse
import sys

from nsedata import reports
from nsedata.reports import REPORT_PATTERNS


def main():
    parser = argparse.ArgumentParser(
        prog="nse-data",
        description="Download market data from NSE India (nsearchives.nseindia.com)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- reports command (parsed DataFrame output) ---
    rpt_parser = subparsers.add_parser("reports", help="Download and parse daily NSE reports")
    rpt_parser.add_argument(
        "--type", required=True,
        choices=["bhavcopy", "sec_bhavdata", "ind_close_all", "market_activity"],
        help="Report type to download and parse",
    )
    rpt_parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    rpt_parser.add_argument("--out", default=None, help="Output CSV path")

    # --- download command (raw file download) ---
    dl_parser = subparsers.add_parser("download", help="Download raw report file to disk")
    dl_parser.add_argument(
        "--type", required=True,
        choices=sorted(REPORT_PATTERNS.keys()),
        help="Report type to download",
    )
    dl_parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    dl_parser.add_argument("--out", default=".", help="Output directory (default: current)")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "reports":
        _handle_reports(args)
    elif args.command == "download":
        _handle_download(args)


def _handle_reports(args):
    report_funcs = {
        "bhavcopy": reports.get_bhavcopy,
        "sec_bhavdata": reports.get_sec_bhavdata,
        "ind_close_all": reports.get_ind_close_all,
        "market_activity": reports.get_market_activity,
    }

    func = report_funcs[args.type]
    df = func(args.date)

    print(f"Downloaded: {args.type} for {args.date} ({len(df)} rows)")
    print(df.head().to_string(index=False))

    if args.out:
        out_path = args.out
    else:
        out_path = f"{args.type}_{args.date}.csv"

    df.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")


def _handle_download(args):
    path = reports.download_report(args.type, args.date, args.out)
    print(f"Downloaded: {path}")


if __name__ == "__main__":
    main()
