---
layout: default
title: API Reference
nav_order: 3
parent: NSE India
---

# API Reference

---

## nse-data

### `nse.get()`

```python
from nsedata import nse

nse.get(category, subcategory, dataset, date, **kwargs) → pd.DataFrame
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | str | `capital_market`, `derivatives`, `debt`, `egr` |
| `subcategory` | str | e.g. `equities_sme`, `equity`, `corporate` |
| `dataset` | str | Dataset key — see `nse.list_datasets()` |
| `date` | str | `"YYYY-MM-DD"` (daily) or `"YYYY-MM"` (monthly) |
| `snapshot` | int | 1–6 for `cvar1` VaR margin snapshots only |
| `settno` | str | Override settlement number for `auction_buy`/`csqr` (auto-calculated by default) |

**Raises:**
- `ValueError` — unknown dataset or download-only format
- `RuntimeError` — HTTP error (non-trading day, NSE unavailable)

---

### `nse.download()`

```python
nse.download(category, subcategory, dataset, date,
             output_dir=".", s3_bucket=None, s3_prefix="",
             **kwargs) → str
```

Returns local file path or `"s3://bucket/key"`. Works for all datasets including download-only (DAT, LST, DOC).

---

### `nse.list_datasets()`

```python
nse.list_datasets(category=None) → pd.DataFrame
```

Columns: `category, subcategory, dataset, name, frequency, df_supported, format`

---

### `nse.get_historical_index()`

```python
nse.get_historical_index(index_name, start_date, end_date) → pd.DataFrame
```

Date format: `"DD-Mon-YYYY"` e.g. `"01-Jan-2026"`

Source: niftyindices.com

---

### `nse.get_tri()`

```python
nse.get_tri(index_name, start_date, end_date) → pd.DataFrame
```

Total Return Index. Same date format as `get_historical_index`.

---

### `nse.get_settlement_number()`

```python
nse.get_settlement_number(date) → str
```

Returns settlement number string e.g. `"2026094"` for `"2026-05-22"`.

---

## mcx-data

### `mcx.get_spot_recent()`

```python
from mcxdata import mcx

mcx.get_spot_recent(commodity="ALL", location="ALL") → pd.DataFrame
```

Returns today's spot prices. No date param needed.

---

### `mcx.get_spot_archive()`

```python
mcx.get_spot_archive(from_date, to_date,
                     commodity="ALL", location="ALL") → pd.DataFrame
```

Date formats accepted: `YYYY-MM-DD`, `DD/MM/YYYY`, `YYYYMMDD`

> Specify a commodity — `"ALL"` returns empty (MCX API limitation).

---

### `mcx.get()`

```python
mcx.get(category, subcategory, dataset, date=None,
        from_date=None, to_date=None,
        commodity="ALL", location="ALL") → pd.DataFrame
```

Generic API mirroring nse-data pattern.

---

### `mcx.download()`

```python
mcx.download(category, subcategory, dataset, date=None,
             from_date=None, to_date=None,
             commodity="ALL", output_dir=".",
             s3_bucket=None, s3_prefix="mcx-data/") → str
```

---

### `mcx.list_datasets()`

```python
mcx.list_datasets() → pd.DataFrame
```

---

### `mcx.list_commodities()`

```python
mcx.list_commodities() → list[str]
```

Returns 28 commodity names from live MCX data.

---

## Subcategory Reference — NSE

| Category | Subcategory | Description |
|----------|-------------|-------------|
| `capital_market` | `equities_sme` | Equities & SME (32 datasets) |
| `capital_market` | `indices` | Indices (2 datasets) |
| `capital_market` | `mutual_fund` | Mutual Fund (1 dataset) |
| `capital_market` | `slb` | Securities Lending & Borrowing (12 datasets) |
| `derivatives` | `equity` | Equity F&O (8 datasets) |
| `derivatives` | `commodity` | Commodity Derivatives (3 datasets) |
| `derivatives` | `currency` | Currency Derivatives (3 datasets) |
| `derivatives` | `interest_rate` | Interest Rate Derivatives (9 datasets) |
| `debt` | `corporate` | Corporate Segment (15 datasets) |
| `debt` | `debt_segment` | Debt Segment / WDM (4 datasets) |
| `debt` | `tri_party_repo` | Tri-Party Repo (1 dataset) |
| `egr` | `egr` | Electronic Gold Receipt (1 dataset) |

---

## Dataset Reference — MCX

| Category | Subcategory | Dataset | Description |
|----------|-------------|---------|-------------|
| `spot` | `market` | `spot_recent` | Today's spot prices — all 28 commodities |
| `spot` | `market` | `spot_archive` | Historical spot prices (requires specific commodity) |
