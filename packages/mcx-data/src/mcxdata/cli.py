"""
mcx-data CLI — command line interface for downloading MCX data.

Usage:
    mcx-data spot recent
    mcx-data spot archive --from 01/05/2026 --to 22/05/2026 --commodity GOLD
    mcx-data list
    mcx-data commodities
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="mcx-data",
        description="Download MCX India commodity market data as CSV",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s 0.1.0")

    sub = parser.add_subparsers(dest="command", help="Command")

    # list command
    sub.add_parser("list", help="List all available MCX datasets")

    # commodities command
    sub.add_parser("commodities", help="List available commodity names from MCX")

    # spot recent
    spot_recent = sub.add_parser("spot-recent", help="Download today's spot market prices")
    spot_recent.add_argument("--commodity", default="ALL", help="Commodity name or ALL")
    spot_recent.add_argument("--location",  default="ALL", help="Location name or ALL")
    spot_recent.add_argument("--out",       default=".",   help="Output directory")
    spot_recent.add_argument("--s3-bucket", default=None,  help="S3 bucket name")
    spot_recent.add_argument("--s3-prefix", default="mcx-data/", help="S3 prefix")

    # spot archive
    spot_archive = sub.add_parser("spot-archive", help="Download historical spot market prices")
    spot_archive.add_argument("--from", dest="from_date", required=True,
                              help="From date DD/MM/YYYY")
    spot_archive.add_argument("--to",   dest="to_date",   required=True,
                              help="To date DD/MM/YYYY")
    spot_archive.add_argument("--commodity", default="ALL", help="Commodity name or ALL")
    spot_archive.add_argument("--out",       default=".",   help="Output directory")
    spot_archive.add_argument("--s3-bucket", default=None,  help="S3 bucket name")
    spot_archive.add_argument("--s3-prefix", default="mcx-data/", help="S3 prefix")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    from mcxdata import mcx

    if args.command == "list":
        df = mcx.list_datasets()
        print(df.to_string(index=False))

    elif args.command == "commodities":
        print("Fetching commodity list from MCX...")
        commodities = mcx.list_commodities()
        for c in commodities:
            print(f"  {c}")

    elif args.command == "spot-recent":
        print(f"Downloading MCX spot recent (commodity={args.commodity})...")
        mcx.download("spot", "market", "spot_recent",
                     commodity=args.commodity,
                     location=args.location,
                     output_dir=args.out,
                     s3_bucket=args.s3_bucket,
                     s3_prefix=args.s3_prefix)

    elif args.command == "spot-archive":
        print(f"Downloading MCX spot archive {args.from_date} → {args.to_date} (commodity={args.commodity})...")
        mcx.download("spot", "market", "spot_archive",
                     from_date=args.from_date,
                     to_date=args.to_date,
                     commodity=args.commodity,
                     output_dir=args.out,
                     s3_bucket=args.s3_bucket,
                     s3_prefix=args.s3_prefix)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
