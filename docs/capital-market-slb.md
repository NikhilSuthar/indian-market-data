---
layout: default
title: Capital Market — SLB
nav_order: 6
parent: NSE India
---

# Capital Market — Securities Lending & Borrowing

**Category:** `capital_market` | **Sub-section:** `slb`

NSE portal: [All Reports → Capital Market → SLB](https://www.nseindia.com/all-reports)

---

## Daily Datasets

### ✅ SLB Eligible Securities List — 29,000+ rows

```python
df = nse.get("capital_market", "slb", "slb_elg_sec", "2026-05-22")
```
`SLB_ELG_SEC_{DDMMYYYY}.csv` | 29,093 rows × 7 cols

---

### ✅ SLB Open Positions — 559 rows

```python
df = nse.get("capital_market", "slb", "slb_openpos", "2026-05-22")
```
`slb_openpos_{DDMMYYYY}.csv` | 559 rows × 4 cols

---

### ✅ SLB Foreclosure Report — 11 rows

```python
df = nse.get("capital_market", "slb", "slb_foreclosure", "2026-05-22")
```
`Forclosure_SLB_{YYYYMMDD}.CSV` | 11 rows × 13 cols

---

### ⬇️ SLB Bhavcopy (SLBM_BC) — Download only (DAT)

```python
nse.download("capital_market", "slb", "slb_bc", "2026-05-22", output_dir="./data")
```
`SLBM_BC_{DDMMYYYY}.DAT`

---

### ⬇️ SLB VaR Margin File — Download only (DAT)

```python
nse.download("capital_market", "slb", "slb_var", "2026-05-22", output_dir="./data")
```
`C_VAR1_SLB_{DDMMYYYY}_1.DAT`

---

## Monthly Datasets

### ✅ SLB Monthly Position Limits (4 files)

```python
df = nse.get("capital_market", "slb", "slb_cli",  "2026-05")  # Client limits — 1,048 rows
df = nse.get("capital_market", "slb", "slb_fopl", "2026-05")  # Fund-of-pool — 1,048 rows
df = nse.get("capital_market", "slb", "slb_mpl",  "2026-05")  # Member limits — 1,048 rows
df = nse.get("capital_market", "slb", "slb_ppl",  "2026-05")  # Pool limits   — 1,048 rows
```
Files: `slbs_{cli/fopl/mpl/ppl}_{Mon}{YYYY}.csv`

---

### ✅ SLB Transaction Data (Monthly) — 326 rows
Note: Current month may be delayed; previous month is always available.

```python
df = nse.get("capital_market", "slb", "slb_transaction_data", "2026-04")  # previous month
```
`SLB_Transaction_Data_{Mon}{YYYY}.csv` | 326 rows × 6 cols

---

## Portal-Only (⏭ no direct archive URL)

Download manually from [nseindia.com/all-reports](https://www.nseindia.com/all-reports):

| Dataset | Description |
|---------|-------------|
| `slb_positions` | SLB Positions (Weekly/Monthly XLS) |
| `slb_transactions` | SLB Transactions (Weekly/Monthly XLS) |
