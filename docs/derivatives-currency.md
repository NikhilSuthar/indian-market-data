---
layout: default
title: Derivatives — Currency
nav_order: 9
parent: NSE India
---

# Derivatives — Currency

**Category:** `derivatives` | **Sub-section:** `currency`

---

## Currency Bhavcopy (UDiFF)
```python
df = nse.get("derivatives", "currency", "cd_bhav_udiff", "2026-05-22")
```
**File:** `BhavCopy_NSE_CD_0_0_0_{YYYYMMDD}_F_0000.csv.zip`

## Currency Contract Master
```python
df = nse.get("derivatives", "currency", "cd_contract", "2026-05-22")
```
**File:** `NSE_CD_contract_{DDMMYYYY}.csv.gz`

## CD Position of Clients (Monthly Excel)
Tabular after skipping first row.

```python
df = nse.get("derivatives", "currency", "cd_pos_clients", "2026-05-22")
```
**File:** `cd_pos_of_clients.xls` (skip_rows=1 applied automatically)
