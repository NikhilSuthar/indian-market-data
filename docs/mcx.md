---
layout: default
title: MCX India
nav_order: 4
has_children: true
permalink: /mcx
---

# MCX India

<img src="{{ '/assets/mcx.png' | relative_url }}" alt="MCX India" width="160"/>

**mcx-data** — Download MCX India commodity spot market data as pandas DataFrames.

```bash
pip install mcx-data
```

**28 commodities** — GOLD, SILVER, CRUDEOIL, NATURALGAS, COPPER, ALUMINIUM and more.

---

## Quick Start

```python
from mcxdata import mcx

# Today's spot prices
df = mcx.get_spot_recent()
df = mcx.get_spot_recent(commodity="GOLD")

# Historical archive
df = mcx.get_spot_archive("2026-05-01", "2026-05-22", commodity="GOLD")
```

---

## Available Commodities

| Metals | Energy | Agri / Others |
|--------|--------|---------------|
| GOLD, GOLDM, GOLDTEN | CRUDEOIL, CRUDEOILM | CARDAMOM, COTTON |
| GOLDGUINEA, GOLDPETAL | NATURALGAS, NATGASMINI | COTTONOIL, KAPAS |
| SILVER, SILVERM, SILVERMIC | ELECDMBL | MENTHAOIL, CPO |
| COPPER, ALUMINI, ALUMINIUM | | |
| LEAD, LEADMINI, NICKEL | | |
| ZINC, ZINCMINI, STEELREBAR | | |

---

## Note on Akamai WAF

MCX India uses Akamai WAF. `mcx-data` automatically uses `curl-cffi` for Chrome TLS impersonation to bypass it. Lambda IPs are generally unblocked.
