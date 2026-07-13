"""
msci-data CLI — command-line interface for MSCI index levels.

Usage:
    msci-data levels --codes 990100 --from 2026-01-01 --to 2026-07-01
    msci-data levels --codes 990100 664185 --from 2026-01-01 --to 2026-07-01 --variant net
    msci-data variants
"""

from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="msci-data",
        description="Download MSCI index levels as CSV.",
    )
    sub = parser.add_subparsers(dest="command")

    # ── levels ────────────────────────────────────────────────────────────────
    p_levels = sub.add_parser("levels", help="Download end-of-day index levels.")
    p_levels.add_argument(
        "--codes", nargs="+", required=True, metavar="CODE",
        help="One or more MSCI numeric index codes. e.g. 990100 664185",
    )
    p_levels.add_argument(
        "--from", dest="from_date", required=True, metavar="YYYY-MM-DD",
        help="Start date.",
    )
    p_levels.add_argument(
        "--to", dest="to_date", default=None, metavar="YYYY-MM-DD",
        help="End date (defaults to --from for single day).",
    )
    p_levels.add_argument(
        "--variant", default="NETR", metavar="VARIANT",
        help="Return variant: STRD/price, NETR/net (default), GRTR/gross.",
    )
    p_levels.add_argument(
        "--output", default=".", metavar="DIR",
        help="Output directory for CSV (default: current dir).",
    )
    p_levels.add_argument(
        "--s3-bucket", default=None, metavar="BUCKET",
        help="S3 bucket name (saves to S3 instead of local file).",
    )
    p_levels.add_argument(
        "--s3-prefix", default="msci-data/", metavar="PREFIX",
        help="S3 key prefix (default: msci-data/).",
    )

    # ── variants ──────────────────────────────────────────────────────────────
    sub.add_parser("variants", help="List all supported return variants.")

    # ── parse ─────────────────────────────────────────────────────────────────
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    from mscidata import msci

    if args.command == "variants":
        df = msci.list_variants()
        print(df.to_string(index=False))
        return

    if args.command == "levels":
        path = msci.download(
            index_codes=args.codes,
            from_date=args.from_date,
            to_date=args.to_date,
            variant=args.variant,
            output_dir=args.output,
            s3_bucket=args.s3_bucket,
            s3_prefix=args.s3_prefix,
        )
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
