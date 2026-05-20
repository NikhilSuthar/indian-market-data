# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
