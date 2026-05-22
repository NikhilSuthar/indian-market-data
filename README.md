# nse-data

[![PyPI version](https://badge.fury.io/py/nse-data.svg)](https://pypi.org/project/nse-data/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library to download market data from NSE India as **pandas DataFrames** or raw files to **local disk / S3**.

Works reliably from **AWS Lambda**, **Snowflake**, and any cloud/serverless environment.

## Installation

```bash
pip install nse-data

# With S3 support (adds boto3)
pip install nse-data[s3]
```

## Quick Start

```python
from nsedata import reports

# Get any report as a DataFrame (26 report types supported)
df = reports.get("sec_bhavdata_full", "2026-05-19")
df = reports.get("ind_close_all", "2026-05-19")
df = reports.get("cmvolt", "2026-05-19")
df = reports.get("security_master", "2026-05-19")
df = reports.get("fo_secban", "2026-05-19")

# Download raw file to local disk
path = reports.download_report("security_master", "2026-05-19", output_dir="./data")

# Download raw file to S3 (uses IAM role — no credentials needed in Lambda)
s3_uri = reports.download_report("sec_bhavdata_full", "2026-05-19",
                                  s3_bucket="my-nse-bucket", s3_prefix="raw/cm/")
# → "s3://my-nse-bucket/raw/cm/sec_bhavdata_full_19052026.csv"
```

## Command Line

```bash
# Parse report → print preview + save CSV
nse-data reports --type bhavcopy --date 2026-05-19
nse-data reports --type sec_bhavdata --date 2026-05-19
nse-data reports --type ind_close_all --date 2026-05-19

# Download raw file to disk
nse-data download --type cmvolt --date 2026-05-19 --out ./data
nse-data download --type security_master --date 2026-05-19 --out ./data
nse-data download --type index_dashboard_pdf --date 2026-03-01 --out ./pdfs
```

---

## Complete Report Type Reference

Date format for all: **`YYYY-MM-DD`** (e.g. `"2026-05-19"`)

### Capital Market — Prices

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `pr` | `PR{DDMMYY}.zip` → `pr{DDMMYYYY}.csv` | ZIP (13 files) | ✅ Extracts main price CSV | Daily bhavcopy — OHLC for all securities + indices |
| `sec_bhavdata_full` | `sec_bhavdata_full_{DDMMYYYY}.csv` | CSV | ✅ | **Recommended** — Full bhavcopy with delivery qty/% |
| `bhav_udiff` | `BhavCopy_NSE_CM_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | ✅ | UDiFF format (ISIN-keyed, modern schema) |
| `sme` | `sme{DDMMYYYY}.csv` | CSV | ✅ | SME platform EOD market data |

### Capital Market — Indices

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `ind_close_all` | `ind_close_all_{DDMMYYYY}.csv` | CSV | ✅ | **Recommended** — All 147+ indices OHLC + P/E + volume |
| `pe` | `PE_{DDMMYY}.csv` | CSV | ✅ | Per-security P/E, P/B, Dividend Yield |
| `reg_ind` | `REG_IND{DDMMYY}.csv` | CSV | ✅ | Regional/sectoral indices daily values |

### Capital Market — Activity & Deals

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `market_activity` | `MA{DDMMYY}.csv` | CSV | ✅ | Market turnover, advances/declines, breadth |
| `short_selling` | `shortselling_{DDMMYYYY}.csv` | CSV | ✅ | Per-security short-sold quantity |

### Capital Market — Reference & Master Data

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `security_master` | `NSE_CM_security_{DDMMYYYY}.csv.gz` | GZIP→CSV | ✅ | **Master list** — ISIN, face value, series, lot size, issued capital |
| `cm_52wk` | `CM_52_wk_High_low_{DDMMYYYY}.csv` | CSV | ✅ | Securities at new 52-week high/low |

### Capital Market — Risk & Margin

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `cmvolt` | `CMVOLT_{DDMMYYYY}.CSV` | CSV | ✅ | Per-security annualized + daily volatility |
| `mto` | `MTO_{DDMMYYYY}.DAT` | DAT (fixed-width) | ⚠️ Best-effort | Delivery qty vs traded qty breakdown |

### Derivatives — Equity F&O

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `fo_secban` | `fo_secban_{DDMMYYYY}.csv` | CSV | ✅ | Securities in F&O ban (crossed 95% MWPL) |
| `fovolt` | `FOVOLT_{DDMMYYYY}.csv` | CSV | ✅ | F&O underlying volatility |
| `fo_sett` | `FOSett_prce_{DDMMYYYY}.csv` | CSV | ✅ | F&O daily settlement prices |
| `fo_bhav_udiff` | `BhavCopy_NSE_FO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | ✅ | F&O bhavcopy (UDiFF format) |
| `fo_contract` | `NSE_FO_contract_{DDMMYYYY}.csv.gz` | GZIP→CSV | ✅ | F&O contract master (all active contracts) |

### Derivatives — Commodity

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `co_volt` | `CO_VOLT_{DDMMYYYY}.csv` | CSV | ✅ | Commodity underlying volatility |
| `co_bhav_udiff` | `BhavCopy_NSE_CO_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | ✅ | Commodity bhavcopy (UDiFF format) |
| `co_contract` | `NSE_COM_contract_{DDMMYYYY}.csv.gz` | GZIP→CSV | ✅ | Commodity contract master |

### Derivatives — Currency

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `x_volt` | `X_VOLT_{DDMMYYYY}.csv` | CSV | ✅ | Currency underlying volatility |
| `cd_sett` | `CDSett_prce_{DDMMYYYY}.csv` | CSV | ✅ | Currency derivatives settlement prices |
| `cd_bhav_udiff` | `BhavCopy_NSE_CD_0_0_0_{YYYYMMDD}_F_0000.csv.zip` | ZIP→CSV | ✅ | Currency bhavcopy (UDiFF format) |
| `cd_contract` | `NSE_CD_contract_{DDMMYYYY}.csv.gz` | GZIP→CSV | ✅ | Currency contract master |

### Debt

| Input Param | NSE File | Source Format | `get()` → DataFrame | Description |
|-------------|----------|---------------|---------------------|-------------|
| `trm_bc` | `TRM_BC{DDMMYYYY}.csv` | CSV | ✅ | Tri-Party Repo bhavcopy |

### PDF Reports (download only — not parseable as DataFrame)

| Input Param | NSE File | Description |
|-------------|----------|-------------|
| `index_dashboard_pdf` | `Index_Dashboard_{MON}{YYYY}.pdf` | Monthly equity index dashboard |
| `fi_index_dashboard_pdf` | `Index_Dashboard_FixedIncome_{MON}{YYYY}.pdf` | Monthly fixed-income index dashboard |
| `passive_fund_pdf` | `NiftyPassiveFundReport-{mon}{YYYY}-B2B-HR.pdf` | Monthly passive fund (ETF/index fund) report |
| `riskometer_pdf` | `NSE_Indices_Riskometer_{YYYY}-{mm}.pdf` | Monthly SEBI riskometer categorization |

```python
# PDF reports — use download_report() (not get())
path = reports.download_report("index_dashboard_pdf", "2026-03-01", "./pdfs")
s3_uri = reports.download_report("passive_fund_pdf", "2026-03-01",
                                  s3_bucket="my-bucket", s3_prefix="nse/pdfs/")
```

---

## S3 Integration

Upload directly to S3 using IAM role-based access (no API keys needed in Lambda):

```python
from nsedata import reports

# Single file to S3
s3_uri = reports.download_report(
    "sec_bhavdata_full", "2026-05-19",
    s3_bucket="my-nse-data-bucket",
    s3_prefix="raw/capital_market/"
)
# → "s3://my-nse-data-bucket/raw/capital_market/sec_bhavdata_full_19052026.csv"

# Multiple reports in a loop
report_types = ["sec_bhavdata_full", "ind_close_all", "cmvolt", "fo_secban"]
for rtype in report_types:
    uri = reports.download_report(rtype, "2026-05-19",
                                  s3_bucket="my-bucket",
                                  s3_prefix=f"nse/{rtype}/")
    print(f"Uploaded: {uri}")
```

**IAM Policy required:**
```json
{
    "Effect": "Allow",
    "Action": ["s3:PutObject"],
    "Resource": "arn:aws:s3:::my-nse-data-bucket/nse/*"
}
```

Install with S3 support: `pip install nse-data[s3]`

---

## AWS Lambda Example

```python
from nsedata import reports

def handler(event, context):
    date = event["date"]
    bucket = event.get("bucket", "my-nse-bucket")

    # Download multiple reports to S3
    uploaded = []
    for rtype in ["sec_bhavdata_full", "ind_close_all", "cmvolt"]:
        try:
            uri = reports.download_report(rtype, date,
                                          s3_bucket=bucket,
                                          s3_prefix=f"raw/{rtype}/")
            uploaded.append(uri)
        except RuntimeError as e:
            print(f"Skipped {rtype}: {e}")

    return {"uploaded": uploaded, "date": date}
```

---

## Recommendations

| Use Case | Recommended Report Type |
|----------|------------------------|
| Daily stock prices + delivery | `sec_bhavdata_full` |
| All index values (NIFTY 50, Bank, IT, etc.) | `ind_close_all` |
| Security master / ISIN lookup | `security_master` |
| Modern ISIN-keyed bhavcopy | `bhav_udiff` |
| F&O ban list monitoring | `fo_secban` |
| Volatility data for risk models | `cmvolt`, `fovolt`, `co_volt`, `x_volt` |
| F&O contract details | `fo_contract` |
| Short selling activity | `short_selling` |

---

## Important Notes

- All data from `nsearchives.nseindia.com` — **no Cloudflare**, works from any IP/cloud
- Data available only on **trading days** (weekends/[NSE holidays](https://www.nseindia.com/resources/exchange-communication-holidays) return HTTP errors)
- NSE may rate-limit aggressive requests — add 1-2s delays for bulk downloads
- `.DAT` files (like `mto`) use fixed-width format — `get()` does best-effort parsing; use `download_report()` for raw file if parsing fails
- PDF reports cannot be parsed as DataFrame — use `download_report()` only
- S3 upload uses `boto3` with IAM role (no credentials stored) — install with `pip install nse-data[s3]`

## Dependencies

| Package | Required | Purpose |
|---------|----------|---------|
| [requests](https://docs.python-requests.org/) | Yes | HTTP client |
| [pandas](https://pandas.pydata.org/) | Yes | DataFrame output |
| [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/) | Optional (`[s3]`) | S3 uploads |

## Contributing

```bash
git clone https://github.com/NikhilSuthar/nse-data.git
cd nse-data
pip install -e ".[dev]"
pytest
ruff check src/
```

## License

MIT — see [LICENSE](LICENSE) for details.
