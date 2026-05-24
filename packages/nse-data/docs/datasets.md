---
layout: default
title: Dataset Catalog
nav_order: 6
---

# Complete Dataset Catalog

All 79 downloadable datasets from NSE India supported by `nse-data`, organized by market segment.

---

## Capital Market — Equities & Cash

### Daily Price Reports

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 1 | **Bhavcopy (PR) Daily Zip Bundle** | `PR{DDMMYY}.zip` | ZIP (13 files) | `nse-data reports --type bhavcopy --date 2026-04-17` |
| 2 | **Securities Bhavcopy with Delivery (Full)** | `sec_bhavdata_full_{DDMMYYYY}.csv` | CSV | `nse-data reports --type sec_bhavdata --date 2026-04-17` |
| 3 | **Capital Market Bhavcopy (UDiFF/ISIN)** | `BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | `nse-data reports --type bhav_udiff --date 2026-04-17` |
| 4 | **Market Activity Report (MA)** | `MA{DDMMYY}.csv` | CSV | `nse-data reports --type market_activity --date 2026-04-17` |
| 5 | **SME Platform EOD Market Data** | `sme{DDMMYYYY}.csv` | CSV | `nse-data reports --type sme --date 2026-04-17` |

**Source URL patterns:**
```
https://nsearchives.nseindia.com/content/historical/EQUITIES/{YYYY}/{MON}/PR{DDMMYY}.zip
https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip
https://nsearchives.nseindia.com/archives/equities/mkt/MA{DDMMYY}.csv
https://nsearchives.nseindia.com/archives/sme/sme{DDMMYYYY}.csv
```

---

### Corporate Actions & Deals

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 6 | **Block Deals** | `block.csv` | CSV | `nse-data reports --type block_deals --date 2026-04-17` |
| 7 | **Bulk Deals (Daily)** | `bulk.csv` | CSV | `nse-data reports --type bulk_deals --date 2026-04-17` |
| 8 | **Bulk Deals (Historical range)** | `Bulk-Deals-{DD-MM-YYYY}-to-{DD-MM-YYYY}.csv` | CSV | `nse-data reports --type bulk_deals_hist --from 2026-04-13 --to 2026-04-20` |
| 9 | **Short Selling Daily Report** | `shortselling_{DDMMYYYY}.csv` | CSV | `nse-data reports --type short_selling --date 2026-04-17` |

**Source URL patterns:**
```
https://nsearchives.nseindia.com/content/equities/block.csv
https://nsearchives.nseindia.com/content/equities/bulk.csv
https://nsearchives.nseindia.com/archives/equities/shortSelling/shortselling_{DDMMYYYY}.csv
```

---

### Security Master & Reference Data

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 10 | **NSE CM Security Master** | `NSE_CM_security_{DDMMYYYY}.csv.gz` | GZIP→CSV | `nse-data reports --type security_master --date 2026-04-17` |
| 11 | **CM Security List (sec_list)** | `sec_list_{DDMMYYYY}.csv` | CSV | `nse-data reports --type sec_list --date 2026-04-17` |
| 12 | **Series Change Notifications** | `series_change.csv` | CSV | `nse-data reports --type series_change --date 2026-04-17` |
| 13 | **Circuit Filter Changes** | `circuit_{DDMMYYYY}.csv` | CSV | `nse-data reports --type circuit --date 2026-04-17` |
| 14 | **Equity Price Band Changes** | `eq_band_changes_{DDMMYYYY}.csv` | CSV | `nse-data reports --type band_changes --date 2026-04-17` |
| 15 | **Capital Market 52-Week High/Low** | `CM_52_wk_High_low_{DDMMYYYY}.csv` | CSV | `nse-data reports --type cm_52wk --date 2026-04-17` |

**Source URL patterns:**
```
https://nsearchives.nseindia.com/content/cm/NSE_CM_security_{DDMMYYYY}.csv.gz
https://nsearchives.nseindia.com/content/equities/CM_52_wk_High_low_{DDMMYYYY}.csv
```

---

### PR Bundle Sub-Files (extracted from PR zip)

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 16 | **PR - Security-wise EOD (pr)** | `pr{DDMMYYYY}.csv` | CSV | `nse-data reports --type pr --date 2026-04-17` |
| 17 | **PR - EOD + Symbol/Series (pd)** | `pd{DDMMYYYY}.csv` | CSV | `nse-data reports --type pd --date 2026-04-17` |
| 18 | **PR - ETF Market Data (etf)** | `etf{DDMMYYYY}.csv` | CSV | `nse-data reports --type etf --date 2026-04-17` |
| 19 | **PR - Corporate Bond (corpbond)** | `corpbond{DDMMYYYY}.csv` | CSV | `nse-data reports --type corpbond --date 2026-04-17` |
| 20 | **PR - Market Capitalisation (mcap)** | `mcap{DDMMYYYY}.csv` | CSV | `nse-data reports --type mcap --date 2026-04-17` |
| 21 | **PR - Gainers & Losers (gl)** | `gl{DDMMYYYY}.csv` | CSV | `nse-data reports --type gainers_losers --date 2026-04-17` |
| 22 | **PR - 52-Week New High/Low (hl)** | `hl{DDMMYYYY}.csv` | CSV | `nse-data reports --type hl --date 2026-04-17` |
| 23 | **PR - Price-Band Hits (bh)** | `bh{DDMMYYYY}.csv` | CSV | `nse-data reports --type band_hits --date 2026-04-17` |
| 24 | **PR - Top 25 by Traded Value (tt)** | `tt{DDMMYYYY}.csv` | CSV | `nse-data reports --type top25 --date 2026-04-17` |
| 25 | **PR - Corporate Actions (bc)** | `bc{DDMMYYYY}.csv` | CSV | `nse-data reports --type corp_actions --date 2026-04-17` |
| 26 | **PR - Board Meetings (bm)** | `bm{DDMMYYYY}.txt` | TXT | `nse-data reports --type board_meetings --date 2026-04-17` |
| 27 | **PR - Announcements (an)** | `an{DDMMYYYY}.txt` | TXT | `nse-data reports --type announcements --date 2026-04-17` |

All extracted from: `https://nsearchives.nseindia.com/content/historical/EQUITIES/{YYYY}/{MON}/PR{DDMMYY}.zip`

---

### Indices

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 28 | **All Indices Daily Close (ind_close_all)** | `ind_close_all_{DDMMYYYY}.csv` | CSV | `nse-data reports --type ind_close_all --date 2026-04-17` |
| 29 | **Index P/E, P/B & Div Yield (PE)** | `PE_{DDMMYY}.csv` | CSV | `nse-data reports --type pe --date 2026-04-17` |
| 30 | **Regional Indices (REG_IND)** | `REG_IND{DDMMYY}.csv` | CSV | `nse-data reports --type reg_ind --date 2026-04-17` |
| 31 | **Regional Indices Secondary (REG1_IND)** | `REG1_IND{DDMMYY}.csv` | CSV | `nse-data reports --type reg1_ind --date 2026-04-17` |
| 32 | **Index Top Movers** | `top10nifty50_{DDMMYY}.csv` | CSV | `nse-data reports --type top_movers --date 2026-04-17` |

**Source URL patterns:**
```
https://nsearchives.nseindia.com/content/indices/ind_close_all_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/archives/equities/mkt/PE_{DDMMYY}.csv
https://nsearchives.nseindia.com/archives/equities/mkt/REG_IND{DDMMYY}.csv
https://nsearchives.nseindia.com/archives/equities/mkt/REG1_IND{DDMMYY}.csv
```

---

### Risk & Margin (Capital Market)

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 33 | **CM Security Volatility (CMVOLT)** | `CMVOLT_{DDMMYYYY}.CSV` | CSV | `nse-data reports --type cmvolt --date 2026-04-17` |
| 34 | **CM VaR Margin (C_VAR1)** | `C_VAR1_{DDMMYYYY}_{N}.DAT` | DAT | `nse-data reports --type cvar1 --date 2026-04-17 --snapshot 1` |
| 35 | **CM Security Categorisation (C_CATG)** | `C_CATG_{MON}{YYYY}.T01` | T01 | `nse-data reports --type c_catg --month APR2026` |
| 36 | **FCM Interim Bhavcopy** | `FCM_INTRM_BC{DDMMYYYY}.DAT` | DAT | `nse-data reports --type fcm_bc --date 2026-04-17` |
| 37 | **Multiple Trade Orders (MTO)** | `MTO_{DDMMYYYY}.DAT` | DAT | `nse-data reports --type mto --date 2026-04-17` |
| 38 | **Client Segregation (CSQR_M)** | `CSQR_M_{DDMMYYYY}.csv` | CSV | `nse-data reports --type csqr --date 2026-04-17` |
| 39 | **STT Report (C_STT)** | `C_STT_{DDMMYYYY}.csv` | CSV | `nse-data reports --type stt --date 2026-04-17` |
| 40 | **Margin Trading Report** | `mrg_trading_{DDMMYYYY}.csv` | CSV | `nse-data reports --type margin_trading --date 2026-04-17` |
| 41 | **Auction Buy (AUB)** | `AUB_{SETTLE}_{DDMMYYYY}.csv` | CSV | `nse-data reports --type auction --date 2026-04-17` |

**Source URL patterns:**
```
https://nsearchives.nseindia.com/archives/nsccl/volt/CMVOLT_{DDMMYYYY}.CSV
https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{DDMMYYYY}_{N}.DAT
https://nsearchives.nseindia.com/archives/nsccl/cs/C_CATG_{MON}{YYYY}.T01
https://nsearchives.nseindia.com/archives/nsccl/fcm/FCM_INTRM_BC{DDMMYYYY}.DAT
https://nsearchives.nseindia.com/archives/equities/mto/MTO_{DDMMYYYY}.DAT
https://nsearchives.nseindia.com/archives/nsccl/csqr/CSQR_M_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/archives/nsccl/stt/C_STT_{DDMMYYYY}.csv
```

---

## Derivatives — Equity F&O

### Daily Trade Data

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 42 | **F&O Bhavcopy (UDiFF)** | `BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | `nse-data derivatives --type fo_bhav_udiff --date 2026-04-17` |
| 43 | **F&O Daily Combined (fo)** | `fo{DDMMYYYY}bhav.csv.zip` | ZIP→CSV | `nse-data derivatives --type fo_bhav --date 2026-04-17` |
| 44 | **Futures on Index (futidx)** | `futidx{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type futidx --date 2026-04-17` |
| 45 | **Futures on Stocks (futstk)** | `futstk{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type futstk --date 2026-04-17` |
| 46 | **Options on Index (optidx)** | `optidx{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type optidx --date 2026-04-17` |
| 47 | **Options on Stocks (optstk)** | `optstk{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type optstk --date 2026-04-17` |
| 48 | **Top Traded Futures (ttfut)** | `ttfut{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type ttfut --date 2026-04-17` |
| 49 | **Top Traded Options (ttopt)** | `ttopt{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type ttopt --date 2026-04-17` |
| 50 | **Futures IVX** | `futivx{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type futivx --date 2026-04-17` |

### Open Interest & Positions

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 51 | **F&O Combined OI (combineoi)** | `combineoi_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type combineoi --date 2026-04-17` |
| 52 | **Combined OI Derivatives-Equity Link** | `combineoi_deleq_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type combineoi_deleq --date 2026-04-17` |
| 53 | **NCL Open Interest (ncloi)** | `ncloi_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type ncloi --date 2026-04-17` |
| 54 | **F&O Participant OI** | `fao_participant_oi_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fao_participant_oi --date 2026-04-17` |
| 55 | **F&O Participant Volume** | `fao_participant_vol_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fao_participant_vol --date 2026-04-17` |
| 56 | **Combined FPI Long Positions** | `Combined_FPI_long_psn_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fpi_long --date 2026-04-17` |
| 57 | **FII Long Positions** | `fii_longpos_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fii_long --date 2026-04-17` |
| 58 | **Early Warning Position Limits (EWPL)** | `EWPL_{DDMMYYYY}.CSV` | CSV | `nse-data derivatives --type ewpl --date 2026-04-17` |

### Risk & Settlement (F&O)

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 59 | **F&O Settlement Prices** | `FOSett_prce_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fo_sett --date 2026-04-17` |
| 60 | **F&O Volatility (FOVOLT)** | `FOVOLT_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fovolt --date 2026-04-17` |
| 61 | **F&O Contract Deltas** | `Contract_Delta_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fo_delta --date 2026-04-17` |
| 62 | **F&O Security Ban List** | `fo_secban_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type fo_secban --date 2026-04-17` |
| 63 | **F&O Bhavcopy (FNO_BC DAT)** | `FNO_BC{DDMMYYYY}.DAT` | DAT | `nse-data derivatives --type fno_bc --date 2026-04-17` |

### Contract Masters (F&O)

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 64 | **F&O Contract Master** | `NSE_FO_contract_{DDMMYYYY}.csv.gz` | GZIP→CSV | `nse-data derivatives --type fo_contract --date 2026-04-17` |
| 65 | **F&O Spread Contract Master** | `NSE_FO_spdcontract_{DDMMYYYY}.csv.gz` | GZIP→CSV | `nse-data derivatives --type fo_spread_contract --date 2026-04-17` |
| 66 | **F&O Position Limits (fopl)** | `fopl_{mon}{yyyy}.csv` | CSV | `nse-data derivatives --type fopl --month apr2026` |
| 67 | **Member Position Limit (mpl)** | `mpl_{mon}{yyyy}.csv` | CSV | `nse-data derivatives --type mpl --month apr2026` |

---

## Derivatives — Commodity

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 68 | **Commodity Bhavcopy UDiFF** | `BhavCopy_NSE_CO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | `nse-data derivatives --type co_bhav_udiff --date 2026-04-17` |
| 69 | **Commodity Bhavcopy (CO_BC DAT)** | `CO_BC{DDMMYYYY}.DAT` | DAT | `nse-data derivatives --type co_bc --date 2026-04-17` |
| 70 | **Commodity Settlement Prices** | `CO_sett_prce_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type co_sett --date 2026-04-17` |
| 71 | **Commodity Volatility (CO_VOLT)** | `CO_VOLT_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type co_volt --date 2026-04-17` |
| 72 | **Commodity Contract Master** | `NSE_COM_contract_{DDMMYYYY}.csv.gz` | GZIP→CSV | `nse-data derivatives --type co_contract --date 2026-04-17` |
| 73 | **Commodity F&O Combined** | `CO_NSE_FO{DDMMYY}.csv` | CSV | `nse-data derivatives --type co_fo --date 2026-04-17` |
| 74 | **Commodity Options** | `CO_NSE_OP{DDMMYY}.csv` | CSV | `nse-data derivatives --type co_op --date 2026-04-17` |

---

## Derivatives — Currency

| # | Dataset | File Pattern | Format | Command |
|---|---------|-------------|--------|---------|
| 75 | **Currency Derivatives Bhavcopy (UDiFF)** | `BhavCopy_NSE_CD_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | `nse-data derivatives --type cd_bhav_udiff --date 2026-04-17` |
| 76 | **Currency Derivatives Settlement Prices** | `CDSett_prce_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type cd_sett --date 2026-04-17` |
| 77 | **Currency Volatility (X_VOLT)** | `X_VOLT_{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type x_volt --date 2026-04-17` |
| 78 | **Currency Contract Master** | `NSE_CD_contract_{DDMMYYYY}.csv.gz` | GZIP→CSV | `nse-data derivatives --type cd_contract --date 2026-04-17` |
| 79 | **Tri-Party Repo Bhavcopy (TRM_BC)** | `TRM_BC{DDMMYYYY}.csv` | CSV | `nse-data derivatives --type trm_bc --date 2026-04-17` |

**Source URL patterns:**
```
https://nsearchives.nseindia.com/content/cd/BhavCopy_NSE_CD_0_0_0_{YYYYMMDD}_F_0000.csv.zip
https://nsearchives.nseindia.com/archives/nsccl/cd/CDSett_prce_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/archives/nsccl/volt/X_VOLT_{DDMMYYYY}.csv
https://nsearchives.nseindia.com/content/cd/NSE_CD_contract_{DDMMYYYY}.csv.gz
https://nsearchives.nseindia.com/archives/trep/TRM_BC{DDMMYYYY}.csv
```

---

## Date Format Reference

| Placeholder | Format | Example (17-Apr-2026) |
|-------------|--------|----------------------|
| `{DDMMYY}` | DDMMYY | `170426` |
| `{DDMMYYYY}` | DDMMYYYY | `17042026` |
| `{YYYYMMDD}` | YYYYMMDD | `20260417` |
| `{YYYY}` | YYYY | `2026` |
| `{MON}` | MON (uppercase 3-letter) | `APR` |
| `{mon}` | mon (lowercase 3-letter) | `apr` |
| `{DD-MM-YYYY}` | DD-MM-YYYY | `17-04-2026` |

---

## Implementation Status

| Status | Meaning |
|--------|---------|
| ✅ Implemented | Available in current release |
| 🚧 Planned | URL pattern known, coming in next release |

### v0.1.0 (Current)
✅ Bhavcopy (PR), sec_bhavdata_full, ind_close_all, Market Activity, Historical Indices (Price + TRI)

### v0.2.0 (Planned)
🚧 All Capital Market reports (UDiFF, Security Master, CMVOLT, Short Selling, etc.)

### v0.3.0 (Planned)
🚧 Derivatives — F&O, Commodity, Currency

---

## NSE Official Links

| Resource | URL |
|----------|-----|
| NSE All Reports | [nseindia.com/all-reports](https://www.nseindia.com/all-reports) |
| NSE Derivatives Reports | [nseindia.com/all-reports-derivatives](https://www.nseindia.com/all-reports-derivatives) |
| NSE Archives | [nsearchives.nseindia.com](https://nsearchives.nseindia.com) |
| Nifty Indices Historical | [niftyindices.com/reports/historical-data](https://niftyindices.com/reports/historical-data) |
| NSE Market Holidays | [nseindia.com/resources/exchange-communication-holidays](https://www.nseindia.com/resources/exchange-communication-holidays) |
