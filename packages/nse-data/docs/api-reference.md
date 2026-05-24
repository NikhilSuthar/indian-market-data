---
layout: default
title: API Reference
nav_order: 14
---

# API Reference

## `nse.get()`

```python
nse.get(category, subcategory, dataset, date, **kwargs) → pd.DataFrame
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | str | `capital_market`, `derivatives`, `debt`, `egr` |
| `subcategory` | str | See table below |
| `dataset` | str | Dataset key — see `nse.list_datasets()` |
| `date` | str | `"YYYY-MM-DD"` (daily) or `"YYYY-MM"` (monthly) |
| `snapshot` | int | 1–6 for `cvar1` (VaR margin snapshots) |

**Raises:**
- `ValueError` — unknown dataset or download-only format
- `RuntimeError` — HTTP error (non-trading day, NSE unavailable)

---

## `nse.download()`

```python
nse.download(category, subcategory, dataset, date,
             output_dir=".", s3_bucket=None, s3_prefix="",
             **kwargs) → str
```

Returns local file path or `"s3://bucket/key"`.

Works for **all** dataset types including download-only (DAT, LST, PDF).

**S3 example (Lambda with IAM role):**
```python
s3_uri = nse.download(
    "capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
    s3_bucket="my-nse-bucket",
    s3_prefix="raw/equities/",
)
# → "s3://my-nse-bucket/raw/equities/sec_bhavdata_full_22052026.csv"
```

---

## `nse.list_datasets()`

```python
nse.list_datasets(category=None, subcategory=None) → pd.DataFrame
```

Returns DataFrame with columns: `category, subcategory, dataset, name, frequency, df_supported, format, description`

---

## `nse.get_config_info()`

```python
nse.get_config_info(category, subcategory, dataset) → dict
```

Returns full configuration: URL pattern, file format, columns, encoding, skip_rows, etc.

---

## Subcategory Reference

| Category | Subcategory | Description |
|----------|-------------|-------------|
| `capital_market` | `equities_sme` | Equities & SME |
| `capital_market` | `indices` | Indices |
| `capital_market` | `mutual_fund` | Mutual Fund |
| `capital_market` | `slb` | Securities Lending & Borrowing |
| `derivatives` | `equity` | Equity F&O |
| `derivatives` | `commodity` | Commodity Derivatives |
| `derivatives` | `currency` | Currency Derivatives |
| `derivatives` | `interest_rate` | Interest Rate Derivatives |
| `debt` | `corporate` | Corporate Segment |
| `debt` | `debt_segment` | Debt Segment (WDM) |
| `debt` | `tri_party_repo` | Tri-Party Repo |
| `egr` | `egr` | Electronic Gold Receipt |

---

## CLI Reference

```bash
# Get dataset as DataFrame (prints + saves CSV)
nse-data get <category> <subcategory> <dataset> <date> [--out FILE]

# Download raw file
nse-data dl  <category> <subcategory> <dataset> <date> [--out DIR] [--s3-bucket BUCKET] [--s3-prefix PREFIX]

# List datasets
nse-data list [--category CATEGORY] [--subcategory SUBCATEGORY] [--df-only]

# Show dataset info
nse-data info <category> <subcategory> <dataset>
```
