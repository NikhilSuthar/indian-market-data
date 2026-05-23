---
layout: default
title: Derivatives — Interest Rate
nav_order: 8
---

# Derivatives — Interest Rate

**Category:** `derivatives` | **Sub-section:** `interest_rate`

---

## IRF Bhavcopy ZIP
```python
df = nse.get("derivatives", "interest_rate", "irf_bhavcopy", "2026-05-22")
```
**File:** `IRF_Bhavcopy{DDMMYY}.zip`

## IRD Volatility
```python
df = nse.get("derivatives", "interest_rate", "i_volt", "2026-05-22")
```
**File:** `I_VOLT_{DDMMYYYY}.csv`

## Currency Derivatives IRF Settlement Prices
```python
df = nse.get("derivatives", "interest_rate", "cd_sett_irf", "2026-05-22")
```
**File:** `CDSett_prce_IRF_{DDMMYYYY}.csv`

## Early Warning Position Limits (EWPL)
```python
df = nse.get("derivatives", "interest_rate", "ewpl", "2026-05-22")
```

## FPI Long Positions / FII Long Positions
Files use latin-1 encoding — handled automatically.

```python
df = nse.get("derivatives", "interest_rate", "fpi_long", "2026-05-22")
df = nse.get("derivatives", "interest_rate", "fii_long", "2026-05-22")
```

## Download-Only Datasets

```python
# Tenure-Symbol Map (LST)
nse.download("derivatives", "interest_rate", "tenure_symbol_map", "2026-05-22", output_dir="./data")

# IRF Client OI Limit (LST)
nse.download("derivatives", "interest_rate", "irf_cli_oi", "2026-05-22", output_dir="./data")

# IRF TM OI Limit (LST)
nse.download("derivatives", "interest_rate", "irf_tm_oi", "2026-05-22", output_dir="./data")
```
