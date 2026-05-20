# Sample Data

This folder contains sample output files showing what data `nse-data` downloads. These are representative examples with realistic column structures and data formats.

## Folder Structure

```
samples/
├── indices/
│   ├── NIFTY_50_price_01-Apr-2026_to_15-Apr-2026.csv   ← Historical OHLC
│   └── NIFTY_50_TRI_01-Apr-2026_to_15-Apr-2026.csv     ← Total Return Index
└── reports/
    ├── bhavcopy_2026-04-17.csv                          ← PR bhavcopy (all securities)
    ├── sec_bhavdata_full_2026-04-17.csv                 ← Full bhavcopy with delivery
    ├── ind_close_all_2026-04-17.csv                     ← All index closing values
    └── market_activity_2026-04-17.csv                   ← Market activity summary
```

## How These Files Are Generated

### Indices

```bash
# Price Index (OHLC)
nse-data indices --index "NIFTY 50" --from "01-Apr-2026" --to "15-Apr-2026"
# → saves: NIFTY_50_01-Apr-2026_to_15-Apr-2026.csv

# Total Return Index
nse-data indices --index "NIFTY 50" --type tri --from "01-Apr-2026" --to "15-Apr-2026"
# → saves: NIFTY_50_TRI_01-Apr-2026_to_15-Apr-2026.csv
```

### Reports

```bash
# Bhavcopy
nse-data reports --type bhavcopy --date 2026-04-17
# → saves: bhavcopy_2026-04-17.csv

# Security-wise bhavcopy with delivery data
nse-data reports --type sec_bhavdata --date 2026-04-17
# → saves: sec_bhavdata_2026-04-17.csv

# All index closing values
nse-data reports --type ind_close_all --date 2026-04-17
# → saves: ind_close_all_2026-04-17.csv

# Market activity
nse-data reports --type market_activity --date 2026-04-17
# → saves: market_activity_2026-04-17.csv
```

## Notes

- These are **sample files** with representative data for illustration purposes.
- Actual downloaded files will have hundreds/thousands of rows.
- Column names and formats match the real NSE data exactly.
- Dates shown are trading days only (no weekends/holidays).
