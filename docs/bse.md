---
layout: default
title: BSE India
nav_order: 4
has_children: true
permalink: /bse
---

# BSE India

<img src="{{ '/assets/BSE_logo.png' | relative_url }}" alt="BSE India" width="160"/>

**bse-index-data** — Download BSE India index data as pandas DataFrames.

```bash
pip install bse-index-data
```

**55 registered indices** across Broad Market, Sectoral, Thematic, Strategy and Global categories.
Live data returns **120+ indices** in a single call.

---

## Quick Start

```python
from bsedata import bse

# Historical SENSEX OHLC
df = bse.get_index("SENSEX", "2026-01-01", "2026-05-22")

# Historical BSE500
df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")

# All 120+ indices for one date (single API call)
df = bse.get_all_indices("2026-05-22")

# Live SENSEX quote
df = bse.get_live_sensex()
```

---

## Index Categories

| Category | Count | Examples |
|----------|-------|---------|
| Broad Market | 17 | SENSEX, BSE500, BSEMIDCAP, BSESMALLCAP |
| Sectoral | 21 | BANKEX, BSEIT, BSEHC, BSEFMCG, BSEMETAL |
| Thematic | 8 | BSECPSE, BSEIPO, BHARAT22, BSEINFRA |
| Strategy | 6 | BSEMOMENTUM, BSEQUALITY, BSELOWVOL, BSE100ESG |
| Global | 3 | DOLLEX30, DOLLEX100, DOLLEX200 |

---

## Session / Bot Check

BSE India uses a bot check on `api.bseindia.com`. `bse-index-data` automatically uses `curl-cffi` for Chrome TLS impersonation to pass it. Lambda IPs are unblocked.

```bash
pip install bse-index-data    # includes curl-cffi automatically
```
