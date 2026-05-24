---
layout: default
title: Python API — NSE
nav_order: 1
parent: NSE India
---

# Python API — NSE

```bash
pip install nse-archives
```

---

## Quick Start

```python
from nsedata import nse

# Daily prices
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")

# F&O
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

# Monthly
df = nse.get("capital_market", "equities_sme", "c_catg", "2026-05")

# Historical TRI from niftyindices.com
df = nse.get_tri("NIFTY 50", "01-Jan-2026", "31-Mar-2026")
```

---

## `nse.get()` — DataFrame

```python
nse.get(category, subcategory, dataset, date, **kwargs) → pd.DataFrame
```

| Parameter | Type | Example |
|-----------|------|---------|
| `category` | str | `"capital_market"`, `"derivatives"`, `"debt"`, `"egr"` |
| `subcategory` | str | `"equities_sme"`, `"equity"`, `"corporate"` |
| `dataset` | str | `"sec_bhavdata_full"`, `"fo_secban"` |
| `date` | str | `"2026-05-22"` (daily) or `"2026-05"` (monthly) |

**Examples:**

```python
from nsedata import nse

# ── Capital Market ───────────────────────────────────────────────
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "equities_sme", "bhavcopy_pr",        "2026-05-22")
df = nse.get("capital_market", "equities_sme", "bhav_udiff",         "2026-05-22")
df = nse.get("capital_market", "equities_sme", "security_master",    "2026-05-22")
df = nse.get("capital_market", "equities_sme", "cmvolt",             "2026-05-22")
df = nse.get("capital_market", "equities_sme", "market_activity",    "2026-05-22")
df = nse.get("capital_market", "equities_sme", "short_selling",      "2026-05-22")
df = nse.get("capital_market", "equities_sme", "mto",                "2026-05-22")
df = nse.get("capital_market", "equities_sme", "block_deals",        "2026-05-22")
df = nse.get("capital_market", "equities_sme", "bulk_deals",         "2026-05-22")
df = nse.get("capital_market", "equities_sme", "pe",                 "2026-05-22")

# Settlement number auto-calculated — no extra param needed
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22")
df = nse.get("capital_market", "equities_sme", "csqr",        "2026-05-22")

# Monthly
df = nse.get("capital_market", "equities_sme", "c_catg", "2026-05")

# ── Indices ──────────────────────────────────────────────────────
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
df = nse.get("capital_market", "indices", "top_movers",    "2026-05-22")

# ── F&O ──────────────────────────────────────────────────────────
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")
df = nse.get("derivatives", "equity", "fo_contract",   "2026-05-22")
df = nse.get("derivatives", "equity", "fo_secban",     "2026-05-22")
df = nse.get("derivatives", "equity", "fovolt",        "2026-05-22")

# ── Commodity Derivatives ────────────────────────────────────────
df = nse.get("derivatives", "commodity", "co_bhav_udiff", "2026-05-22")
df = nse.get("derivatives", "commodity", "co_contract",   "2026-05-22")

# ── Interest Rate Derivatives ────────────────────────────────────
df = nse.get("derivatives", "interest_rate", "irf_bhavcopy", "2026-05-22")
df = nse.get("derivatives", "interest_rate", "i_volt",        "2026-05-22")
df = nse.get("derivatives", "interest_rate", "fpi_long",      "2026-05-22")

# ── Debt ─────────────────────────────────────────────────────────
# T-1 datasets — use previous trading day
df = nse.get("debt", "corporate", "cbm_trd",              "2026-05-21")
df = nse.get("debt", "corporate", "cbm_list_man",         "2026-05-21")
df = nse.get("debt", "corporate", "corporate_bond_report","2026-05-21")
df = nse.get("debt", "debt_segment", "dly_bundle",        "2026-05-22")
df = nse.get("debt", "tri_party_repo", "trm_bc",          "2026-05-22")

# ── EGR ──────────────────────────────────────────────────────────
df = nse.get("egr", "egr", "egr_bc", "2026-05-22")

# ── VaR snapshots (download-only, snapshot 1–6) ──────────────────
nse.download("capital_market", "equities_sme", "cvar1", "2026-05-22",
             snapshot=1, output_dir="./data")
```

---

## `nse.download()` — Save to Disk or S3

```python
nse.download(category, subcategory, dataset, date,
             output_dir=".", s3_bucket=None, s3_prefix="",
             **kwargs) → str
```

Returns local file path or `"s3://bucket/key"`.

```python
from nsedata import nse

# Save to local folder
path = nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
                    output_dir="./data")
# → "./data/sec_bhavdata_full_22052026.csv"

# Save to S3 (Lambda with IAM role — no credentials needed)
uri = nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
                   s3_bucket="my-bucket", s3_prefix="raw/nse/equity/")
# → "s3://my-bucket/raw/nse/equity/sec_bhavdata_full_22052026.csv"
```

---

## `nse.list_datasets()` — Discover datasets

```python
df = nse.list_datasets()
df = nse.list_datasets(category="derivatives")
```

Returns DataFrame: `category, subcategory, dataset, name, frequency, df_supported, format`

---

## Historical Index + TRI (niftyindices.com)

```python
from nsedata import nse

# Price Index (OHLC)
df = nse.get_historical_index("NIFTY 50",    "01-Jan-2026", "31-Mar-2026")
df = nse.get_historical_index("NIFTY BANK",  "01-Jan-2026", "31-Mar-2026")
df = nse.get_historical_index("NIFTY IT",    "01-Jan-2026", "31-Mar-2026")

# Total Return Index
df = nse.get_tri("NIFTY 50",    "01-Jan-2026", "31-Mar-2026")
df = nse.get_tri("NIFTY BANK",  "01-Jan-2026", "31-Mar-2026")
```

**Date format:** `"DD-Mon-YYYY"` e.g. `"01-Jan-2026"`, `"31-Mar-2026"`

**Available indices (30):** NIFTY 50, NIFTY NEXT 50, NIFTY 100, NIFTY 200, NIFTY 500, NIFTY MIDCAP 50/100/150, NIFTY SMALLCAP 50/100/250, NIFTY BANK, NIFTY IT, NIFTY AUTO, NIFTY PHARMA, NIFTY FMCG, NIFTY METAL, NIFTY ENERGY, NIFTY REALTY, NIFTY MEDIA, NIFTY PSE, NIFTY PSU BANK, NIFTY PVT BANK, NIFTY FIN SERVICE, NIFTY OIL & GAS, NIFTY INFRA, NIFTY MNC, NIFTY CONSUMPTION, NIFTY SERVICES, NIFTY COMMODITIES

> **Note:** Works from residential IPs. Lambda IPs also work — Cloudflare does not block Lambda.

---

## Settlement Number (auto-calculated)

`auction_buy` and `csqr` datasets use a settlement number in the filename. It is **auto-calculated** from the date — no extra param needed:

```python
# Auto-calculate (recommended)
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22")

# Override manually if needed
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22",
             settno="2026094")

# Inspect settlement number for any date
info = nse.get_settlement_number("2026-05-22")
# → "2026094"
```

Formula: `YYYY` + 3-digit count of NSE trading days from Jan 1 (May 22 2026 = 94th → `2026094`)

---

## Error Handling

```python
from nsedata import nse

try:
    df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-24")
except RuntimeError as e:
    print(f"Download failed: {e}")
    # RuntimeError: HTTP 404 — file not available (weekend/holiday)

try:
    df = nse.get("capital_market", "equities_sme", "cvar1", "2026-05-22")
except ValueError as e:
    print(f"Format error: {e}")
    # ValueError: use download() for DAT format datasets
```

Common errors:
- `RuntimeError: HTTP 404` — not a trading day or file not yet published
- `RuntimeError: HTTP 403` — NSE rate-limiting (retry after a few seconds)
- `ValueError` — wrong dataset key or download-only format
