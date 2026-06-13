---
layout: default
title: Index Data
nav_order: 1
parent: BSE India
---

# BSE India — Index Data

**Package:** `bse-index-data` | **Install:** `pip install bse-index-data`

BSE India provides historical OHLC and live data for all its indices via a JSON API on `api.bseindia.com`.

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Confirmed working — DataFrame + Download |

---

## Datasets

### ✅ Historical Index OHLC

Historical open/high/low/close for any BSE index over a date range.

```python
from bsedata import bse

# SENSEX — May 2026
df = bse.get_index("SENSEX", "2026-05-01", "2026-05-22")

# BSE500 — full year
df = bse.get_index("BSE500", "2026-01-01", "2026-05-22")

# BANKEX — sectoral
df = bse.get_index("BANKEX", "2026-01-01", "2026-05-22")

# Also accepts YYYYMMDD format
df = bse.get_index("BSEMIDCAP", "20260101", "20260522")
```

**Columns:** `Index Name, Date, Open, High, Low, Close`

**Sample output (SENSEX, May 2026):**

| Index Name | Date | Open | High | Low | Close |
|-----------|------|------|------|-----|-------|
| SENSEX | 2026-05-04 | 77257.27 | 77910.75 | 76939.54 | 77269.40 |
| SENSEX | 2026-05-05 | 77103.72 | 77151.33 | 76515.03 | 77017.79 |
| SENSEX | 2026-05-06 | 77424.36 | 78022.78 | 76773.25 | 77958.52 |

Returns one row per trading day. Weekends and holidays are excluded automatically.

**API endpoint:** `GET https://api.bseindia.com/BseIndiaAPI/api/ProduceCSVForDate/w`
**Params:** `strIndex=SENSEX&dtFromDate=DD/MM/YYYY&dtToDate=DD/MM/YYYY&period=D`

---

### ✅ Historical Index — Full Columns (P/E, P/B, Volume, Turnover)

Historical data with all fundamental columns. Uses same key as `get_index()`.

> Slower than `get_index()` — makes one API call per calendar day.

```python
from bsedata import bse

# BSE200 — full columns
df = bse.get_index_full("BSE200", "2026-05-01", "2026-05-22")

# SENSEX — with fundamentals
df = bse.get_index_full("SENSEX", "2026-05-01", "2026-05-22")

# BANKEX
df = bse.get_index_full("BANKEX", "2026-05-01", "2026-05-22")
```

**Columns:** `Index Name, Date, Open, High, Low, Close, Change, Change %, Volume (Cr.), Turnover (Rs. Cr.), P/E, P/B, Div Yield, Prev Close`

**Sample output (BSE200, May 2026):**

| Index Name | Date | Open | Close | P/E | P/B | Div Yield | Volume (Cr.) |
|-----------|------|------|-------|-----|-----|-----------|-------------|
| BSE 200 | 2026-05-20 | 10922.23 | 11011.04 | 21.88 | 4.20 | 1.12 | 15.29 |
| BSE 200 | 2026-05-21 | 11081.79 | 11015.45 | 21.86 | 4.20 | 1.12 | 12.65 |
| BSE 200 | 2026-05-22 | 11041.19 | 11047.96 | 21.93 | 4.21 | 1.15 | 13.42 |

**API endpoint:** `GET https://api.bseindia.com/BseIndiaAPI/api/IndexArchDailyAll/w`

---

### ✅ Historical Index — Full Columns (P/E, P/B, Volume, Turnover)

Same index keys as `get_index()` but returns all fundamental columns.
Uses one API call per calendar day — slower for long date ranges.

```python
from bsedata import bse

# BSE200 — full columns for May 2026
df = bse.get_index_full("BSE200", "2026-05-01", "2026-05-22")

# SENSEX with P/E, P/B, Div Yield
df = bse.get_index_full("SENSEX", "2026-05-01", "2026-05-22")

# BANKEX sectoral
df = bse.get_index_full("BANKEX", "2026-05-01", "2026-05-22")
```

**Columns:** `Index Name, Date, Open, High, Low, Close, Change, Change %, Volume (Cr.), Turnover (Rs. Cr.), P/E, P/B, Div Yield, Prev Close`

**Sample output (BSE200, May 2026):**

| Index Name | Date | Open | Close | Change % | P/E | P/B | Div Yield | Volume (Cr.) |
|-----------|------|------|-------|---------|-----|-----|-----------|-------------|
| BSE 200 | 2026-05-20 | 10922.23 | 11011.04 | 0.31 | 21.88 | 4.20 | 1.12 | 15.29 |
| BSE 200 | 2026-05-21 | 11081.79 | 11015.45 | 0.04 | 21.86 | 4.20 | 1.12 | 12.65 |
| BSE 200 | 2026-05-22 | 11041.19 | 11047.96 | 0.30 | 21.93 | 4.21 | 1.15 | 13.42 |

> **Note:** `get_index()` and `get_index_full()` use the **same index key** (e.g. `"BSE200"`).
> `get_index()` is faster (single API call). `get_index_full()` is slower but returns P/E, P/B, Volume, Turnover.

**API endpoint:** `GET https://api.bseindia.com/BseIndiaAPI/api/IndexArchDailyAll/w`

---

### ✅ All Indices for One Date

Get all 120+ BSE indices' closing values for a single date in one API call.

```python
from bsedata import bse

df = bse.get_all_indices("2026-05-22")
```

**Columns:** `Index Name, Date, Open, High, Low, Close, Change, Change %` (+ additional BSE fields)

**Sample output:**

| Index Name | Date | Open | High | Low | Close | Change | Change % |
|-----------|------|------|------|-----|-------|--------|---------|
| BSE SENSEX | 2026-05-22 | 75260.39 | 75810.97 | 75230.75 | 75415.35 | 231.99 | 0.31 |
| BSE 100 | 2026-05-22 | 25126.35 | 25255.94 | 25099.07 | 25157.55 | 80.11 | 0.32 |
| BSE 500 | 2026-05-22 | 35427.79 | 35534.81 | 35350.16 | 35413.94 | 73.63 | 0.21 |
| BANKEX | 2026-05-22 | 62140.00 | 62580.00 | 62050.00 | 62310.00 | 180.00 | 0.29 |

Returns 120+ rows — one per index. Use `Index Name` column to filter.

**API endpoint:** `GET https://api.bseindia.com/BseIndiaAPI/api/IndexArchDailyAll/w`
**Params:** `fmdt=DD/MM/YYYY&todt=DD/MM/YYYY&index=All&period=D`

---

### ✅ Live SENSEX Quote

Real-time SENSEX quote — no date param, no session needed.

```python
from bsedata import bse

df = bse.get_live_sensex()
print(f"SENSEX: ₹{df['LTP'].iloc[0]:,.2f}")
```

**Columns:** `Index, LTP, Change, Change %, Open, High, Low, Prev Close, DateTime`

**Sample output:**

| Index | LTP | Change | Change % | Open | High | Low | Prev Close | DateTime |
|-------|-----|--------|---------|------|------|-----|-----------|---------|
| SenSexValue | 74775.74 | -1092.06 | -1.44 | 75988.51 | 76220.02 | 74589.11 | 75867.80 | 29 May 26 \| 16:00 |

**API endpoint:** `GET https://api.bseindia.com/RealTimeBseIndiaAPI/api/GetSensexData/w`

---

## All Supported Indices (55 registered)

### Broad Market (17)

| API Key | Name | Description |
|---------|------|-------------|
| `SENSEX` | SENSEX | Top 30 large-cap companies. India's flagship benchmark since 1986 |
| `SENSEX50` | SENSEX 50 | Top 50 companies by free-float market cap |
| `SENSEXNXT50` | SENSEX NEXT 50 | Next 50 after SENSEX 50 — mid-large cap |
| `BSE100` | BSE 100 | Top 100 companies — covers ~80% of BSE market cap |
| `BSE200` | BSE 200 | Top 200 companies |
| `BSE500` | BSE 500 | Top 500 companies — covers ~93% of BSE market cap |
| `BSEALLCAP` | BSE ALLCAP | All listed companies with adequate liquidity |
| `BSEMIDCAP` | BSE MIDCAP | Mid-cap companies — ranked 101–300 by market cap |
| `BSESMALLCAP` | BSE SMALLCAP | Small-cap companies — ranked 301+ |
| `BSE150MIDCAP` | BSE 150 MIDCAP | Top 150 mid-cap companies |
| `BSE250SMALLCAP` | BSE 250 SMALLCAP | Top 250 small-cap companies |
| `BSE400MIDSMALLCAP` | BSE 400 MID & SMALLCAP | Combined mid and small-cap — 400 companies |
| `BSE250LARGEMIDCAP` | BSE 250 LARGE & MIDCAP | Top 250 large and mid-cap |
| `BSE100LARGECAPTMC` | BSE 100 LARGECAP TMC | Top 100 large-cap by total market cap |
| `BSEMIDCAPSELECT` | BSE MIDCAP SELECT | Select mid-cap with strong fundamentals |
| `BSESMALLCAPSELECT` | BSE SMALLCAP SELECT | Select small-cap with strong fundamentals |
| `BSELARGECAP` | BSE LARGECAP | Large-cap — top 100 by full market cap |

### Sectoral (21)

| API Key | Name | Description |
|---------|------|-------------|
| `BANKEX` | BANKEX | Top banking sector companies |
| `BSEAUTO` | BSE AUTO | Automobile and auto-ancillary |
| `BSECG` | BSE CAPITAL GOODS | Capital goods and industrial machinery |
| `BSECD` | BSE CONSUMER DISCRETIONARY | Retail, media, leisure |
| `BSECDGS` | BSE CONSUMER DURABLES | Appliances, electronics |
| `BSEENERGY` | BSE ENERGY | Oil, gas, power generation |
| `BSEFMCG` | BSE FMCG | Fast-moving consumer goods |
| `BSEFINANCE` | BSE FINANCIAL SERVICES | Banks, NBFCs, insurance, AMCs |
| `BSEHC` | BSE HEALTHCARE | Pharma, hospitals, diagnostics |
| `BSEIT` | BSE IT | Software, IT services |
| `BSEINDUSTRIALS` | BSE INDUSTRIALS | Engineering, defence, aerospace |
| `BSEMETAL` | BSE METAL | Steel, aluminium, copper |
| `BSEOILGAS` | BSE OIL & GAS | Exploration, refining, distribution |
| `BSEPOWER` | BSE POWER | Generation, transmission, distribution |
| `BSEPRIVATEBANKS` | BSE PRIVATE BANKS | Private sector banks |
| `BSEPSU` | BSE PSU | Government-owned companies |
| `BSEREALTY` | BSE REALTY | Real estate developers, REITs |
| `BSESERVICES` | BSE SERVICES | Logistics, hospitality, media |
| `BSETECK` | BSE TECK | Technology, media and telecom |
| `BSETELECOM` | BSE TELECOMMUNICATION | Mobile, broadband, infrastructure |
| `BSEUTILS` | BSE UTILITIES | Power, water, gas distribution |

### Thematic (8)

| API Key | Name | Description |
|---------|------|-------------|
| `BSECPSE` | BSE CPSE | Central Public Sector Enterprises — disinvestment index |
| `BSEIPO` | BSE IPO | Recently listed IPO companies |
| `BSESMEIPO` | BSE SME IPO | SME IPO companies on BSE SME platform |
| `BSEGREENEX` | BSE GREENEX | Companies with strong environmental credentials |
| `BSECARBONEX` | BSE CARBONEX | Low carbon footprint companies |
| `BSEINFRA` | BSE INDIA INFRASTRUCTURE | Roads, ports, airports, utilities |
| `BSEMANUFACTURING` | BSE INDIA MANUFACTURING | Make in India theme |
| `BHARAT22` | BHARAT 22 | 22 government companies selected for disinvestment. ETF benchmark |

### Strategy / Factor (6)

| API Key | Name | Description |
|---------|------|-------------|
| `BSEMOMENTUM` | BSE MOMENTUM | High-momentum stocks |
| `BSEQUALITY` | BSE QUALITY | Strong ROE, low debt, stable earnings |
| `BSEVALUE` | BSE ENHANCED VALUE | Value stocks — discount to intrinsic value |
| `BSELOWVOL` | BSE LOW VOLATILITY | Defensive portfolio with lower drawdowns |
| `BSEDIVSTAB` | BSE DIVIDEND STABILITY | Consistent dividend payment history |
| `BSE100ESG` | BSE 100 ESG | Top 100 screened for ESG criteria |

### Global / Dollar (3)

| API Key | Name | Description |
|---------|------|-------------|
| `DOLLEX30` | DOLLEX-30 | SENSEX in USD terms |
| `DOLLEX100` | DOLLEX-100 | BSE 100 in USD terms |
| `DOLLEX200` | DOLLEX-200 | BSE 200 in USD terms |

---

## Download to Disk or S3

```python
from bsedata import bse

# Save to local file
path = bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                           output_dir="./bse_data")
# → ./bse_data/BSE_SENSEX_20260101_20260522.csv

# Save to S3 (Lambda with IAM role)
uri = bse.download_index("SENSEX", "2026-01-01", "2026-05-22",
                          s3_bucket="my-bucket", s3_prefix="raw/bse/")
# → s3://my-bucket/raw/bse/BSE_SENSEX_20260101_20260522.csv

# Download all indices for one date
path = bse.download_all_indices("2026-05-22", output_dir="./bse_data")
# → ./bse_data/BSE_all_indices_20260522.csv
```

---

## CLI

```bash
# Historical SENSEX
bse-index-data index --name SENSEX --from 2026-01-01 --to 2026-05-22

# Historical BSE500 — save to S3
bse-index-data index --name BSE500 --from 2026-01-01 --to 2026-05-22 \
  --s3-bucket my-bucket --s3-prefix raw/bse/

# All indices for one date
bse-index-data all-indices --date 2026-05-22

# Live SENSEX quote
bse-index-data live

# List all supported indices
bse-index-data list

# Filter by category
bse-index-data list --category Sectoral
bse-index-data list --category "Broad Market"
```

---

## Method Comparison

| Method | Speed | Columns | Use case |
|--------|-------|---------|---------|
| `get_index(key, from, to)` | Fast — single API call | OHLC only (6 cols) | Price charts, returns computation |
| `get_index_full(key, from, to)` | Slower — one call per day | Full 15 cols incl. P/E, P/B, Volume | Fundamental analysis, valuation |
| `get_all_indices(date)` | Fast — single call | Full columns for ALL indices | Daily snapshot of entire market |
| `get_live_sensex()` | Instant | Live quote | Real-time monitoring |

> Both `get_index()` and `get_index_full()` use the **same index key** — e.g. `"BSE200"`, `"SENSEX"`, `"BANKEX"`.

---

## List Indices

```python
from bsedata import bse

# All 55 registered indices
df = bse.list_indices()

# Filter by category
df = bse.list_indices(category="Sectoral")
df = bse.list_indices(category="Broad Market")
df = bse.list_indices(category="Strategy")

# Fetch live index names from BSE API (discovers new indices)
names = bse.get_index_names_from_api()
```

---

## Error Handling

```python
from bsedata import bse

try:
    df = bse.get_index("SENSEX", "2026-05-24", "2026-05-24")  # Sunday — no data
    if df.empty:
        print("No data — weekend or holiday")
except RuntimeError as e:
    print(f"Failed: {e}")

try:
    df = bse.get_index("INVALID", "2026-05-01", "2026-05-22")
except ValueError as e:
    print(f"Unknown index: {e}")
    # Use bse.list_indices() to see valid keys
```

Common errors:
- `ValueError` — unknown index key (use `bse.list_indices()`)
- `RuntimeError` — BSE API unavailable or session failed
- Empty DataFrame — weekend, holiday, or date before index inception
