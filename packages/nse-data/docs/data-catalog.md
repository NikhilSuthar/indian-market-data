---
layout: default
title: Data Catalog
nav_order: 6
---

# NSE Data Catalog

Complete catalog of **79 downloadable datasets** from NSE, organized by market segment.

---

## Summary

| Category | Datasets | ✅ Implemented | 🔜 Planned |
|----------|----------|---------------|------------|
| Capital Market — Equities | 18 | 3 | 15 |
| Capital Market — Indices | 7 | 1 | 6 |
| Capital Market — Risk & Margins | 7 | 0 | 7 |
| Capital Market — SME | 2 | 0 | 2 |
| Capital Market — SLB | 6 | 0 | 6 |
| Derivatives — Equity F&O | 24 | 0 | 24 |
| Derivatives — Commodity | 7 | 0 | 7 |
| Derivatives — Currency | 6 | 0 | 6 |
| Derivatives — Interest Rate (IRD) | 2 | 0 | 2 |
| Debt — Tri-Party Repo | 1 | 0 | 1 |
| **Total** | **80** | **4** | **76** |

---

## Usage Pattern

**CLI:**
```bash
nse-data download --type <type_key> --date YYYY-MM-DD
```

**Python:**
```python
from nsedata.reports import download_report
download_report("<type_key>", "2026-04-17")
```

---

## Capital Market — Equities (EOD Prices & Delivery)

### 1. `pr_bundle` — Bhavcopy (PR) Daily Zip Bundle ✅

| Field | Value |
|-------|-------|
| **File** | `PR{DDMMYY}.zip` |
| **Frequency** | Daily |
| **Format** | ZIP → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/historical/EQUITIES/{YYYY}/{MON}/PR{DDMMYY}.zip` |

```bash
nse-data download --type pr_bundle --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("pr_bundle", "2026-04-17")
```

---

### 2. `sec_bhavdata` — Securities Bhavcopy with Delivery (Full) ✅

| Field | Value |
|-------|-------|
| **File** | `sec_bhavdata_full_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{DDMMYYYY}.csv` |

```bash
nse-data download --type sec_bhavdata --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("sec_bhavdata", "2026-04-17")
```

---

### 3. `bhavcopy_udiff` — Capital Market Bhavcopy (UDiFF/ISIN format) 🔜

| Field | Value |
|-------|-------|
| **File** | `BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |
| **Frequency** | Daily |
| **Format** | ZIP → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |

```bash
nse-data download --type bhavcopy_udiff --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("bhavcopy_udiff", "2026-04-17")
```

---

### 4. `cm_security_master` — NSE CM Security Master 🔜

| Field | Value |
|-------|-------|
| **File** | `NSE_CM_security_{DDMMYYYY}.csv.gz` |
| **Frequency** | Daily |
| **Format** | GZ → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/cm/NSE_CM_security_{DDMMYYYY}.csv.gz` |

```bash
nse-data download --type cm_security_master --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cm_security_master", "2026-04-17")
```

---

### 5. `market_activity` — Market Activity Report (MA) ✅

| Field | Value |
|-------|-------|
| **File** | `MA{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/equities/mkt/MA{DDMMYY}.csv` |

```bash
nse-data download --type market_activity --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("market_activity", "2026-04-17")
```

---

### 6. `mto` — Multiple Trade Orders (Delivery Position) 🔜

| Field | Value |
|-------|-------|
| **File** | `MTO_{DDMMYYYY}.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/equities/mto/MTO_{DDMMYYYY}.DAT` |

```bash
nse-data download --type mto --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("mto", "2026-04-17")
```

---

### 7. `short_selling` — Short Selling Daily Report 🔜

| Field | Value |
|-------|-------|
| **File** | `shortselling_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/equities/shortSelling/shortselling_{DDMMYYYY}.csv` |

```bash
nse-data download --type short_selling --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("short_selling", "2026-04-17")
```

---

### 8. `cm_52wk_highlow` — Capital Market 52-Week High/Low 🔜

| Field | Value |
|-------|-------|
| **File** | `CM_52_wk_High_low_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/equities/CM_52_wk_High_low_{DDMMYYYY}.csv` |

```bash
nse-data download --type cm_52wk_highlow --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cm_52wk_highlow", "2026-04-17")
```

---

### 9. `block_deals` — Block Deals (Daily) 🔜

| Field | Value |
|-------|-------|
| **File** | `block.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type block_deals --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("block_deals", "2026-04-17")
```

---

### 10. `bulk_deals` — Bulk Deals (Daily) 🔜

| Field | Value |
|-------|-------|
| **File** | `bulk.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type bulk_deals --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("bulk_deals", "2026-04-17")
```

---

### 11. `bulk_deals_hist` — Bulk Deals (Historical date range) 🔜

| Field | Value |
|-------|-------|
| **File** | `Bulk-Deals-{DD-MM-YYYY}-to-{DD-MM-YYYY}.csv` |
| **Frequency** | On-demand (date range) |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type bulk_deals_hist --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("bulk_deals_hist", "2026-04-17")
```

---

### 12. `circuit_changes` — Circuit Filter Changes 🔜

| Field | Value |
|-------|-------|
| **File** | `circuit_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type circuit_changes --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("circuit_changes", "2026-04-17")
```

---

### 13. `eq_band_changes` — Equity Price Band Changes 🔜

| Field | Value |
|-------|-------|
| **File** | `eq_band_changes_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type eq_band_changes --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("eq_band_changes", "2026-04-17")
```

---

### 14. `sec_list` — CM Security List 🔜

| Field | Value |
|-------|-------|
| **File** | `sec_list_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type sec_list --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("sec_list", "2026-04-17")
```

---

### 15. `series_change` — Series Change Notifications 🔜

| Field | Value |
|-------|-------|
| **File** | `series_change.csv` |
| **Frequency** | As needed |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type series_change --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("series_change", "2026-04-17")
```

---

### 16. `auction_buy` — Auction Buy (AUB) 🔜

| Field | Value |
|-------|-------|
| **File** | `AUB_{SETTLNO}_{DDMMYYYY}.csv` |
| **Frequency** | Per settlement |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type auction_buy --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("auction_buy", "2026-04-17")
```

---

### 17. `margin_trading` — Margin Trading Report 🔜

| Field | Value |
|-------|-------|
| **File** | `mrg_trading_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type margin_trading --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("margin_trading", "2026-04-17")
```

---

### 18. `most_active` — Most Active Securities (Monthly) 🔜

| Field | Value |
|-------|-------|
| **File** | `Most Active Securities - {Month} {YYYY}.csv` |
| **Frequency** | Monthly |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type most_active --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("most_active", "2026-04-17")
```

---

## Capital Market — Indices

### 19. `ind_close_all` — All Indices Daily Close ✅

| Field | Value |
|-------|-------|
| **File** | `ind_close_all_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/indices/ind_close_all_{DDMMYYYY}.csv` |

```bash
nse-data download --type ind_close_all --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("ind_close_all", "2026-04-17")
```

---

### 20. `pe_pb_div` — Index P/E, P/B & Dividend Yield 🔜

| Field | Value |
|-------|-------|
| **File** | `PE_{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/equities/mkt/PE_{DDMMYY}.csv` |

```bash
nse-data download --type pe_pb_div --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("pe_pb_div", "2026-04-17")
```

---

### 21. `reg_ind` — Regional Indices Daily 🔜

| Field | Value |
|-------|-------|
| **File** | `REG_IND{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/equities/mkt/REG_IND{DDMMYY}.csv` |

```bash
nse-data download --type reg_ind --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("reg_ind", "2026-04-17")
```

---

### 22. `reg1_ind` — Regional Indices (Secondary) 🔜

| Field | Value |
|-------|-------|
| **File** | `REG1_IND{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/equities/mkt/REG1_IND{DDMMYY}.csv` |

```bash
nse-data download --type reg1_ind --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("reg1_ind", "2026-04-17")
```

---

### 23. `top10_nifty50` — Index Top Movers 🔜

| Field | Value |
|-------|-------|
| **File** | `top10nifty50_{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type top10_nifty50 --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("top10_nifty50", "2026-04-17")
```

---

### 24. `ind_impact_cost` — Index Impact Cost 🔜

| Field | Value |
|-------|-------|
| **File** | `ind_ic_nifty50_{YYYY}.csv` |
| **Frequency** | Annual |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type ind_impact_cost --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("ind_impact_cost", "2026-04-17")
```

---

### 25. `nifty_mcwb` — Nifty MCWB (Market Cap Weight Basis) 🔜

| Field | Value |
|-------|-------|
| **File** | `nifty50_mcwb.csv` |
| **Frequency** | Periodic |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type nifty_mcwb --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("nifty_mcwb", "2026-04-17")
```

---

## Capital Market — Risk & Margins

### 26. `cmvolt` — CM Security Volatility 🔜

| Field | Value |
|-------|-------|
| **File** | `CMVOLT_{DDMMYYYY}.CSV` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/volt/CMVOLT_{DDMMYYYY}.CSV` |

```bash
nse-data download --type cmvolt --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cmvolt", "2026-04-17")
```

---

### 27. `c_var1` — CM VaR Margin File (6 intraday snapshots) 🔜

| Field | Value |
|-------|-------|
| **File** | `C_VAR1_{DDMMYYYY}_{N}.DAT` |
| **Frequency** | Daily (6 snapshots) |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{DDMMYYYY}_{N}.DAT` |

```bash
nse-data download --type c_var1 --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("c_var1", "2026-04-17")
```

---

### 28. `c_catg` — CM Security Categorisation 🔜

| Field | Value |
|-------|-------|
| **File** | `C_CATG_{MON}{YYYY}.T01` |
| **Frequency** | Monthly |
| **Format** | T01 |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/cs/C_CATG_{MON}{YYYY}.T01` |

```bash
nse-data download --type c_catg --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("c_catg", "2026-04-17")
```

---

### 29. `csqr_m` — Client Segregation Quarterly Report 🔜

| Field | Value |
|-------|-------|
| **File** | `CSQR_M_{DDMMYYYY}.csv` |
| **Frequency** | Quarterly |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/csqr/CSQR_M_{DDMMYYYY}.csv` |

```bash
nse-data download --type csqr_m --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("csqr_m", "2026-04-17")
```

---

### 30. `fcm_intrm_bc` — FCM Interim Bhavcopy 🔜

| Field | Value |
|-------|-------|
| **File** | `FCM_INTRM_BC{DDMMYYYY}.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/fcm/FCM_INTRM_BC{DDMMYYYY}.DAT` |

```bash
nse-data download --type fcm_intrm_bc --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fcm_intrm_bc", "2026-04-17")
```

---

### 31. `c_stt` — STT Report 🔜

| Field | Value |
|-------|-------|
| **File** | `C_STT_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/stt/C_STT_{DDMMYYYY}.csv` |

```bash
nse-data download --type c_stt --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("c_stt", "2026-04-17")
```

---

### 32. `ael` — Approved Eligible List 🔜

| Field | Value |
|-------|-------|
| **File** | `ael_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/ael/ael_{DDMMYYYY}.csv` |

```bash
nse-data download --type ael --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("ael", "2026-04-17")
```

---

## Capital Market — SME

### 33. `sme_eod` — SME Platform EOD Market Data 🔜

| Field | Value |
|-------|-------|
| **File** | `sme{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/sme/sme{DDMMYYYY}.csv` |

```bash
nse-data download --type sme_eod --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("sme_eod", "2026-04-17")
```

---

### 34. `sme_bands` — SME Complete Price Bands 🔜

| Field | Value |
|-------|-------|
| **File** | `sme_bands_complete_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type sme_bands --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("sme_bands", "2026-04-17")
```

---

## Capital Market — Securities Lending & Borrowing

### 35. `slb_var` — SLB VaR Margin File 🔜

| Field | Value |
|-------|-------|
| **File** | `C_VAR1_SLB_{DDMMYYYY}_1.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/slb/C_VAR1_SLB_{DDMMYYYY}_1.DAT` |

```bash
nse-data download --type slb_var --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("slb_var", "2026-04-17")
```

---

### 36. `slbm_bc` — SLB Bhavcopy 🔜

| Field | Value |
|-------|-------|
| **File** | `SLBM_BC_{DDMMYYYY}.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type slbm_bc --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("slbm_bc", "2026-04-17")
```

---

### 37. `slb_elg_sec` — SLB Eligible Securities List 🔜

| Field | Value |
|-------|-------|
| **File** | `SLB_ELG_SEC_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type slb_elg_sec --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("slb_elg_sec", "2026-04-17")
```

---

### 38. `slb_openpos` — SLB Open Positions 🔜

| Field | Value |
|-------|-------|
| **File** | `slb_openpos_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type slb_openpos --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("slb_openpos", "2026-04-17")
```

---

### 39. `slb_transaction` — SLB Transaction Data (Monthly) 🔜

| Field | Value |
|-------|-------|
| **File** | `SLB_Transaction_Data_{Mon}{YYYY}.csv` |
| **Frequency** | Monthly |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type slb_transaction --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("slb_transaction", "2026-04-17")
```

---

### 40. `slb_foreclosure` — SLB Foreclosure Report 🔜

| Field | Value |
|-------|-------|
| **File** | `Forclosure_SLB_{YYYYMMDD}.CSV` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type slb_foreclosure --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("slb_foreclosure", "2026-04-17")
```

---

## Derivatives — Equity F&O

### 41. `fo_bhav` — F&O Daily Bhavcopy (zip) 🔜

| Field | Value |
|-------|-------|
| **File** | `fo{DDMMYYYY}bhav.csv.zip` |
| **Frequency** | Daily |
| **Format** | ZIP → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/historical/DERIVATIVES/{YYYY}/{MON}/fo{DDMMYYYY}bhav.csv.zip` |

```bash
nse-data download --type fo_bhav --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_bhav", "2026-04-17")
```

---

### 42. `fo_udiff` — F&O Bhavcopy (UDiFF) 🔜

| Field | Value |
|-------|-------|
| **File** | `BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |
| **Frequency** | Daily |
| **Format** | ZIP → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |

```bash
nse-data download --type fo_udiff --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_udiff", "2026-04-17")
```

---

### 43. `fo_contract` — F&O Contract Master 🔜

| Field | Value |
|-------|-------|
| **File** | `NSE_FO_contract_{DDMMYYYY}.csv.gz` |
| **Frequency** | Daily |
| **Format** | GZ → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/fo/NSE_FO_contract_{DDMMYYYY}.csv.gz` |

```bash
nse-data download --type fo_contract --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_contract", "2026-04-17")
```

---

### 44. `fo_spd_contract` — F&O Spread Contract Master 🔜

| Field | Value |
|-------|-------|
| **File** | `NSE_FO_spdcontract_{DDMMYYYY}.csv.gz` |
| **Frequency** | Daily |
| **Format** | GZ → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/fo/NSE_FO_spdcontract_{DDMMYYYY}.csv.gz` |

```bash
nse-data download --type fo_spd_contract --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_spd_contract", "2026-04-17")
```

---

### 45. `fno_bc` — F&O Bhavcopy (DAT) 🔜

| Field | Value |
|-------|-------|
| **File** | `FNO_BC{DDMMYYYY}.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/fao/FNO_BC{DDMMYYYY}.DAT` |

```bash
nse-data download --type fno_bc --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fno_bc", "2026-04-17")
```

---

### 46. `fo_sett_prce` — F&O Settlement Prices 🔜

| Field | Value |
|-------|-------|
| **File** | `FOSett_prce_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/fao/FOSett_prce_{DDMMYYYY}.csv` |

```bash
nse-data download --type fo_sett_prce --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_sett_prce", "2026-04-17")
```

---

### 47. `fovolt` — F&O Volatility 🔜

| Field | Value |
|-------|-------|
| **File** | `FOVOLT_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/volt/FOVOLT_{DDMMYYYY}.csv` |

```bash
nse-data download --type fovolt --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fovolt", "2026-04-17")
```

---

### 48. `fo_secban` — F&O Security Ban List 🔜

| Field | Value |
|-------|-------|
| **File** | `fo_secban_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/fo/sec_ban/fo_secban_{DDMMYYYY}.csv` |

```bash
nse-data download --type fo_secban --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_secban", "2026-04-17")
```

---

### 49. `combineoi` — F&O Combined OI 🔜

| Field | Value |
|-------|-------|
| **File** | `combineoi_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type combineoi --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("combineoi", "2026-04-17")
```

---

### 50. `combineoi_deleq` — Combined OI Derivatives-Equity Link 🔜

| Field | Value |
|-------|-------|
| **File** | `combineoi_deleq_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type combineoi_deleq --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("combineoi_deleq", "2026-04-17")
```

---

### 51. `fo_participant_oi` — F&O Participant OI 🔜

| Field | Value |
|-------|-------|
| **File** | `fao_participant_oi_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type fo_participant_oi --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_participant_oi", "2026-04-17")
```

---

### 52. `fo_participant_vol` — F&O Participant Volume 🔜

| Field | Value |
|-------|-------|
| **File** | `fao_participant_vol_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type fo_participant_vol --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fo_participant_vol", "2026-04-17")
```

---

### 53. `contract_delta` — F&O Contract Deltas 🔜

| Field | Value |
|-------|-------|
| **File** | `Contract_Delta_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type contract_delta --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("contract_delta", "2026-04-17")
```

---

### 54. `futidx` — Futures on Index 🔜

| Field | Value |
|-------|-------|
| **File** | `futidx{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type futidx --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("futidx", "2026-04-17")
```

---

### 55. `futstk` — Futures on Stocks 🔜

| Field | Value |
|-------|-------|
| **File** | `futstk{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type futstk --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("futstk", "2026-04-17")
```

---

### 56. `optidx` — Options on Index 🔜

| Field | Value |
|-------|-------|
| **File** | `optidx{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type optidx --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("optidx", "2026-04-17")
```

---

### 57. `optstk` — Options on Stocks 🔜

| Field | Value |
|-------|-------|
| **File** | `optstk{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type optstk --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("optstk", "2026-04-17")
```

---

### 58. `ncloi` — NCL Open Interest 🔜

| Field | Value |
|-------|-------|
| **File** | `ncloi_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type ncloi --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("ncloi", "2026-04-17")
```

---

### 59. `fpi_long` — Combined FPI Long Positions 🔜

| Field | Value |
|-------|-------|
| **File** | `Combined_FPI_long_psn_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type fpi_long --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fpi_long", "2026-04-17")
```

---

### 60. `fii_longpos` — FII Long Positions 🔜

| Field | Value |
|-------|-------|
| **File** | `fii_longpos_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type fii_longpos --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fii_longpos", "2026-04-17")
```

---

### 61. `ewpl` — Early Warning Position Limits 🔜

| Field | Value |
|-------|-------|
| **File** | `EWPL_{DDMMYYYY}.CSV` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type ewpl --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("ewpl", "2026-04-17")
```

---

### 62. `fopl` — F&O Position Limits (Monthly) 🔜

| Field | Value |
|-------|-------|
| **File** | `fopl_{mon}{yyyy}.csv` |
| **Frequency** | Monthly |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type fopl --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("fopl", "2026-04-17")
```

---

### 63. `mpl` — Member Position Limit (Monthly) 🔜

| Field | Value |
|-------|-------|
| **File** | `mpl_{mon}{yyyy}.csv` |
| **Frequency** | Monthly |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type mpl --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("mpl", "2026-04-17")
```

---

### 64. `tmopl` — TM Open Position Limit (Monthly) 🔜

| Field | Value |
|-------|-------|
| **File** | `tmopl_{mon}{yyyy}.csv` |
| **Frequency** | Monthly |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type tmopl --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("tmopl", "2026-04-17")
```

---

## Derivatives — Commodity

### 65. `co_bc` — Commodity Bhavcopy (DAT) 🔜

| Field | Value |
|-------|-------|
| **File** | `CO_BC{DDMMYYYY}.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/com/CO_BC{DDMMYYYY}.DAT` |

```bash
nse-data download --type co_bc --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_bc", "2026-04-17")
```

---

### 66. `co_udiff` — Commodity Bhavcopy (UDiFF) 🔜

| Field | Value |
|-------|-------|
| **File** | `BhavCopy_NSE_CO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |
| **Frequency** | Daily |
| **Format** | ZIP → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/com/BhavCopy_NSE_CO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |

```bash
nse-data download --type co_udiff --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_udiff", "2026-04-17")
```

---

### 67. `co_contract` — Commodity Derivatives Contract Master 🔜

| Field | Value |
|-------|-------|
| **File** | `NSE_COM_contract_{DDMMYYYY}.csv.gz` |
| **Frequency** | Daily |
| **Format** | GZ → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/com/NSE_COM_contract_{DDMMYYYY}.csv.gz` |

```bash
nse-data download --type co_contract --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_contract", "2026-04-17")
```

---

### 68. `co_volt` — Commodity Volatility 🔜

| Field | Value |
|-------|-------|
| **File** | `CO_VOLT_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/volt/CO_VOLT_{DDMMYYYY}.csv` |

```bash
nse-data download --type co_volt --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_volt", "2026-04-17")
```

---

### 69. `co_sett_prce` — Commodity Settlement Prices 🔜

| Field | Value |
|-------|-------|
| **File** | `CO_sett_prce_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type co_sett_prce --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_sett_prce", "2026-04-17")
```

---

### 70. `co_nse_fo` — Commodity F&O Combined 🔜

| Field | Value |
|-------|-------|
| **File** | `CO_NSE_FO{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type co_nse_fo --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_nse_fo", "2026-04-17")
```

---

### 71. `co_nse_op` — Commodity Options 🔜

| Field | Value |
|-------|-------|
| **File** | `CO_NSE_OP{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type co_nse_op --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("co_nse_op", "2026-04-17")
```

---

## Derivatives — Currency

### 72. `cd_bc` — Currency Derivatives Bhavcopy (DAT) 🔜

| Field | Value |
|-------|-------|
| **File** | `CD_BC{DDMMYYYY}.DAT` |
| **Frequency** | Daily |
| **Format** | DAT |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/cd/CD_BC{DDMMYYYY}.DAT` |

```bash
nse-data download --type cd_bc --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cd_bc", "2026-04-17")
```

---

### 73. `cd_udiff` — Currency Derivatives Bhavcopy (UDiFF) 🔜

| Field | Value |
|-------|-------|
| **File** | `BhavCopy_NSE_CD_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |
| **Frequency** | Daily |
| **Format** | ZIP → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/cd/BhavCopy_NSE_CD_0_0_0_{YYYYMMDD}_F_0000.csv.zip` |

```bash
nse-data download --type cd_udiff --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cd_udiff", "2026-04-17")
```

---

### 74. `cd_contract` — Currency Derivatives Contract Master 🔜

| Field | Value |
|-------|-------|
| **File** | `NSE_CD_contract_{DDMMYYYY}.csv.gz` |
| **Frequency** | Daily |
| **Format** | GZ → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/cd/NSE_CD_contract_{DDMMYYYY}.csv.gz` |

```bash
nse-data download --type cd_contract --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cd_contract", "2026-04-17")
```

---

### 75. `cd_spd_contract` — CD Spread Contract Master 🔜

| Field | Value |
|-------|-------|
| **File** | `NSE_CD_spdcontract_{DDMMYYYY}.csv.gz` |
| **Frequency** | Daily |
| **Format** | GZ → CSV |
| **Source URL** | `https://nsearchives.nseindia.com/content/cd/NSE_CD_spdcontract_{DDMMYYYY}.csv.gz` |

```bash
nse-data download --type cd_spd_contract --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cd_spd_contract", "2026-04-17")
```

---

### 76. `cd_sett_prce` — Currency Derivatives Settlement Prices 🔜

| Field | Value |
|-------|-------|
| **File** | `CDSett_prce_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/cd/CDSett_prce_{DDMMYYYY}.csv` |

```bash
nse-data download --type cd_sett_prce --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("cd_sett_prce", "2026-04-17")
```

---

### 77. `x_volt` — Currency Volatility 🔜

| Field | Value |
|-------|-------|
| **File** | `X_VOLT_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/nsccl/volt/X_VOLT_{DDMMYYYY}.csv` |

```bash
nse-data download --type x_volt --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("x_volt", "2026-04-17")
```

---

## Derivatives — Interest Rate (IRD)

### 78. `i_volt` — IRD Volatility 🔜

| Field | Value |
|-------|-------|
| **File** | `I_VOLT_{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type i_volt --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("i_volt", "2026-04-17")
```

---

### 79. `irf_nse` — IRF Daily File 🔜

| Field | Value |
|-------|-------|
| **File** | `IRF_NSE{DDMMYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://www.nseindia.com/all-reports` (portal) |

```bash
nse-data download --type irf_nse --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("irf_nse", "2026-04-17")
```

---

## Debt — Tri-Party Repo

### 80. `trm_bc` — Tri-Party Repo Bhavcopy 🔜

| Field | Value |
|-------|-------|
| **File** | `TRM_BC{DDMMYYYY}.csv` |
| **Frequency** | Daily |
| **Format** | CSV |
| **Source URL** | `https://nsearchives.nseindia.com/archives/trep/TRM_BC{DDMMYYYY}.csv` |

```bash
nse-data download --type trm_bc --date 2026-04-17
```
```python
from nsedata.reports import download_report
download_report("trm_bc", "2026-04-17")
```

---

## Quick Reference Table

| # | Key | Name | Status |
|---|-----|------|--------|
| 1 | `pr_bundle` | Bhavcopy (PR) Daily Zip Bundle | ✅ |
| 2 | `sec_bhavdata` | Securities Bhavcopy with Delivery | ✅ |
| 3 | `bhavcopy_udiff` | CM Bhavcopy (UDiFF/ISIN) | 🔜 |
| 4 | `cm_security_master` | NSE CM Security Master | 🔜 |
| 5 | `market_activity` | Market Activity Report | ✅ |
| 6 | `mto` | Multiple Trade Orders | 🔜 |
| 7 | `short_selling` | Short Selling Daily Report | 🔜 |
| 8 | `cm_52wk_highlow` | 52-Week High/Low | 🔜 |
| 9 | `block_deals` | Block Deals (Daily) | 🔜 |
| 10 | `bulk_deals` | Bulk Deals (Daily) | 🔜 |
| 11 | `bulk_deals_hist` | Bulk Deals (Historical) | 🔜 |
| 12 | `circuit_changes` | Circuit Filter Changes | 🔜 |
| 13 | `eq_band_changes` | Equity Price Band Changes | 🔜 |
| 14 | `sec_list` | CM Security List | 🔜 |
| 15 | `series_change` | Series Change Notifications | 🔜 |
| 16 | `auction_buy` | Auction Buy (AUB) | 🔜 |
| 17 | `margin_trading` | Margin Trading Report | 🔜 |
| 18 | `most_active` | Most Active Securities | 🔜 |
| 19 | `ind_close_all` | All Indices Daily Close | ✅ |
| 20 | `pe_pb_div` | Index P/E, P/B & Div Yield | 🔜 |
| 21 | `reg_ind` | Regional Indices Daily | 🔜 |
| 22 | `reg1_ind` | Regional Indices (Secondary) | 🔜 |
| 23 | `top10_nifty50` | Index Top Movers | 🔜 |
| 24 | `ind_impact_cost` | Index Impact Cost | 🔜 |
| 25 | `nifty_mcwb` | Nifty MCWB | 🔜 |
| 26 | `cmvolt` | CM Security Volatility | 🔜 |
| 27 | `c_var1` | CM VaR Margin File | 🔜 |
| 28 | `c_catg` | CM Security Categorisation | 🔜 |
| 29 | `csqr_m` | Client Segregation Quarterly | 🔜 |
| 30 | `fcm_intrm_bc` | FCM Interim Bhavcopy | 🔜 |
| 31 | `c_stt` | STT Report | 🔜 |
| 32 | `ael` | Approved Eligible List | 🔜 |
| 33 | `sme_eod` | SME Platform EOD | 🔜 |
| 34 | `sme_bands` | SME Complete Price Bands | 🔜 |
| 35 | `slb_var` | SLB VaR Margin File | 🔜 |
| 36 | `slbm_bc` | SLB Bhavcopy | 🔜 |
| 37 | `slb_elg_sec` | SLB Eligible Securities | 🔜 |
| 38 | `slb_openpos` | SLB Open Positions | 🔜 |
| 39 | `slb_transaction` | SLB Transaction Data | 🔜 |
| 40 | `slb_foreclosure` | SLB Foreclosure Report | 🔜 |
| 41 | `fo_bhav` | F&O Daily Bhavcopy | 🔜 |
| 42 | `fo_udiff` | F&O Bhavcopy (UDiFF) | 🔜 |
| 43 | `fo_contract` | F&O Contract Master | 🔜 |
| 44 | `fo_spd_contract` | F&O Spread Contract Master | 🔜 |
| 45 | `fno_bc` | F&O Bhavcopy (DAT) | 🔜 |
| 46 | `fo_sett_prce` | F&O Settlement Prices | 🔜 |
| 47 | `fovolt` | F&O Volatility | 🔜 |
| 48 | `fo_secban` | F&O Security Ban List | 🔜 |
| 49 | `combineoi` | F&O Combined OI | 🔜 |
| 50 | `combineoi_deleq` | Combined OI Deriv-Equity Link | 🔜 |
| 51 | `fo_participant_oi` | F&O Participant OI | 🔜 |
| 52 | `fo_participant_vol` | F&O Participant Volume | 🔜 |
| 53 | `contract_delta` | F&O Contract Deltas | 🔜 |
| 54 | `futidx` | Futures on Index | 🔜 |
| 55 | `futstk` | Futures on Stocks | 🔜 |
| 56 | `optidx` | Options on Index | 🔜 |
| 57 | `optstk` | Options on Stocks | 🔜 |
| 58 | `ncloi` | NCL Open Interest | 🔜 |
| 59 | `fpi_long` | Combined FPI Long Positions | 🔜 |
| 60 | `fii_longpos` | FII Long Positions | 🔜 |
| 61 | `ewpl` | Early Warning Position Limits | 🔜 |
| 62 | `fopl` | F&O Position Limits | 🔜 |
| 63 | `mpl` | Member Position Limit | 🔜 |
| 64 | `tmopl` | TM Open Position Limit | 🔜 |
| 65 | `co_bc` | Commodity Bhavcopy (DAT) | 🔜 |
| 66 | `co_udiff` | Commodity Bhavcopy (UDiFF) | 🔜 |
| 67 | `co_contract` | Commodity Contract Master | 🔜 |
| 68 | `co_volt` | Commodity Volatility | 🔜 |
| 69 | `co_sett_prce` | Commodity Settlement Prices | 🔜 |
| 70 | `co_nse_fo` | Commodity F&O Combined | 🔜 |
| 71 | `co_nse_op` | Commodity Options | 🔜 |
| 72 | `cd_bc` | Currency Derivatives Bhavcopy | 🔜 |
| 73 | `cd_udiff` | Currency Bhavcopy (UDiFF) | 🔜 |
| 74 | `cd_contract` | Currency Contract Master | 🔜 |
| 75 | `cd_spd_contract` | CD Spread Contract Master | 🔜 |
| 76 | `cd_sett_prce` | Currency Settlement Prices | 🔜 |
| 77 | `x_volt` | Currency Volatility | 🔜 |
| 78 | `i_volt` | IRD Volatility | 🔜 |
| 79 | `irf_nse` | IRF Daily File | 🔜 |
| 80 | `trm_bc` | Tri-Party Repo Bhavcopy | 🔜 |

---

## Date Format Reference

| Placeholder | Format | Example (17-Apr-2026) |
|-------------|--------|----------------------|
| `{DDMMYY}` | 6-digit date | `170426` |
| `{DDMMYYYY}` | 8-digit date | `17042026` |
| `{YYYYMMDD}` | ISO-style date | `20260417` |
| `{YYYY}` | 4-digit year | `2026` |
| `{MON}` | 3-letter month (uppercase) | `APR` |
| `{Mon}` | 3-letter month (title case) | `Apr` |
| `{mon}` | 3-letter month (lowercase) | `apr` |
| `{N}` | Snapshot number (1-6) | `1` |

---

## Notes

- **Trading days only** — Data is not available on weekends and NSE holidays.
- **Availability** — Daily reports are typically available by 6:00 PM IST.
- **Portal datasets** — Some datasets require session-based access via the NSE portal and cannot be downloaded via direct URL.
- **Rate limiting** — NSE may block IPs for aggressive scraping. Use delays between requests.
