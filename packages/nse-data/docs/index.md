---
layout: default
title: Home
nav_order: 1
---

# nse-data

Download NSE India market data as **pandas DataFrames** or raw files to **local disk / S3**.

Works from **AWS Lambda**, **Snowflake**, and any cloud environment.

```bash
pip install nse-data
```

---

## Status Summary

**83 datasets confirmed working** from actual Lambda + local run (May 2026):

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Download + DataFrame | 59 | Full support — download to disk + parse as DataFrame |
| ⬇️ Download only | 8 | DAT/LST/DOC formats — download raw file |
| 🕐 T-1 (previous day) | 16 | Settlement files — available next trading day |
| ⏭ Portal-only | 8 | No direct archive URL — download from NSE website |

> **Note:** `auction_buy` and `csqr` previously required a `settno` param. Settlement number is now **auto-calculated** from the date — no extra params needed.

---

## Quick Start

```python
from nsedata import nse

# DataFrame
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

# T-1 datasets — use previous trading day
df = nse.get("debt", "corporate", "cbm_list_man", "2026-05-21")

# auction_buy and csqr — settno auto-calculated, no extra params needed
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22")
df = nse.get("capital_market", "equities_sme", "csqr", "2026-05-22")

# Inspect settlement number for any date
nse.get_settlement_number("2026-05-22")  # → "2026094"

# Download to disk
nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22", output_dir="./data")

# Download to S3 (IAM role — no credentials needed)
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")

# List all datasets
nse.list_datasets()
```

---

## Dataset Categories

| Category | Sub-section | Datasets | Docs |
|----------|------------|---------|------|
| Capital Market | [Equities & SME](capital-market) | 32 | Daily prices, volatility, deals, master data |
| Capital Market | [Indices](capital-market-indices) | 2 | All-indices close, top movers |
| Capital Market | [Mutual Fund](capital-market-mf) | 1 | NSCCL annexures |
| Capital Market | [SLB](capital-market-slb) | 12 | Securities Lending & Borrowing |
| Derivatives | [Equity F&O](derivatives-equity) | 8 | F&O bhavcopy, contracts, ban list |
| Derivatives | [Commodity](derivatives-commodity) | 3 | Commodity bhavcopy, contracts |
| Derivatives | [Currency](derivatives-currency) | 3 | CD bhavcopy, contracts |
| Derivatives | [Interest Rate](derivatives-ird) | 9 | IRF, volatility, FPI/FII positions |
| Debt | [Corporate](debt-corporate) | 15 | CB trades, settlements (T-1) |
| Debt | [Debt Segment](debt-segment) | 4 | WDM daily/weekly bundles |
| Debt | [Tri-Party Repo](debt-trm) | 1 | TRM bhavcopy |
| EGR | [EGR](egr) | 1 | Electronic Gold Receipt bhavcopy |

---

## Source

All data from [nseindia.com/all-reports](https://www.nseindia.com/all-reports) served via [nsearchives.nseindia.com](https://nsearchives.nseindia.com) — direct file downloads, no Cloudflare.
