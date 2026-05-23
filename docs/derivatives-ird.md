---
layout: default
title: Derivatives — Interest Rate
nav_order: 8
---

# Derivatives — Interest Rate

**Category:** `derivatives` | **Sub-section:** `interest_rate`

NSE portal: [All Reports → Derivatives → Interest Rate Derivatives](https://www.nseindia.com/all-reports)

---

### ✅ IRF Bhavcopy ZIP — 2,390 rows

```python
df = nse.get("derivatives", "interest_rate", "irf_bhavcopy", "2026-05-22")
```
`IRF_Bhavcopy{DDMMYY}.zip` | 2,390 rows × 14 cols

---

### ✅ IRD Volatility (I_VOLT) — 11 rows

```python
df = nse.get("derivatives", "interest_rate", "i_volt", "2026-05-22")
```
`I_VOLT_{DDMMYYYY}.csv` | 11 rows × 4 cols

---

### 🕐 Currency Derivatives IRF Settlement Prices — T-1

```python
df = nse.get("derivatives", "interest_rate", "cd_sett_irf", "2026-05-21")
```
`CDSett_prce_IRF_{DDMMYYYY}.csv` | 53 rows × 5 cols

---

### ✅ Early Warning Position Limits (EWPL) — 27 rows

```python
df = nse.get("derivatives", "interest_rate", "ewpl", "2026-05-22")
```
`EWPL_{DDMMYYYY}.CSV` | 27 rows × 7 cols

---

### ✅ Combined FPI Long Positions / FII Long Positions

```python
df = nse.get("derivatives", "interest_rate", "fpi_long", "2026-05-22")
df = nse.get("derivatives", "interest_rate", "fii_long", "2026-05-22")
```
Note: These files use latin-1 encoding — handled automatically.

---

### ⬇️ Tenure-Symbol Map (LST) — Download only

```python
nse.download("derivatives", "interest_rate", "tenure_symbol_map", "2026-05-22", output_dir="./data")
```
`TENURE_SYMBOL_MAP_{DD-MON-YYYY}.lst` (uppercase month: `22-MAY-2026`)

---

### ⬇️ IRF Client OI Limit / IRF TM OI Limit (LST) — Download only

```python
nse.download("derivatives", "interest_rate", "irf_cli_oi", "2026-05-22", output_dir="./data")
nse.download("derivatives", "interest_rate", "irf_tm_oi",  "2026-05-22", output_dir="./data")
```
`i_oi_cli_limit_{DD-MON-YYYY}.lst` / `i_oi_tm_limit_{DD-MON-YYYY}.lst`
