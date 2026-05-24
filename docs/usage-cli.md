---
layout: default
title: CLI Reference
nav_order: 2
parent: NSE India
---

# CLI Reference

Both packages install CLI commands after `pip install`.

---

## nse-data CLI

```bash
nse-data --help
```

### `nse-data get` — Print dataset as DataFrame

```bash
nse-data get <category> <subcategory> <dataset> <date>
```

```bash
nse-data get capital_market equities_sme sec_bhavdata_full 2026-05-22
nse-data get capital_market indices ind_close_all 2026-05-22
nse-data get derivatives equity fo_secban 2026-05-22
nse-data get debt corporate cbm_trd 2026-05-21
```

### `nse-data download` — Save to disk

```bash
nse-data download <category> <subcategory> <dataset> <date> [--out DIR]
```

```bash
nse-data download capital_market equities_sme sec_bhavdata_full 2026-05-22
nse-data download capital_market equities_sme sec_bhavdata_full 2026-05-22 --out ./data
```

### `nse-data list` — List all datasets

```bash
nse-data list
nse-data list --category derivatives
nse-data list --category capital_market --subcategory equities_sme
```

---

## mcx-data CLI

```bash
mcx-data --help
```

### `mcx-data spot-recent` — Today's spot prices

```bash
mcx-data spot-recent
mcx-data spot-recent --commodity GOLD
mcx-data spot-recent --commodity SILVER --out ./data
```

### `mcx-data spot-archive` — Historical spot prices

```bash
mcx-data spot-archive --from 01/05/2026 --to 22/05/2026 --commodity GOLD
mcx-data spot-archive --from 2026-01-01 --to 2026-05-22 --commodity CRUDEOIL --out ./data
```

**Save to S3:**
```bash
mcx-data spot-archive \
  --from 01/05/2026 --to 22/05/2026 \
  --commodity GOLD \
  --s3-bucket my-bucket --s3-prefix raw/mcx/
```

### `mcx-data list` — List datasets

```bash
mcx-data list
```

### `mcx-data commodities` — List available commodities

```bash
mcx-data commodities
# ALUMINI, ALUMINIUM, CARDAMOM, COPPER, COTTON, COTTONOIL,
# CPO, CRUDEOIL, CRUDEOILM, ELECDMBL, GOLD, GOLDGUINEA,
# GOLDM, GOLDPETAL, GOLDTEN, KAPAS, LEAD, LEADMINI,
# MENTHAOIL, NATGASMINI, NATURALGAS, NICKEL, SILVER, SILVERM,
# SILVERMIC, STEELREBAR, ZINC, ZINCMINI
```
