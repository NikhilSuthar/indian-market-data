---
layout: default
title: CLI Reference
nav_order: 4
---

# Command Line Interface

After installing `nse-data`, the `nse-data` command is available in your terminal.

```bash
nse-data --help
```

## Commands

### `nse-data indices` — Download Historical Index Data

```bash
nse-data indices --index "NIFTY 50" --from "01-Apr-2026" --to "15-May-2026"
```

**Options:**

| Flag | Required | Description |
|------|----------|-------------|
| `--index` | Yes | Index name (e.g. `"NIFTY 50"`, `"NIFTY BANK"`) |
| `--type` | No | `price` (default) or `tri` |
| `--from` | Yes | Start date in `dd-Mon-yyyy` format |
| `--to` | Yes | End date in `dd-Mon-yyyy` format |
| `--out` | No | Output CSV path (auto-generated if omitted) |

**Examples:**

```bash
# Price Index OHLC
nse-data indices --index "NIFTY 50" --from "01-Apr-2026" --to "15-May-2026"
# → Saves: NIFTY_50_01-Apr-2026_to_15-May-2026.csv

# Total Return Index
nse-data indices --index "NIFTY BANK" --type tri --from "01-Jan-2026" --to "31-Mar-2026"
# → Saves: NIFTY_BANK_TRI_01-Jan-2026_to_31-Mar-2026.csv

# Custom output path
nse-data indices --index "Nifty IT" --from "01-Apr-2026" --to "15-Apr-2026" --out ./data/nifty_it.csv
```

---

### `nse-data reports` — Download Daily Reports

```bash
nse-data reports --type bhavcopy --date 2026-04-17
```

**Options:**

| Flag | Required | Description |
|------|----------|-------------|
| `--type` | Yes | Report type (see below) |
| `--date` | Yes | Date in `YYYY-MM-DD` format |
| `--out` | No | Output CSV path (auto-generated if omitted) |

**Report types:**

| Type | Description | Output filename |
|------|-------------|-----------------|
| `bhavcopy` | PR bhavcopy zip (all securities) | `bhavcopy_2026-04-17.csv` |
| `sec_bhavdata` | Full bhavcopy with delivery data | `sec_bhavdata_2026-04-17.csv` |
| `ind_close_all` | All index closing values | `ind_close_all_2026-04-17.csv` |
| `market_activity` | Market activity summary | `market_activity_2026-04-17.csv` |

**Examples:**

```bash
# Bhavcopy
nse-data reports --type bhavcopy --date 2026-04-17

# Security-wise data with delivery
nse-data reports --type sec_bhavdata --date 2026-04-17

# All index closing values
nse-data reports --type ind_close_all --date 2026-04-17

# Market activity
nse-data reports --type market_activity --date 2026-04-17

# Custom output path
nse-data reports --type sec_bhavdata --date 2026-04-17 --out ./data/bhav.csv
```

---

## Output

The CLI prints a preview of the data to stdout and saves the full dataset as CSV:

```
$ nse-data reports --type sec_bhavdata --date 2026-04-17
Downloaded: sec_bhavdata for 2026-04-17 (1842 rows)
 SYMBOL SERIES  OPEN_PRICE  HIGH_PRICE  LOW_PRICE  CLOSE_PRICE ...
RELIANCE     EQ     2490.00     2518.75    2478.30      2512.45 ...
     TCS     EQ     3850.00     3878.90    3835.60      3865.20 ...
    INFY     EQ     1565.00     1582.40    1558.20      1575.60 ...
...

Saved: sec_bhavdata_2026-04-17.csv
```
