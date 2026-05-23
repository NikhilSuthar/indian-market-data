---
layout: default
title: Capital Market — SLB
nav_order: 4
---

# Capital Market — Securities Lending & Borrowing

**Category:** `capital_market` | **Sub-section:** `slb`

NSE portal path: All Reports → Capital Market → Securities Lending and Borrowing

---

## Daily Datasets

### SLB Eligible Securities List
Securities eligible for lending/borrowing with eligibility type flags.

```python
df = nse.get("capital_market", "slb", "slb_elg_sec", "2026-05-22")
```
**File:** `SLB_ELG_SEC_{DDMMYYYY}.csv`  
**Columns:** `Sr.No., Symbol, Series, Normal Eligibility, Recall Eligibility, Repay Eligibility, Market Type`

---

### SLB Open Positions
Outstanding positions at member/client level.

```python
df = nse.get("capital_market", "slb", "slb_openpos", "2026-05-22")
```
**File:** `slb_openpos_{DDMMYYYY}.csv`

---

### SLB Foreclosure Report
Foreclosure events with corporate action details.

```python
df = nse.get("capital_market", "slb", "slb_foreclosure", "2026-05-22")
```
**File:** `Forclosure_SLB_{YYYYMMDD}.CSV`

---

### SLB Bhavcopy (SLBM_BC) — Download Only
Daily SLB trade summary. Fixed-width DAT.

```python
nse.download("capital_market", "slb", "slb_bc", "2026-05-22", output_dir="./data")
```
**File:** `SLBM_BC_{DDMMYYYY}.DAT`

---

### SLB VaR Margin File — Download Only

```python
nse.download("capital_market", "slb", "slb_var", "2026-05-22", output_dir="./data")
```
**File:** `C_VAR1_SLB_{DDMMYYYY}_1.DAT`

---

## Weekly / Monthly Datasets

### SLB Positions / Transactions (Excel)
```python
df = nse.get("capital_market", "slb", "slb_positions",    "2026-05-22")
df = nse.get("capital_market", "slb", "slb_transactions",  "2026-05-22")
```
**Files:** `slbs_positions_{DDMMYYYY}.xls`, `slbs_transactions_{DDMMYYYY}.xls`

---

### Monthly Position Limits

```python
df = nse.get("capital_market", "slb", "slb_cli",  "2026-05")  # Client limits
df = nse.get("capital_market", "slb", "slb_fopl", "2026-05")  # Fund-of-pool limits
df = nse.get("capital_market", "slb", "slb_mpl",  "2026-05")  # Member limits
df = nse.get("capital_market", "slb", "slb_ppl",  "2026-05")  # Pool limits
df = nse.get("capital_market", "slb", "slb_transaction_data", "2026-05")  # Monthly transactions
```
