# india-market-data

Monorepo for India financial market data packages.

## Packages

| Package | PyPI | Description |
|---------|------|-------------|
| [nse-data](packages/nse-data/) | [![PyPI](https://badge.fury.io/py/nse-data.svg)](https://pypi.org/project/nse-data/) | NSE India — equities, F&O, debt, indices (91 datasets) |
| [mcx-data](packages/mcx-data/) | [![PyPI](https://badge.fury.io/py/mcx-data.svg)](https://pypi.org/project/mcx-data/) | MCX India — commodity futures (coming soon) |
| [india-market-data](packages/india-market-data/) | [![PyPI](https://badge.fury.io/py/india-market-data.svg)](https://pypi.org/project/india-market-data/) | Umbrella — installs both |

## Install

```bash
# Individual packages
pip install nse-data        # NSE only
pip install mcx-data        # MCX only (coming soon)

# Umbrella (both)
pip install india-market-data
```

## Quick Start

```python
from indiamarketdata import nse, mcx

# NSE data
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# NSE TRI (niftyindices.com)
df = nse.get_tri("NIFTY 50", "01-May-2026", "22-May-2026")

# Download to S3
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")
```

## Documentation

[NikhilSuthar.github.io/india-market-data](https://NikhilSuthar.github.io/india-market-data)

## Release Tags

| Tag | Triggers |
|-----|----------|
| `nse-v0.9.0` | Publish `nse-data` to PyPI |
| `mcx-v0.1.0` | Publish `mcx-data` to PyPI |
| `v0.9.0` | Publish `india-market-data` umbrella to PyPI |
| `release/*` branch | Publish all three to TestPyPI |

## License

MIT
