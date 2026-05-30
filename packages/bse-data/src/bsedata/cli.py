"""
bse-index-data CLI — command line interface for downloading BSE index data.

Usage:
    bse-index-data index --name SENSEX --from 2026-01-01 --to 2026-05-22
    bse-index-data all-indices --date 2026-05-22
    bse-index-data live
    bse-index-data list
    bse-index-data list --category Sectoral
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="bse-index-data",
        description="Download BSE India index data as CSV",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    sub = parser.add_subparsers(dest="command", help="Command")

    # list
    p_list = sub.add_parser("list", help="List all supported BSE indices")
    p_list.add_argument("--category", default=None,
                        help="Filter by category: Broad Market, Sectoral, Thematic, Strategy, Global")

    # index
    p_idx = sub.add_parser("index", help="Download historical OHLC for one index")
    p_idx.add_argument("--name",  required=True, help="Index key e.g. SENSEX, BSE500, BANKEX")
    p_idx.add_argument("--from",  dest="from_date", required=True, help="From date YYYY-MM-DD")
    p_idx.add_argument("--to",    dest="to_date",   required=True, help="To date YYYY-MM-DD")
    p_idx.add_argument("--out",   default=".",       help="Output directory (default: .)")
    p_idx.add_argument("--s3-bucket", default=None,  help="S3 bucket name")
    p_idx.add_argument("--s3-prefix", default="bse-index-data/", help="S3 prefix")

    # all-indices
    p_all = sub.add_parser("all-indices", help="Download all indices for one date")
    p_all.add_argument("--date", required=True, help="Date YYYY-MM-DD")
    p_all.add_argument("--out",  default=".",   help="Output directory")
    p_all.add_argument("--s3-bucket", default=None,  help="S3 bucket name")
    p_all.add_argument("--s3-prefix", default="bse-index-data/", help="S3 prefix")

    # live
    sub.add_parser("live", help="Get live SENSEX quote")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    from bsedata import bse

    if args.command == "list":
        df = bse.list_indices(category=args.category)
        print(df[["api_key", "name", "category"]].to_string(index=False))

    elif args.command == "index":
        print(f"Downloading BSE {args.name} from {args.from_date} to {args.to_date}...")
        bse.download_index(
            args.name, args.from_date, args.to_date,
            output_dir=args.out,
            s3_bucket=args.s3_bucket,
            s3_prefix=args.s3_prefix,
        )

    elif args.command == "all-indices":
        print(f"Downloading all BSE indices for {args.date}...")
        bse.download_all_indices(
            args.date,
            output_dir=args.out,
            s3_bucket=args.s3_bucket,
            s3_prefix=args.s3_prefix,
        )

    elif args.command == "live":
        df = bse.get_live_sensex()
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
