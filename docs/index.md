---
layout: default
title: Home
nav_order: 1
---

# nse-data

Download NSE India market data as **pandas DataFrames** or raw files to **local disk / S3**.

```bash
pip install nse-data
```

```python
from nsedata import nse

df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
```

---

## How It Works

```
nse.get(category, subcategory, dataset, date)
          │           │           │        └── "2026-05-22" or "2026-05"
          │           │           └── dataset key (e.g. "sec_bhavdata_full")
          │           └── sub-section (e.g. "equities_sme", "equity")
          └── top category ("capital_market", "derivatives", "debt", "egr")
```

All datasets are downloaded from `nsearchives.nseindia.com` — direct file URLs, no Cloudflare, works from AWS Lambda and any cloud.

---

## Dataset Categories

| Category | Sub-section | Datasets | Description |
|----------|------------|----------|-------------|
| [Capital Market — Equities & SME](capital-market) | `equities_sme` | 26 | Daily prices, volatility, deals, master data |
| [Capital Market — Indices](capital-market-indices) | `indices` | 2 | All-indices close, top movers |
| [Capital Market — Mutual Fund](capital-market-mf) | `mutual_fund` | 1 | NSCCL annexures |
| [Capital Market — SLB](capital-market-slb) | `slb` | 10 | Securities Lending & Borrowing |
| [Derivatives — Equity F&O](derivatives-equity) | `equity` | 8 | F&O bhavcopy, contracts, ban list |
| [Derivatives — Commodity](derivatives-commodity) | `commodity` | 3 | Commodity bhavcopy, contracts |
| [Derivatives — Currency](derivatives-currency) | `currency` | 3 | CD bhavcopy, contracts, client positions |
| [Derivatives — Interest Rate](derivatives-ird) | `interest_rate` | 9 | IRF, volatility, FPI/FII positions |
| [Debt — Corporate](debt-corporate) | `corporate` | 13 | CB trades, settlements, SDT |
| [Debt — Debt Segment](debt-segment) | `debt_segment` | 4 | WDM list, daily/weekly bundles |
| [Debt — Tri-Party Repo](debt-trm) | `tri_party_repo` | 1 | TRM bhavcopy |
| [EGR](egr) | `egr` | 1 | Electronic Gold Receipt bhavcopy |

---

## Quick Reference

```python
from nsedata import nse

# List all datasets
nse.list_datasets()

# Filter by category
nse.list_datasets(category="capital_market")

# Get dataset info
nse.get_config_info("capital_market", "equities_sme", "sec_bhavdata_full")

# Download to S3 (IAM role — no credentials in Lambda)
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")
```

---

## Source

All data from [nseindia.com/all-reports](https://www.nseindia.com/all-reports) → served via [nsearchives.nseindia.com](https://nsearchives.nseindia.com)
