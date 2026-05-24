# indian-market-data

Umbrella package for NSE and MCX India market data — download NSE bhavcopy, Nifty indices, F&O, MCX commodity futures as pandas DataFrames. AWS Lambda ready.

```bash
pip install indian-market-data
```

Installs both `nse-data` and `mcx-data`.

```python
from indianmarketdata import nse, mcx

# NSE data
df = nse.get("capital_market", "equities_sme", "sec_bhavdata_full", "2026-05-22")
df = nse.get("capital_market", "indices", "ind_close_all", "2026-05-22")

# MCX data (coming soon)
# df = mcx.get("commodity", "bhavcopy", "2026-05-22")
```

## Individual packages

| Package | Install | Description |
|---------|---------|-------------|
| [nse-data](https://pypi.org/project/nse-data/) | `pip install nse-data` | NSE India — equities, F&O, debt, indices |
| [mcx-data](https://pypi.org/project/mcx-data/) | `pip install mcx-data` | MCX India — commodity futures |

## Documentation

[NikhilSuthar.github.io/nse-data](https://NikhilSuthar.github.io/nse-data)

## License

MIT
