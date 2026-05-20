---
layout: default
title: Data Sources
nav_order: 5
---

# Data Sources & NSE Links

This page documents the exact NSE websites and URL patterns used by `nse-data`.

---

## 1. Nifty Indices — Historical Data

**Website:** [niftyindices.com/reports/historical-data](https://niftyindices.com/reports/historical-data)

**Protection:** Cloudflare (requires `cloudscraper` for JS challenge bypass)

**API Endpoints:**

| Endpoint | Method | Data |
|----------|--------|------|
| `/Backpage.aspx/getHistoricaldatatabletoString` | POST | Price Index (OHLC) |
| `/Backpage.aspx/getTotalReturnIndexString` | POST | Total Return Index |

**Request payload:**
```json
{
  "cinfo": "{\"name\":\"NIFTY 50\",\"startDate\":\"01-Apr-2026\",\"endDate\":\"15-May-2026\",\"indexName\":\"NIFTY 50\"}"
}
```

**Response format:**
```json
{
  "d": "[{\"indexName\":\"NIFTY 50\",\"HistoricalDate\":\"01 Apr 2026\",\"OPEN\":\"23410.50\",\"HIGH\":\"23562.80\",\"LOW\":\"23385.15\",\"CLOSE\":\"23519.35\"}]"
}
```

---

## 2. NSE Archives — Daily Reports

**Website:** [nseindia.com/all-reports](https://www.nseindia.com/all-reports)

**File server:** [nsearchives.nseindia.com](https://nsearchives.nseindia.com)

**Protection:** Session cookies (requires visiting main page first)

### URL Patterns

| Report | URL Pattern | Format |
|--------|-------------|--------|
| PR Bhavcopy | `/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip` | ZIP → CSV |
| sec_bhavdata_full | `/products/content/sec_bhavdata_full_{ddmmyyyy}.csv` | CSV |
| Bhav Copy | `/content/historical/EQUITIES/{YYYY}/{MON}/cm{ddMONyyyy}bhav.csv.zip` | ZIP → CSV |
| ind_close_all | `/content/indices/ind_close_all_{ddmmyyyy}.csv` | CSV |
| Market Activity | `/archives/equities/market-activity/MA{ddmmyy}.csv` | CSV |

### Date Format Placeholders

| Placeholder | Format | Example |
|-------------|--------|---------|
| `{ddmmyy}` | DDMMYY | `170426` |
| `{ddmmyyyy}` | DDMMYYYY | `17042026` |
| `{ddMONyyyy}` | DDMONYYYY (uppercase) | `17APR2026` |
| `{MON}` | MON (uppercase) | `APR` |
| `{YYYY}` | YYYY | `2026` |

### Example URLs

```
# PR Bhavcopy for 17-Apr-2026
https://nsearchives.nseindia.com/archives/equities/bhavcopy/pr/PR170426.zip

# sec_bhavdata_full for 17-Apr-2026
https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_17042026.csv

# ind_close_all for 17-Apr-2026
https://nsearchives.nseindia.com/content/indices/ind_close_all_17042026.csv

# Market Activity for 17-Apr-2026
https://nsearchives.nseindia.com/archives/equities/market-activity/MA170426.csv
```

---

## 3. Official NSE Links

| Resource | URL |
|----------|-----|
| NSE India (main site) | [www.nseindia.com](https://www.nseindia.com) |
| NSE All Reports | [www.nseindia.com/all-reports](https://www.nseindia.com/all-reports) |
| NSE Archives | [nsearchives.nseindia.com](https://nsearchives.nseindia.com) |
| Nifty Indices | [niftyindices.com](https://niftyindices.com) |
| Nifty Historical Data | [niftyindices.com/reports/historical-data](https://niftyindices.com/reports/historical-data) |
| NSE Market Holidays | [www.nseindia.com/resources/exchange-communication-holidays](https://www.nseindia.com/resources/exchange-communication-holidays) |

---

## 4. Data Availability

- **Trading days only** — Data is not available on weekends (Sat/Sun) and NSE holidays
- **Historical depth** — Index data typically available from 1999 onwards
- **Report availability** — Daily reports are usually available by 6:00 PM IST on trading days
- **No official API** — NSE does not provide a documented public API; this library uses web scraping

---

## 5. Rate Limiting & Access

NSE websites may:
- Return **HTTP 403** if too many requests are made in quick succession
- **Block IPs** temporarily for aggressive scraping
- **Change URL patterns** without notice

Recommendations:
- Add delays between requests (the library adds 1-2 second delays during session warmup)
- Don't make more than 1 request per second
- Cache downloaded data locally
- Pin your `nse-data` version to avoid breakage from URL pattern changes
