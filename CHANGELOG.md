# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2026-07-05

### Fixed
- `mrg_trading` now returns proper scripwise detail (~2170 securities) instead of garbage data
- Added `mrg_trading_summary` dataset key for the 4-row daily summary section
- `_extract_section` now treats comma-only lines as section separators (handles ZIP-based multi-section CSVs)
- `zip_csv` format now supports `section` extraction after ZIP decompression
- Added `rename_columns` config to `DatasetConfig` — applied to clean `mrg_trading` column names:
  - `Qty Fin by all the members(No.of Shares)` → `Qty_Financed_Shares`
  - `Amt Fin by all the members(Rs. In Lakhs)` → `Amt_Financed_Lakhs`

## [1.2.0] - 2026-07-02

### Added
- 11 new dataset keys for Bhavcopy (PR) Daily ZIP Bundle sub-files:
  - `bhavcopy_pd` — Price Data with Symbol & Series
  - `bhavcopy_bc` — Book Closure / Corporate Actions
  - `bhavcopy_bh` — Price Band Hits (circuit breakers)
  - `bhavcopy_hl` — 52-Week New High/Low
  - `bhavcopy_gl` — Gainers & Losers
  - `bhavcopy_tt` — Top 25 Traded Securities
  - `bhavcopy_etf` — ETF End-of-Day Data
  - `bhavcopy_sme` — SME Platform EOD (from PR ZIP)
  - `bhavcopy_mcap` — Market Capitalisation
  - `bhavcopy_an` — Company Announcements
  - `bhavcopy_bm` — Board Meetings

### Changed
- Fetcher ZIP extraction now supports `.txt` files in addition to `.csv` inside ZIP archives

## [0.1.0] - 2026-05-19

### Added
- Initial release
- `indices.get_historical()` — fetch historical Price Index (OHLC) data from niftyindices.com
- `indices.get_tri()` — fetch Total Return Index data from niftyindices.com
- `reports.get_bhavcopy()` — download daily PR bhavcopy zip
- `reports.get_sec_bhavdata()` — download sec_bhavdata_full CSV
- `reports.get_ind_close_all()` — download index closing values
- `reports.get_market_activity()` — download market activity report
- `reports.download_report()` — download raw report file to disk
- CLI interface: `nse-data indices ...` and `nse-data reports ...`
- Cloudflare bypass via `cloudscraper` for niftyindices.com
- Cookie warming for nseindia.com session management
