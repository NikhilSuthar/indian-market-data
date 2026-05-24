"""
nse-data CLI

Usage:
    nse-data get   <category> <subcategory> <dataset> <date>  [--out FILE]
    nse-data dl    <category> <subcategory> <dataset> <date>  [--out DIR] [--s3-bucket BUCKET] [--s3-prefix PREFIX]
    nse-data list  [--category CATEGORY] [--subcategory SUBCATEGORY]
    nse-data info  <category> <subcategory> <dataset>

Examples:
    nse-data get capital_market equities_sme sec_bhavdata_full 2026-05-22
    nse-data get capital_market indices ind_close_all 2026-05-22
    nse-data get derivatives equity fo_bhav_udiff 2026-05-22
    nse-data dl  capital_market equities_sme bhavcopy_pr 2026-05-22 --out ./data
    nse-data dl  capital_market equities_sme cvar1 2026-05-22 --out ./data --snapshot 1
    nse-data dl  capital_market equities_sme sec_bhavdata_full 2026-05-22 --s3-bucket my-bucket --s3-prefix raw/nse/
    nse-data list
    nse-data list --category capital_market
    nse-data info capital_market equities_sme sec_bhavdata_full
"""

import argparse
import json
import sys

from nsedata import nse


def main():
    parser = argparse.ArgumentParser(
        prog="nse-data",
        description="Download NSE India market data as DataFrames or raw files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command")

    # ─── get: download and print as DataFrame ───────────────────────────
    get_p = subparsers.add_parser("get", help="Download and print a dataset as DataFrame")
    get_p.add_argument("category",    help="e.g. capital_market, derivatives, debt")
    get_p.add_argument("subcategory", help="e.g. equities_sme, indices, equity, slb")
    get_p.add_argument("dataset",     help="Dataset key — see 'nse-data list'")
    get_p.add_argument("date",        help="YYYY-MM-DD (daily) or YYYY-MM (monthly)")
    get_p.add_argument("--out",       default=None, help="Save output CSV to this path")
    get_p.add_argument("--snapshot",  type=int, default=None, help="Snapshot 1-6 (for cvar1)")

    # ─── dl: download raw file ──────────────────────────────────────────
    dl_p = subparsers.add_parser("dl", help="Download raw file to disk or S3")
    dl_p.add_argument("category")
    dl_p.add_argument("subcategory")
    dl_p.add_argument("dataset")
    dl_p.add_argument("date")
    dl_p.add_argument("--out",       default=".", help="Local output directory (default: .)")
    dl_p.add_argument("--s3-bucket", default=None, help="S3 bucket name")
    dl_p.add_argument("--s3-prefix", default="",   help="S3 key prefix")
    dl_p.add_argument("--snapshot",  type=int, default=None)

    # ─── list: list available datasets ──────────────────────────────────
    list_p = subparsers.add_parser("list", help="List available datasets")
    list_p.add_argument("--category",    default=None)
    list_p.add_argument("--subcategory", default=None)
    list_p.add_argument("--df-only",     action="store_true", help="Show only DataFrame-supported")

    # ─── info: show dataset config ──────────────────────────────────────
    info_p = subparsers.add_parser("info", help="Show dataset configuration and URL pattern")
    info_p.add_argument("category")
    info_p.add_argument("subcategory")
    info_p.add_argument("dataset")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "get":
        kwargs = {}
        if args.snapshot: kwargs["snapshot"] = args.snapshot
        df = nse.get(args.category, args.subcategory, args.dataset, args.date, **kwargs)
        print(df.to_string(index=False, max_rows=20))
        print(f"\n{len(df)} rows × {len(df.columns)} columns")
        if args.out:
            df.to_csv(args.out, index=False)
            print(f"Saved: {args.out}")
        else:
            out = f"{args.dataset}_{args.date}.csv"
            df.to_csv(out, index=False)
            print(f"Saved: {out}")

    elif args.command == "dl":
        kwargs = {}
        if args.snapshot: kwargs["snapshot"] = args.snapshot
        result = nse.download(
            args.category, args.subcategory, args.dataset, args.date,
            output_dir=args.out,
            s3_bucket=args.s3_bucket,
            s3_prefix=args.s3_prefix,
            **kwargs,
        )
        print(f"Downloaded: {result}")

    elif args.command == "list":
        df = nse.list_datasets(args.category, args.subcategory)
        if args.df_only:
            df = df[df["df_supported"]]
        print(df[["category", "subcategory", "dataset", "name", "frequency", "df_supported"]].to_string(index=False))
        print(f"\nTotal: {len(df)} datasets")

    elif args.command == "info":
        info = nse.get_config_info(args.category, args.subcategory, args.dataset)
        for k, v in info.items():
            print(f"  {k:<18}: {v}")


if __name__ == "__main__":
    main()
