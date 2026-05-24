---
layout: default
title: Derivatives — Equity F&O
nav_order: 7
parent: NSE India
---

# Derivatives — Equity F&O

**Category:** `derivatives` | **Sub-section:** `equity`

NSE portal path: All Reports → Derivatives → Equity Derivatives

---

## F&O Bhavcopy (UDiFF format)
Modern ISIN-keyed F&O bhavcopy. Includes open interest, settlement price.

```python
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")
```
```bash
nse-data get derivatives equity fo_bhav_udiff 2026-05-22
```
**File:** `BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip`  
**~45,000 rows × 34 cols**

---

## F&O Contract Master
All active contracts: lot size, strike, expiry, instrument type.

```python
df = nse.get("derivatives", "equity", "fo_contract", "2026-05-22")
df[df["Symbol"] == "NIFTY"]  # Filter Nifty contracts
```
**File:** `NSE_FO_contract_{DDMMYYYY}.csv.gz`  
**~96,000 rows × 150 cols**

---

## F&O Security Ban List
Securities in F&O ban period (crossed 95% of MWPL).

```python
df = nse.get("derivatives", "equity", "fo_secban", "2026-05-22")
```
**File:** `fo_secban_{DDMMYYYY}.csv`

---

## F&O Volatility (FOVOLT)
Per-underlying annualized volatility for margin computation.

```python
df = nse.get("derivatives", "equity", "fovolt", "2026-05-22")
```
**File:** `FOVOLT_{DDMMYYYY}.csv`

---

## Monthly Position Limit Files

```python
df = nse.get("derivatives", "equity", "fopl",           "2026-05")  # F&O position limits
df = nse.get("derivatives", "equity", "mpl",            "2026-05")  # Member position limits
df = nse.get("derivatives", "equity", "tmopl",          "2026-05")  # TM open position limits
df = nse.get("derivatives", "equity", "fo_impact_cost", "2026-05")  # Impact cost
```
