"""
Command-line interface for nse-data.

Usage:
    nse-data indices --index "NIFTY 50" --from "01-Apr-2026" --to "15-May-2026"
    nse-data indices --index "NIFTY 50" --type tri --from "01-Apr-2026" --to "15-May-2026"
    nse-data reports --type bhavcopy --date 2026-04-17
    nse-data reports --type sec_bhavdata --date 2026-04-17
"""

import argparse
import sys

from nsedata import indices, reports


def main():
    parser = argparse.ArgumentParser(
        prog="nse-data",
        description="Download market data from NSE India",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- indices command ---
    idx_parser = subparsers.add_parser("indices", help="Download historical index data")
    idx_parser.add_argument("--index", required=True, help="Index name e.g. 'NIFTY 50'")
    idx_parser.add_argument(
        "--type", default="price", choices=["price", "tri"],
        help="'price' for OHLC, 'tri' for Total Return Index",
    )
    idx_parser.add_argument("--from", dest="start", required=True, help="Start date dd-Mon-yyyy")
    idx_parser.add_argument("--to", dest="end", required=True, help="End date dd-Mon-yyyy")
    idx_parser.add_argument("--out", default=None, help="Output CSV path")

    # --- reports command ---
    rpt_parser = subparsers.add_parser("reports", help="Download daily NSE reports")
    rpt_parser.add_argument(
        "--type", required=True,
        choices=["bhavcopy", "sec_bhavdata", "ind_close_all", "market_activity"],
        help="Report type to download",
    )
    rpt_parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    rpt_parser.add_argument("--out", default=None, help="Output CSV path")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "indices":
        _handle_indices(args)
    elif args.command == "reports":
        _handle_reports(args)


def _handle_indices(args):
    if args.type == "price":
        df = indices.get_historical(args.index, args.start, args.end)
    else:
        df = indices.get_tri(args.index, args.start, args.end)

    print(df.to_string(index=False))

    if args.out:
        out_path = args.out
    else:
        safe_name = args.index.replace(" ", "_")
        suffix = "_TRI" if args.type == "tri" else ""
        out_path = f"{safe_name}{suffix}_{args.start}_to_{args.end}.csv"

    df.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")


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


if __name__ == "__main__":
    main()
