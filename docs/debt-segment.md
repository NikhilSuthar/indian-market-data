---
layout: default
title: Debt — Debt Segment
nav_order: 12
parent: NSE India
---

# Debt — Debt Segment (WDM)

**Category:** `debt` | **Sub-section:** `debt_segment`

---

## WDM Securities List
```python
df = nse.get("debt", "debt_segment", "wdmlist", "2026-05-22")
```

## Debt Daily Bundle ZIP
ZIP of all WDM daily files (trade report, adds, mats, settlements).
```python
df = nse.get("debt", "debt_segment", "dly_bundle", "2026-05-22")
```
**File:** `dly{DDMMYYYY}.zip`

## Debt Weekly Bundle ZIP
```python
df = nse.get("debt", "debt_segment", "wkly_bundle", "2026-05-22")
```

## Accrued Interest (Monthly)
```python
df = nse.get("debt", "debt_segment", "accrued_interest", "2026-05")
```
**File:** `ACCTINT_{MON}{YYYY}.csv`
