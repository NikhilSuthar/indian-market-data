---
layout: default
title: Capital Market — Equities & SME
nav_order: 2
---

# Capital Market — Equities & SME

**Category:** `capital_market` | **Sub-section:** `equities_sme`

NSE portal path: All Reports → Capital Market → Equities

---

## Daily Datasets

### Bhavcopy (PR) ZIP Bundle
Full daily price bundle — ZIP containing 13 files: OHLC prices, corporate actions, announcements, ETF data, market cap, gainers/losers.

```python
# Returns main pr{date}.csv as DataFrame (OHLC for all securities)
df = nse.get("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22")

# Download full 13-file ZIP to disk
nse.download("capital_market", "equities_sme", "bhavcopy_pr", "2026-05-22", output_dir="./data")
```
```bash
nse-data get capital_market equities_sme bhavcopy_pr 2026-05-22
nse-data dl  capital_market equities_sme bhavcopy_pr 2026-05-22 --out ./data
```
**File:** `PR{DDMMYY}.zip` → extracts `pr{DDMMYYYY}.csv`  
**Columns:** `MKT, SECURITY, PREV_CL_PR, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, NET_TRDVAL, NET_TRDQTY, TRADES`

---

### Securities Bhavcopy with Delivery (Full)
**Recommended daily price file.** OHLC + delivery quantity/% for every security.

```python
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df[df["SYMBOL"] == "RELIANCE"]
```
```bash
nse-data get capital_market equities_sme sec_bhavdata_full 2026-05-22
```
**File:** `sec_bhavdata_full_{DDMMYYYY}.csv`  
**Columns:** `SYMBOL, SERIES, DATE1, PREV_CLOSE, OPEN_PRICE, HIGH_PRICE, LOW_PRICE, CLOSE_PRICE, AVG_PRICE, TTL_TRD_QNTY, TURNOVER_LACS, NO_OF_TRADES, DELIV_QTY, DELIV_PER`

---

### CM Bhavcopy (UDiFF / ISIN format)
Modern ISIN-keyed bhavcopy. Preferred for new integrations — includes lot size, tick size, ISIN.

```python
df = nse.get("capital_market", "equities_sme", "bhav_udiff", "2026-05-22")
```
```bash
nse-data get capital_market equities_sme bhav_udiff 2026-05-22
```
**File:** `BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip`

---

### NSE CM Security Master
ISIN, face value, series, lot size, issued capital for all securities. Reference for SYMBOL→ISIN lookup.

```python
df = nse.get("capital_market", "equities_sme", "security_master", "2026-05-22")
df[df["TckrSymb"] == "RELIANCE"]
```
```bash
nse-data get capital_market equities_sme security_master 2026-05-22
```
**File:** `NSE_CM_security_{DDMMYYYY}.csv.gz` (GZIP → decompressed in memory)  
**~35,000 rows × 120 cols**

---

### Market Activity Report
Daily market summary: turnover, advances/declines, circuit hits.

```python
df = nse.get("capital_market", "equities_sme", "market_activity", "2026-05-22")
```
**File:** `MA{DDMMYY}.csv`

---

### CM Security Volatility (CMVOLT)
Per-security annualized and daily volatility for VaR margin.

```python
df = nse.get("capital_market", "equities_sme", "cmvolt", "2026-05-22")
```
**File:** `CMVOLT_{DDMMYYYY}.CSV`  
**Columns:** `Date, Symbol, Underlying Close Price, Prev Day Close, Log Returns, Prev Volatility, Daily Volatility, Annualised Volatility`

---

### Short Selling Report
Per-security short-sold quantity by members.

```python
df = nse.get("capital_market", "equities_sme", "short_selling", "2026-05-22")
```
**File:** `shortselling_{DDMMYYYY}.csv`

---

### Multiple Trade Orders (MTO)
Delivery qty vs traded qty per security. Input for delivery % computation.

```python
df = nse.get("capital_market", "equities_sme", "mto", "2026-05-22")
```
**File:** `MTO_{DDMMYYYY}.DAT` (fixed-width, best-effort parse)

---

### 52-Week High/Low
Securities hitting new 52-week high or low (adjusted for corporate actions).

```python
df = nse.get("capital_market", "equities_sme", "52wk_high_low", "2026-05-22")
```
**File:** `CM_52_wk_High_low_{DDMMYYYY}.csv` (skips 2 disclaimer rows)

---

### Block Deals / Bulk Deals
Disclosed deals (static files, updated daily).

```python
df = nse.get("capital_market", "equities_sme", "block_deals", "2026-05-22")
df = nse.get("capital_market", "equities_sme", "bulk_deals", "2026-05-22")
```
**Files:** `block.csv`, `bulk.csv`

---

### Index P/E, P/B & Dividend Yield
Daily P/E, P/B and dividend yield per index constituent.

```python
df = nse.get("capital_market", "equities_sme", "pe", "2026-05-22")
```
**File:** `PE_{DDMMYY}.csv`

---

### Regional Indices / Regional Indices Secondary
Daily regional and sectoral index values with surveillance flags.

```python
df = nse.get("capital_market", "equities_sme", "reg_ind",  "2026-05-22")
df = nse.get("capital_market", "equities_sme", "reg1_ind", "2026-05-22")
```

---

### SME Platform EOD / SME Price Bands

```python
df = nse.get("capital_market", "equities_sme", "sme",       "2026-05-22")
df = nse.get("capital_market", "equities_sme", "sme_bands", "2026-05-22")
```

---

### Other Daily Datasets

| Dataset Key | Description | File |
|-------------|-------------|------|
| `eq_band_changes` | Price band reclassifications | `eq_band_changes_{DDMMYYYY}.csv` |
| `sec_list` | Current security list | `sec_list_{DDMMYYYY}.csv` |
| `series_change` | Series reclassifications | `series_change.csv` |
| `mf_var` | MF units VaR for collateral | `MF_VAR_{DDMMYYYY}.csv` |
| `appsec_collval` | Approved security collateral valuation | `APPSEC_COLLVAL_{DDMMYYYY}.csv` |
| `csqr` | Client Segregation Quarterly Report | `CSQR_M_{DDMMYYYY}.csv` |
| `c_stt` | Securities Transaction Tax | `C_STT_{DDMMYYYY}.csv` |
| `c_stt_ind` | STT indicator per security | `C_STT_IND_{DDMMYYYY}.csv` |
| `cm_latency` | CM latency statistics | `CM_Latency_stats{DDMMYYYY}.csv` |
| `fcm_bc` | FCM Interim Bhavcopy (DAT) | `FCM_INTRM_BC{DDMMYYYY}.DAT` |
| `corpbond` | Corporate bond EOD (from PR ZIP) | extracted from `PR{DDMMYY}.zip` |
| `mrg_trading` | Margin trading facility | `mrg_trading_{DDMMYY}.zip` |
| `auction_buy` | Auction buy results | `AUB_{settno}_{DDMMYYYY}.csv` |

### Download-Only (no DataFrame)

```python
# VaR Margin File — 6 intraday snapshots (DAT format)
nse.download("capital_market", "equities_sme", "cvar1", "2026-05-22",
             snapshot=1, output_dir="./data")  # snapshot=1..6
```

### Monthly Datasets

```python
# C_CATG — Security categorisation for VaR
nse.download("capital_market", "equities_sme", "c_catg", "2026-05",
             output_dir="./data")
```
