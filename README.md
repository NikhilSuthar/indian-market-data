<!-- Topics: nse mcx nifty india bhavcopy stock-market commodity financial-data pandas aws-lambda -->
# indian-market-data

Monorepo for India financial market data packages — download NSE bhavcopy, Nifty indices, F&O, equity, debt, MCX commodity futures as pandas DataFrames. Works on AWS Lambda and Snowflake.

## Packages

| Package | PyPI | Description |
|---------|------|-------------|
| [nse-data](packages/nse-data/) | [![PyPI](https://badge.fury.io/py/nse-data.svg)](https://pypi.org/project/nse-data/) | NSE India — equities, F&O, debt, indices (91 datasets) |
| [mcx-data](packages/mcx-data/) | [![PyPI](https://badge.fury.io/py/mcx-data.svg)](https://pypi.org/project/mcx-data/) | MCX India — commodity futures (coming soon) |
| [indian-market-data](packages/indian-market-data/) | [![PyPI](https://badge.fury.io/py/indian-market-data.svg)](https://pypi.org/project/indian-market-data/) | Umbrella — installs both |

## Install

```bash
# Individual packages
pip install nse-data        # NSE only
pip install mcx-data        # MCX only (coming soon)

# Umbrella (both)
pip install indian-market-data
```

## Quick Start

```python
from indianmarketdata import nse, mcx

# NSE bhavcopy
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")

# Nifty indices
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# NSE TRI (niftyindices.com)
df = nse.get_tri("NIFTY 50", "01-May-2026", "22-May-2026")

# Download to S3
nse.download("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22",
             s3_bucket="my-bucket", s3_prefix="raw/nse/")
```

## Documentation

[NikhilSuthar.github.io/nse-data](https://NikhilSuthar.github.io/nse-data)

## Release Tags

| Tag | Triggers |
|-----|----------|
| `nse-v0.9.0` | Publish `nse-data` to PyPI |
| `mcx-v0.1.0` | Publish `mcx-data` to PyPI |
| `v0.9.0` | Publish `indian-market-data` umbrella to PyPI |
| `release/*` branch | Publish all three to TestPyPI |

## License

MIT
