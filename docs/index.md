---
layout: default
title: Home
nav_order: 1
---

# Indian Market Data

Download **NSE** and **MCX India** market data as **pandas DataFrames** or raw files to **local disk / S3**.

Works from **AWS Lambda**, **Snowflake**, and any cloud environment — no browser, no portal session needed.

```bash
pip install indian-market-data     # NSE + MCX together
pip install nse-archives               # NSE only
pip install mcx-data               # MCX only
```

---

## Packages

| Package | PyPI | Datasets | Exchange |
|---------|------|----------|----------|
| `nse-data` | [pypi.org/project/nse-data](https://pypi.org/project/nse-data/) | 91 | NSE India — equities, F&O, debt, indices, EGR |
| `mcx-data` | [pypi.org/project/mcx-data](https://pypi.org/project/mcx-data/) | 2 | MCX India — commodity spot prices |
| `indian-market-data` | [pypi.org/project/indian-market-data](https://pypi.org/project/indian-market-data/) | All | Umbrella — installs both |

---

## Quick Start — NSE

```python
from nsedata import nse

# Daily prices
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

# Settlement files (available T-1 — previous trading day)
df = nse.get("debt", "corporate", "cbm_list_man", "2026-05-21")

# auto settlement number — no extra params needed
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22")

# Historical index + TRI from niftyindices.com
df = nse.get_historical_index("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")

# Download to S3
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")

# List all datasets
nse.list_datasets()
```

---

## Quick Start — MCX

```python
from mcxdata import mcx

# Today's spot prices — all 28 commodities
df = mcx.get_spot_recent()

# Today's spot price — single commodity
df = mcx.get_spot_recent(commodity="GOLD")

# Historical spot prices (requires specific commodity)
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="SILVER")
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="CRUDEOIL")

# Download to S3
mcx.download("spot", "market", "spot_recent",
             s3_bucket="my-bucket", s3_prefix="raw/mcx/")

# List available commodities
mcx.list_commodities()
```

---

## Quick Start — Combined (indian-market-data)

```python
from nsedata import nse
from mcxdata import mcx

# NSE
nse_df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")

# MCX
mcx_df = mcx.get_spot_recent()
```

---

## NSE Dataset Status Summary

**86 datasets confirmed working** (May 2026 Lambda run):

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Download + DataFrame | 59 | Full support |
| ⬇️ Download only | 8 | DAT/LST/DOC formats |
| 🕐 T-1 (previous day) | 16 | Settlement files — available next trading day |
| ⏭ Portal-only | 8 | Must download from NSE website |

---

## MCX Dataset Status

| Dataset | Description | Status |
|---------|-------------|--------|
| `spot_recent` | Today's spot prices — all 28 commodities | ✅ |
| `spot_archive` | Historical spot prices by commodity + date range | ✅ |

---

## NSE Dataset Categories

| Category | Sub-section | Datasets | Docs |
|----------|-------------|---------|------|
| Capital Market | [Equities & SME](capital-market) | 32 | Daily prices, volatility, deals, master |
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

## MCX Datasets

→ [MCX Spot Market](mcx-spot)

---

## Sources

- NSE: [nseindia.com/all-reports](https://www.nseindia.com/all-reports) via [nsearchives.nseindia.com](https://nsearchives.nseindia.com) — direct file downloads, no Cloudflare
- MCX: [mcxindia.com/market-data/spot-market-price](https://www.mcxindia.com/market-data/spot-market-price) — JSON API via `curl-cffi` Chrome TLS impersonation (bypasses Akamai WAF)
