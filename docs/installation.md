---
layout: default
title: Installation
nav_order: 2
---

# Installation

## From PyPI (recommended)

```bash
pip install nse-data
```

## From GitHub (latest development version)

```bash
pip install git+https://github.com/NikhilSuthar/nse-data.git
```

## From Source (for development)

```bash
git clone https://github.com/NikhilSuthar/nse-data.git
cd nse-data
pip install -e ".[dev]"
```

## Requirements

- Python 3.9 or higher
- Internet access to NSE websites

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [requests](https://docs.python-requests.org/) | ≥ 2.31.0 | HTTP client for nseindia.com |
| [pandas](https://pandas.pydata.org/) | ≥ 2.0.0 | DataFrame output and data manipulation |
| [cloudscraper](https://github.com/VeNoMouS/cloudscraper) | ≥ 1.2.71 | Cloudflare bypass for niftyindices.com |

## Verify Installation

```python
import nsedata
print(nsedata.__version__)
# 0.1.0
```

```bash
nse-data --help
```
