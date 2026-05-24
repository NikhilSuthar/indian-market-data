---
layout: default
title: Capital Market — Equities & SME
nav_order: 2
---

# Capital Market — Equities & SME

**Category:** `capital_market` | **Sub-section:** `equities_sme`

NSE portal: [All Reports → Capital Market → Equities](https://www.nseindia.com/all-reports)

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Confirmed working — DataFrame + Download |
| ⬇️ | Download only (no DataFrame — DAT/T01 format) |
| 🕐 | T-1 only — available previous trading day (settlement files) |
| ⚙️ | Requires extra param (e.g. settno) |
| ⏭ | Portal-only — download from NSE website manually |

---

## Daily Datasets

### ✅ Bhavcopy (PR) Daily ZIP Bundle
ZIP containing 13 files. `reports.get()` extracts the main `pr{date}.csv` (OHLC prices).

```python
df = nse.get("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22")
nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22", output_dir="./data")
```
`PR{DDMMYY}.zip` | 3,500+ rows × 14 cols

---

### ✅ Securities Bhavcopy with Delivery (Full) — **Recommended**
Most comprehensive daily price file. OHLC + delivery qty/% for every security.

```python
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df[df["SYMBOL"] == "RELIANCE"]
```
`sec_bhavdata_full_{DDMMYYYY}.csv` | 3,200+ rows × 15 cols

---

### ✅ CM Bhavcopy (UDiFF / ISIN format)
Modern ISIN-keyed bhavcopy. Preferred for new integrations.

```python
df = nse.get("capital_market", "equities_sme", "bhav_udiff", "2026-05-22")
```
`BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | 3,374 rows × 34 cols

---

### ✅ NSE CM Security Master
ISIN, face value, series, lot size for all securities. Reference for SYMBOL→ISIN lookup.

```python
df = nse.get("capital_market", "equities_sme", "security_master", "2026-05-22")
df[df["TckrSymb"] == "RELIANCE"]
```
`NSE_CM_security_{DDMMYYYY}.csv.gz` | 35,000+ rows × 120 cols

---

### ✅ Market Activity Report
Daily market summary: turnover, advances/declines.

```python
df = nse.get("capital_market", "equities_sme", "market_activity", "2026-05-22")
```
`MA{DDMMYY}.csv`

---

### ✅ CM Security Volatility (CMVOLT)
Per-security annualized and daily volatility for VaR margin.

```python
df = nse.get("capital_market", "equities_sme", "cmvolt", "2026-05-22")
```
`CMVOLT_{DDMMYYYY}.CSV` | 4,818 rows × 8 cols

---

### ✅ Short Selling Report

```python
df = nse.get("capital_market", "equities_sme", "short_selling", "2026-05-22")
```
`shortselling_{DDMMYYYY}.csv` | 85 rows × 4 cols

---

### ✅ Block Deals / Bulk Deals (static files, updated daily)

```python
df = nse.get("capital_market", "equities_sme", "block_deals", "2026-05-22")
df = nse.get("capital_market", "equities_sme", "bulk_deals", "2026-05-22")
```
`block.csv` | `bulk.csv`

---

### ✅ Index P/E, P/B & Dividend Yield

```python
df = nse.get("capital_market", "equities_sme", "pe", "2026-05-22")
```
`PE_{DDMMYY}.csv` | 2,181 rows × 3 cols

---

### ✅ Regional Indices / Regional Indices Secondary

```python
df = nse.get("capital_market", "equities_sme", "reg_ind",  "2026-05-22")
df = nse.get("capital_market", "equities_sme", "reg1_ind", "2026-05-22")
```
`REG_IND{DDMMYY}.csv` / `REG1_IND{DDMMYY}.csv` | 2,935 rows

---

### ✅ SME Platform EOD / SME Price Bands

```python
df = nse.get("capital_market", "equities_sme", "sme",       "2026-05-22")
df = nse.get("capital_market", "equities_sme", "sme_bands", "2026-05-22")
```
`sme{DDMMYYYY}.csv` | 442 rows × 14 cols

---

### ✅ Equity Price Band Changes / Security List / Series Change

```python
df = nse.get("capital_market", "equities_sme", "eq_band_changes", "2026-05-22")
df = nse.get("capital_market", "equities_sme", "sec_list",        "2026-05-22")
df = nse.get("capital_market", "equities_sme", "series_change",   "2026-05-22")
```

---

### ✅ Mutual Fund VaR / APPSEC Collateral Valuation / C_STT / C_STT_IND

```python
df = nse.get("capital_market", "equities_sme", "mf_var",        "2026-05-22")  # 7,037 rows
df = nse.get("capital_market", "equities_sme", "appsec_collval","2026-05-22")  # 948 rows
df = nse.get("capital_market", "equities_sme", "c_stt",         "2026-05-22")  # 12,397 rows
df = nse.get("capital_market", "equities_sme", "c_stt_ind",     "2026-05-22")  # 1,067 rows
```

---

### ✅ FCM Interim Bhavcopy (DAT — best-effort parse)

```python
df = nse.get("capital_market", "equities_sme", "fcm_bc", "2026-05-22")
# Or download raw DAT:
nse.download("capital_market", "equities_sme", "fcm_bc", "2026-05-22", output_dir="./data")
```
`FCM_INTRM_BC{DDMMYYYY}.DAT` | 3,373 rows × 17 cols

---

### ⬇️ VaR Margin File (C_VAR1) — 6 intraday snapshots

```python
# Download only — DAT format, snapshot 1–6
for snap in range(1, 7):
    nse.download("capital_market", "equities_sme", "cvar1", "2026-05-22",
                 snapshot=snap, output_dir="./data")
```
`C_VAR1_{DDMMYYYY}_{1..6}.DAT`

---

### ✅ Corporate Bond (from PR ZIP)

```python
df = nse.get("capital_market", "equities_sme", "corpbond", "2026-05-22")
```
Extracted from `PR{DDMMYY}.zip` | 128 rows × 15 cols

---

### 🕐 CM Latency Statistics (T-1)
Only published the next trading day.

```python
df = nse.get("capital_market", "equities_sme", "cm_latency", "2026-05-21")  # use T-1 date
```

---

### 🕐 Margin Trading Facility Report (T-1 / intermittent)

```python
nse.download("capital_market", "equities_sme", "mrg_trading", "2026-05-20", output_dir="./data")
```
`mrg_trading_{DDMMYY}.zip`

---

### ⚙️ Auction Buy File — auto settlement number
Settlement number (`settno`) is **auto-calculated** from the date. You can also override it.

```python
# Auto-calculate settno (recommended)
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22")

# Or provide it explicitly (settno = YYYY + NSE trading day count from Jan 1)
df = nse.get("capital_market", "equities_sme", "auction_buy", "2026-05-22", settno="2026094")
```
`AUB_{YYYYNNN}_{DDMMYYYY}.csv` | 144 rows

Settlement number formula: `YYYY` + 3-digit count of NSE trading days from Jan 1 (e.g. May 22 2026 = 94th trading day → `2026094`).

---

### ⚙️ CSQR — auto settlement number
Same auto-calculation as auction_buy.

```python
# Auto-calculate settno (recommended)
df = nse.get("capital_market", "equities_sme", "csqr", "2026-05-22")

# Or provide explicitly
df = nse.get("capital_market", "equities_sme", "csqr", "2026-05-22", settno="2026094")
```
`CSQR_M{YYYYNNN}_{DDMMYYYY}.csv` | 13,000+ rows

---

### ⬇️ Daily Settlement Statistics (DOC — download only)

```python
nse.download("capital_market", "equities_sme", "daily_settlement_doc", "2026-05-22", output_dir="./data")
```

---

## Monthly Datasets

### ✅ CM Security Categorisation (C_CATG)

```python
df = nse.get("capital_market", "equities_sme", "c_catg", "2026-05")
```
`C_CATG_{MON}{YYYY}.T01` | 13,580 rows

---

## Portal-Only (⏭ no direct archive URL)

Download manually from [nseindia.com/all-reports](https://www.nseindia.com/all-reports):

| Dataset | Description |
|---------|-------------|
| `52wk_high_low` | 52-Week High/Low (portal API) |
