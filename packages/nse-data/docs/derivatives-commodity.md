---
layout: default
title: Derivatives — Commodity
nav_order: 6
---

# Derivatives — Commodity

**Category:** `derivatives` | **Sub-section:** `commodity`

---

## Commodity Bhavcopy (UDiFF)
```python
df = nse.get("derivatives", "commodity", "co_bhav_udiff", "2026-05-22")
```
**File:** `BhavCopy_NSE_CO_0_0_0_{YYYYMMDD}_F_0000.csv.zip`

## Commodity Contract Master
```python
df = nse.get("derivatives", "commodity", "co_contract", "2026-05-22")
```
**File:** `NSE_COM_contract_{DDMMYYYY}.csv.gz`

## Pay-in Pay-out Report (Monthly)
```python
nse.download("derivatives", "commodity", "payinpayout", "2026-05", output_dir="./data")
```
**File:** `Payinpayout_{MON}{YYYY}.zip`
