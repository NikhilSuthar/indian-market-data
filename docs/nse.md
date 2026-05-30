---
layout: default
title: NSE India
nav_order: 2
has_children: true
permalink: /nse
---

# NSE India

<img src="{{ '/assets/nse.jpg' | relative_url }}" alt="NSE India" width="160"/>

**nse-archives** — Download NSE India market data as pandas DataFrames.

```bash
pip install nse-archives
```

**86 datasets** confirmed working across equities, F&O, debt, indices, SLB, IRD, and EGR.

---

## Quick Start

```python
from nsedata import nse

df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")
df = nse.get("derivatives", "equity", "fo_bhav_udiff", "2026-05-22")

nse.list_datasets()
```

---

## Dataset Categories

| Category | Sub-section | Datasets |
|----------|-------------|---------|
| Capital Market | [Equities & SME]({{ site.baseurl }}/nse/capital-market) | 32 |
| Capital Market | [Indices]({{ site.baseurl }}/nse/capital-market-indices) | 2 |
| Capital Market | [SLB]({{ site.baseurl }}/nse/capital-market-slb) | 12 |
| Derivatives | [Equity F&O]({{ site.baseurl }}/nse/derivatives-equity) | 8 |
| Derivatives | [Commodity]({{ site.baseurl }}/nse/derivatives-commodity) | 3 |
| Derivatives | [Currency]({{ site.baseurl }}/nse/derivatives-currency) | 3 |
| Derivatives | [Interest Rate]({{ site.baseurl }}/nse/derivatives-ird) | 9 |
| Debt | [Corporate Segment]({{ site.baseurl }}/nse/debt-corporate) | 15 |
| Debt | [Debt Segment]({{ site.baseurl }}/nse/debt-segment) | 4 |
| Debt | [Tri-Party Repo]({{ site.baseurl }}/nse/debt-trm) | 1 |
| EGR | [EGR]({{ site.baseurl }}/nse/egr) | 1 |

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Confirmed working — DataFrame + Download |
| ⬇️ | Download only (DAT/LST/DOC format) |
| 🕐 | T-1 only — available previous trading day |
| ⚙️ | Extra param (auto-calculated by default) |
| ⏭ | Portal-only — download manually from NSE website |

---

## Source

Data served from [nsearchives.nseindia.com](https://nsearchives.nseindia.com) — direct file downloads, no Cloudflare, works from any IP including Lambda.
