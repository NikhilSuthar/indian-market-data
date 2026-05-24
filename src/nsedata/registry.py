"""
NSE Dataset Registry — single source of truth for all supported datasets.

Structure:
    REGISTRY[category][subcategory][dataset_key] = DatasetConfig

Usage:
    from nsedata.registry import REGISTRY, get_config, list_datasets
"""

from dataclasses import dataclass, field
from typing import Optional, Literal


@dataclass
class DatasetConfig:
    """Configuration for a single NSE dataset."""

    # Display info
    name: str               # Human-readable name as shown on NSE website
    description: str        # What this dataset contains

    # URL
    url_pattern: str        # URL pattern with {ddmmyy}, {ddmmyyyy}, {yyyymmdd}, {MON}, {YYYY} etc.
    base_url: str = "https://nsearchives.nseindia.com"

    # File info
    file_pattern: str = ""  # Filename pattern e.g. "sec_bhavdata_full_{ddmmyyyy}.csv"
    file_format: str = "csv"  # csv, dat, zip_csv, gz_csv, zip_xlsx, xls, xlsx, lst, t01, pdf, dat_fw

    # Date parameter type
    date_type: Literal["daily", "monthly", "static"] = "daily"
    # "daily"   → takes YYYY-MM-DD
    # "monthly" → takes YYYY-MM (e.g. "2026-05")
    # "static"  → no date param (file is always the same)

    # DataFrame support
    df_supported: bool = True       # Can be returned as DataFrame
    download_only: bool = False     # download_only=True means no DataFrame, just file download
    portal_only: bool = False       # portal_only=True — requires NSE portal session, no direct URL

    # Parser hints
    skip_rows: int = 0              # Rows to skip before header
    encoding: str = "utf-8"         # File encoding
    separator: Optional[str] = None # None = auto-detect
    zip_extract: Optional[str] = None  # For ZIP: which file to extract (regex pattern)

    # Metadata
    frequency: str = "Daily"
    columns: str = ""               # Key columns hint


# ─── Helper to build URL ──────────────────────────────────────────────────
NSE_ARCHIVES = "https://nsearchives.nseindia.com"


# ─── REGISTRY ─────────────────────────────────────────────────────────────
# Structure: REGISTRY[category][subcategory][dataset_key]

REGISTRY = {

    # ════════════════════════════════════════════════════════════
    # CAPITAL MARKET
    # ════════════════════════════════════════════════════════════
    "capital_market": {

        # ── Equities & SME ─────────────────────────────────────
        "equities_sme": {

            "bhavcopy_pr": DatasetConfig(
                name="Bhavcopy (PR) Daily ZIP Bundle",
                description="Daily price records ZIP containing 13 files: pr (OHLC), pd (OHLC+Symbol), "
                            "bc (corporate actions), bh (price band hits), hl (52-wk hi/lo), "
                            "gl (gainers/losers), tt (top 25), etf, sme, corpbond, mcap, bm, an.",
                url_pattern="/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip",
                file_pattern="PR{ddmmyy}.zip",
                file_format="zip_csv",
                zip_extract=r"^pr\d{8}\.csv$",  # extract pr file by default
                frequency="Daily",
                columns="MKT,SECURITY,PREV_CL_PR,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,NET_TRDVAL,NET_TRDQTY,TRADES",
            ),

            "sec_bhavdata_full": DatasetConfig(
                name="Securities Bhavcopy with Delivery (Full)",
                description="Full EOD bhavcopy with delivery qty/% for all cash-market securities. "
                            "One row per SYMBOL+SERIES. Most comprehensive daily price file.",
                url_pattern="/products/content/sec_bhavdata_full_{ddmmyyyy}.csv",
                file_pattern="sec_bhavdata_full_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="SYMBOL,SERIES,DATE1,PREV_CLOSE,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,AVG_PRICE,TTL_TRD_QNTY,TURNOVER_LACS,NO_OF_TRADES,DELIV_QTY,DELIV_PER",
            ),

            "bhav_udiff": DatasetConfig(
                name="CM Bhavcopy (UDiFF / ISIN format)",
                description="Modern ISIN-keyed bhavcopy in Unified Download Interface File Format. "
                            "Preferred for new integrations — includes ISIN, tick size, lot size.",
                url_pattern="/content/cm/BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_pattern="BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_format="zip_csv",
                frequency="Daily",
                columns="TradDt,BizDt,Sgmt,FinInstrmId,ISIN,TckrSymb,SctySrs,OpnPric,HghPric,LwPric,ClsPric,LastPric,TtlTradgVol,TtlTrfVal",
            ),

            "security_master": DatasetConfig(
                name="NSE CM Security Master",
                description="Master list of all securities: ISIN, face value, series, lot size, "
                            "issued capital, trading status. Reference for SYMBOL→ISIN lookup.",
                url_pattern="/content/cm/NSE_CM_security_{ddmmyyyy}.csv.gz",
                file_pattern="NSE_CM_security_{ddmmyyyy}.csv.gz",
                file_format="gz_csv",
                frequency="Daily",
                columns="FinInstrmId,TckrSymb,SctySrs,FinInstrmNm,ISIN,NewBrdLotQty,ParVal,IssdCptl",
            ),

            "market_activity": DatasetConfig(
                name="Market Activity Report",
                description="Daily market summary: turnover, advances/declines, breadth, circuit hits.",
                url_pattern="/archives/equities/mkt/MA{ddmmyy}.csv",
                file_pattern="MA{ddmmyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Market,Advances,Declines,Unchanged,Total,Traded,Turnover",
            ),

            "cmvolt": DatasetConfig(
                name="CM Security Volatility (CMVOLT)",
                description="Per-security annualized and daily volatility for VaR margin computation.",
                url_pattern="/archives/nsccl/volt/CMVOLT_{ddmmyyyy}.CSV",
                file_pattern="CMVOLT_{ddmmyyyy}.CSV",
                file_format="csv",
                frequency="Daily",
                columns="Date,Symbol,Underlying Close Price,Previous Day Close,Log Returns,Prev Volatility,Daily Volatility,Annualised Volatility",
            ),

            "short_selling": DatasetConfig(
                name="Short Selling Report",
                description="Per-security short-sold quantity disclosed by members at EOD.",
                url_pattern="/archives/equities/shortSelling/shortselling_{ddmmyyyy}.csv",
                file_pattern="shortselling_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Security Name,Symbol Name,Trade Date,Quantity",
            ),

            "mto": DatasetConfig(
                name="Multiple Trade Orders (MTO)",
                description="Security-level delivery qty vs total traded qty. Input for delivery % computation.",
                url_pattern="/archives/equities/mto/MTO_{ddmmyyyy}.DAT",
                file_pattern="MTO_{ddmmyyyy}.DAT",
                file_format="dat",
                frequency="Daily",
                columns="Security Wise Delivery Position - Compulsory Rolling Settlement",
            ),

            "52wk_high_low": DatasetConfig(
                name="52-Week High/Low",
                description="Securities hitting new 52-week high or low. Available via NSE portal API only — not on direct archive URL.",
                url_pattern="",
                base_url="",
                file_pattern="CM_52_wk_High_low_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=True,
                skip_rows=2,
                frequency="Daily",
                columns="Symbol,Name,High Date,52W High,Low Date,52W Low,Adj High,Adj Low",
            ),

            "block_deals": DatasetConfig(
                name="Block Deals",
                description="Disclosed block deals (single static file, updated intraday).",
                url_pattern="/content/equities/block.csv",
                file_pattern="block.csv",
                file_format="csv",
                date_type="static",
                frequency="Daily (static)",
                columns="Date,Symbol,Security Name,Client Name,Buy/Sell,Quantity Traded,Trade Price",
            ),

            "bulk_deals": DatasetConfig(
                name="Bulk Deals",
                description="Disclosed bulk deals (single static file, updated daily).",
                url_pattern="/content/equities/bulk.csv",
                file_pattern="bulk.csv",
                file_format="csv",
                date_type="static",
                frequency="Daily (static)",
                columns="Date,Symbol,Security Name,Client Name,Buy/Sell,Quantity Traded,Trade Price,Remarks",
            ),

            "pe": DatasetConfig(
                name="Index P/E, P/B & Dividend Yield",
                description="Daily P/E, P/B and dividend yield for each NSE index constituent.",
                url_pattern="/content/equities/peDetail/PE_{ddmmyy}.csv",
                file_pattern="PE_{ddmmyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Symbol,P/E,Adjusted P/E",
            ),

            "reg_ind": DatasetConfig(
                name="Regional Indices",
                description="Daily values of NSE regional / sectoral indices.",
                url_pattern="/content/cm/REG_IND{ddmmyy}.csv",
                file_pattern="REG_IND{ddmmyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="ScripCode,Symbol,Status,Series,GSM,ASM,ESM",
            ),

            "reg1_ind": DatasetConfig(
                name="Regional Indices (Secondary Cut)",
                description="Alternate regional indices snapshot with extended surveillance flags.",
                url_pattern="/content/cm/REG1_IND{ddmmyy}.csv",
                file_pattern="REG1_IND{ddmmyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="ScripCode,Symbol,Status,Series,GSM,ASM,ESM",
            ),

            "sme": DatasetConfig(
                name="SME Platform EOD Market Data",
                description="EOD OHLC, volumes and 52-wk hi/lo for all NSE SME-Emerge securities.",
                url_pattern="/archives/sme/bhavcopy/sme{ddmmyyyy}.csv",
                file_pattern="sme{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="MARKET,SERIES,SYMBOL,SECURITY,PREV_CL_PR,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,NET_TRDVAL,NET_TRDQTY,CORP_IND,HI_52_WK,LO_52_WK",
            ),

            "sme_bands": DatasetConfig(
                name="SME Complete Price Bands",
                description="Complete SME price-band list for all SME securities.",
                url_pattern="/sme/content/price_band/archieves/sme_bands_complete_{ddmmyyyy}.csv",
                file_pattern="sme_bands_complete_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Symbol,Series,Name,Band,Remarks",
            ),

            "eq_band_changes": DatasetConfig(
                name="Equity Price Band Changes",
                description="Securities with price-band reclassification effective that day.",
                url_pattern="/content/equities/eq_band_changes_{ddmmyyyy}.csv",
                file_pattern="eq_band_changes_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Sr No,Symbol,Series,Security Name,From,To",
            ),

            "sec_list": DatasetConfig(
                name="Security List",
                description="Current CM security list with band and remarks.",
                url_pattern="/content/equities/sec_list_{ddmmyyyy}.csv",
                file_pattern="sec_list_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Symbol,Series,Security Name,Band,Remarks",
            ),

            "series_change": DatasetConfig(
                name="Series Change Notifications",
                description="Securities with series reclassification (e.g. EQ → BE).",
                url_pattern="/content/equities/series_change.csv",
                file_pattern="series_change.csv",
                file_format="csv",
                date_type="static",
                frequency="Daily (static)",
                columns="Symbol,Security,From Series,To Series,Change Date,Remarks",
            ),

            "auction_buy": DatasetConfig(
                name="Auction Buy File",
                description="Auction-buy session results. Settlement number (settno) is auto-calculated from the date. "
                            "You can also override: settno='{YYYYNNN}' e.g. '2026094'.",
                url_pattern="/content/nsccl/AUB_{settno}_{ddmmyyyy}.csv",
                file_pattern="AUB_{settno}_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                skip_rows=1,
                frequency="Daily",
                columns="Symbol,Series,Security Name,Quantity",
            ),

            "cm_latency": DatasetConfig(
                name="CM Latency Statistics",
                description="Order/trade latency statistics for cash market.",
                url_pattern="/content/CM_Latency_stats{ddmmyyyy}.csv",
                file_pattern="CM_Latency_stats{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Latency statistics for the trading date",
            ),

            "mf_var": DatasetConfig(
                name="Mutual Fund VaR File",
                description="Daily VaR applicable to MF units pledged as collateral.",
                url_pattern="/archives/equities/mf_haircut/MF_VAR_{ddmmyyyy}.csv",
                file_pattern="MF_VAR_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,SYMBOL,SERIES,TYPE,HAIRCUT,NAV",
            ),

            "appsec_collval": DatasetConfig(
                name="Approved Security Collateral Valuation",
                description="Daily haircut-applied valuation of securities accepted as collateral.",
                url_pattern="/content/equities/APPSEC_COLLVAL_{ddmmyyyy}.csv",
                file_pattern="APPSEC_COLLVAL_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Token,Symbol,ISIN,Closing Price,Haircut%",
            ),

            "csqr": DatasetConfig(
                name="Client Segregation Quarterly Report (CSQR)",
                description="Client-level collateral segregation. Settlement number (settno) is auto-calculated from the date. "
                            "You can also override: settno='{YYYYNNN}'. No header row.",
                url_pattern="/archives/equities/csqr/CSQR_M{settno}_{ddmmyyyy}.csv",
                file_pattern="CSQR_M{settno}_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="MemberCode,Series,SegmentCode,SettlementNo,Amount",
            ),

            "c_stt": DatasetConfig(
                name="Securities Transaction Tax (C_STT)",
                description="Daily STT collection per security.",
                url_pattern="/content/equities/C_STT_{ddmmyyyy}.csv",
                file_pattern="C_STT_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="STT collection data",
            ),

            "c_stt_ind": DatasetConfig(
                name="Securities Transaction Tax Indicator (C_STT_IND)",
                description="STT indicator flags per security/series.",
                url_pattern="/content/equities/C_STT_IND_{ddmmyyyy}.csv",
                file_pattern="C_STT_IND_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="SYMBOL,SERIES,ISIN,Sec Desc,STT Indicator",
            ),

            "fcm_bc": DatasetConfig(
                name="FCM Interim Bhavcopy",
                description="Interim bhavcopy for clearing/margining before EOD files. Fixed-width DAT format.",
                url_pattern="/content/trdops/FCM_INTRM_BC{ddmmyyyy}.DAT",
                file_pattern="FCM_INTRM_BC{ddmmyyyy}.DAT",
                file_format="dat",
                portal_only=False,
                frequency="Daily",
                columns="Security,Symbol,Series,PrevClose,Open,High,Low,Close,TradeDate",
            ),

            "mrg_trading": DatasetConfig(
                name="Margin Trading Facility Report",
                description="Margin trading facility activity. Delivered as ZIP containing CSV.",
                url_pattern="/content/equities/mrg_trading_{ddmmyy}.zip",
                file_pattern="mrg_trading_{ddmmyy}.zip",
                file_format="zip_csv",
                portal_only=False,
                frequency="Daily",
                columns="SEBI Report data on margin trading",
            ),

            "cvar1": DatasetConfig(
                name="VaR Margin File (C_VAR1)",
                description="6 intraday snapshots of VaR margin. Snapshot number 1-6 appended to filename. "
                            "Use snapshot param 1-6.",
                url_pattern="/archives/nsccl/var/C_VAR1_{ddmmyyyy}_{snapshot}.DAT",
                file_pattern="C_VAR1_{ddmmyyyy}_{snapshot}.DAT",
                file_format="dat",
                download_only=True,
                frequency="Daily (6 intraday snapshots)",
                columns="Exchange,Date,ELM%,Total Records",
            ),

            "fcm_bc": DatasetConfig(
                name="FCM Interim Bhavcopy",
                description="Interim bhavcopy for clearing/margining before EOD files. Fixed-width DAT format.",
                url_pattern="/content/trdops/FCM_INTRM_BC{ddmmyyyy}.DAT",
                file_pattern="FCM_INTRM_BC{ddmmyyyy}.DAT",
                file_format="dat",
                portal_only=False,
                frequency="Daily",
                columns="Security,Symbol,Series,PrevClose,Open,High,Low,Close,TradeDate",
            ),

            "corpbond": DatasetConfig(
                name="Corporate Bond Market Data",
                description="Traded corporate bonds EOD — extracted from PR ZIP bundle.",
                url_pattern="/archives/equities/bhavcopy/pr/PR{ddmmyy}.zip",
                file_pattern="corpbond{ddmmyyyy}.csv",
                file_format="zip_csv",
                zip_extract=r"^corpbond\d{8}\.csv$",
                frequency="Daily",
                columns="MARKET,SERIES,SYMBOL,SECURITY,PREV_CL_PR,OPEN_PRICE,HIGH_PRICE,LOW_PRICE,CLOSE_PRICE,NET_TRDVAL,NET_TRDQTY,CORP_IND,TRADES,HI_52_WK,LO_52_WK",
            ),

            "mrg_trading": DatasetConfig(
                name="Margin Trading Facility Report",
                description="Margin trading facility activity. Delivered as ZIP containing CSV.",
                url_pattern="/content/equities/mrg_trading_{ddmmyy}.zip",
                file_pattern="mrg_trading_{ddmmyy}.zip",
                file_format="zip_csv",
                portal_only=False,
                frequency="Daily",
                columns="SEBI Report data on margin trading",
            ),

            # Monthly
            "c_catg": DatasetConfig(
                name="CM Security Categorisation (C_CATG)",
                description="Monthly classification of securities into risk groups I/II/III. "
                            "Drives VaR margin multiplier. Pipe-delimited T01 format.",
                url_pattern="/content/nsccl/C_CATG_{MON}{YYYY}.T01",
                file_pattern="C_CATG_{MON}{YYYY}.T01",
                file_format="t01",
                date_type="monthly",
                frequency="Monthly",
                columns="Month,Year,TotalRecords",
            ),

            "daily_settlement_doc": DatasetConfig(
                name="Daily Settlement Statistics",
                description="Word document with daily settlement statistics. DOC format — not parseable as DataFrame. "
                            "URL: /content/nsccl/Daily_Settlement_Statistics_{DDMMYYYY}.doc",
                url_pattern="/content/nsccl/Daily_Settlement_Statistics_{ddmmyyyy}.doc",
                file_pattern="Daily_Settlement_Statistics_{ddmmyyyy}.doc",
                file_format="pdf",
                download_only=True,
                portal_only=False,
                df_supported=False,
                frequency="Daily",
            ),
        },

        # ── Indices ────────────────────────────────────────────
        "indices": {

            "ind_close_all": DatasetConfig(
                name="All Indices Daily Close Values",
                description="EOD values for all 147+ NSE indices: OHLC, P/E, P/B, Div Yield, Volume.",
                url_pattern="/content/indices/ind_close_all_{ddmmyyyy}.csv",
                file_pattern="ind_close_all_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Index Name,Index Date,Open Index Value,High Index Value,Low Index Value,Closing Index Value,Points Change,Change(%),Volume,Turnover (Rs. Cr.),P/E,P/B,Div Yield",
            ),

            "top_movers": DatasetConfig(
                name="Index Top Movers",
                description="Top 10 securities by weight/movement for Nifty 50 and other indices.",
                url_pattern="/content/indices/top10nifty50_{ddmmyy}.csv",
                file_pattern="top10nifty50_{ddmmyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="SYMBOL,SECURITY,WEIGHTAGE(%)",
            ),
        },

        # ── Mutual Fund ────────────────────────────────────────
        "mutual_fund": {

            "nsccl_cm_ann_mf": DatasetConfig(
                name="NSCCL CM Annexure – Mutual Funds",
                description="NSCCL CM Annexure for mutual funds — ZIP containing XLSX workbook. "
                            "Use sheet_name param or sheet index to access specific sheet.",
                url_pattern="/content/nsccl/nsccl_cm_ann_mf.zip",
                base_url="https://nsearchives.nseindia.com",
                file_pattern="nsccl_cm_ann_mf.zip",
                file_format="zip_xlsx",
                portal_only=False,
                date_type="static",
                frequency="Monthly (static file, always current)",
                columns="Multiple sheets: member-wise MF data",
            ),
        },

        # ── Securities Lending & Borrowing ─────────────────────
        "slb": {

            "slb_elg_sec": DatasetConfig(
                name="SLB Eligible Securities List",
                description="List of securities eligible for lending/borrowing with eligibility types. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/slbs/seclist/SLB_ELG_SEC_{ddmmyyyy}.csv",
                                file_pattern="SLB_ELG_SEC_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Sr.No.,Symbol,Series,Normal Eligibility,Recall Eligibility,Repay Eligibility,Market Type",
            ),

            "slb_openpos": DatasetConfig(
                name="SLB Open Positions",
                description="Open positions at SLB member/client level. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/slbs/open_pos/slb_openpos_{ddmmyyyy}.csv",
                                file_pattern="slb_openpos_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Sr no,Security,Series,Outstanding Quantity at the end of the day",
            ),

            "slb_foreclosure": DatasetConfig(
                name="SLB Foreclosure Report",
                description="SLB foreclosure events with corporate action details. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/slbs/Forclosure_SLB_{yyyymmdd}.CSV",
                                file_pattern="Forclosure_SLB_{yyyymmdd}.CSV",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="SECURITY,SERIES,ISIN,ANNOUNCEMENT DATE,BOOK CLOSURE START DATE,RECORD DATE,EX DATE,FORECLOSURE DATE",
            ),

            "slb_bc": DatasetConfig(
                name="SLB Bhavcopy (SLBM_BC)",
                description="Daily SLB segment trade summary. Fixed-width DAT format.",
                url_pattern="/archives/slbs/bhavcopy/SLBM_BC_{ddmmyyyy}.DAT",
                file_pattern="SLBM_BC_{ddmmyyyy}.DAT",
                file_format="dat",
                download_only=True,
                portal_only=False,
                frequency="Daily",
                columns="Security,Symbol,Expiry,Open,High,Low,Close,Lend/Borrow,TradeDate",
            ),

            "slb_var": DatasetConfig(
                name="SLB VaR Margin File",
                description="VaR margin parameter file for SLB segment.",
                url_pattern="/archives/slbs/var/C_VAR1_SLB_{ddmmyyyy}_1.DAT",
                file_pattern="C_VAR1_SLB_{ddmmyyyy}_1.DAT",
                file_format="dat",
                download_only=True,
                portal_only=False,
                frequency="Daily",
                columns="Exchange,Date,ELM%,Total Records",
            ),

            "slb_positions": DatasetConfig(
                name="SLB Positions",
                description="SLB positions weekly/monthly. Excel format (XLS). NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="slbs_positions_{ddmmyyyy}.xls",
                file_format="xls",
                portal_only=True,
                frequency="Weekly/Monthly",
                columns="SLB position data",
            ),

            "slb_transactions": DatasetConfig(
                name="SLB Transactions",
                description="SLB transaction data weekly/monthly. Excel format (XLS). NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="slbs_transactions_{ddmmyyyy}.xls",
                file_format="xls",
                portal_only=True,
                frequency="Weekly/Monthly",
                columns="SLB transaction data",
            ),

            "slb_cli": DatasetConfig(
                name="SLB Client-Level Position Limits",
                description="Monthly client-level SLB position limits. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/slbs/cli/slbs_cli_{Mon}{YYYY}.csv",
                                file_pattern="slbs_cli_{mon}{yyyy}.csv",
                file_format="csv",
                portal_only=False,
                date_type="monthly",
                frequency="Monthly",
                columns="SYMBOL,Client Limit (no. of shares)",
            ),

            "slb_fopl": DatasetConfig(
                name="SLB Fund-of-Pool Limits",
                description="Monthly SLB fund-of-pool limit statistics. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/slbs/fopl/slbs_fopl_{Mon}{YYYY}.csv",
                                file_pattern="slbs_fopl_{mon}{yyyy}.csv",
                file_format="csv",
                portal_only=False,
                date_type="monthly",
                frequency="Monthly",
                columns="SYMBOL,Participant Limit (no. of shares)",
            ),

            "slb_mpl": DatasetConfig(
                name="SLB Member Position Limits",
                description="Monthly member-level position-limit utilization. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/slbs/mpl/slbs_mpl_{Mon}{YYYY}.csv",
                                file_pattern="slbs_mpl_{mon}{yyyy}.csv",
                file_format="csv",
                portal_only=False,
                date_type="monthly",
                frequency="Monthly",
                columns="SYMBOL,MWPL(no. of shares)",
            ),

            "slb_ppl": DatasetConfig(
                name="SLB Pool Position Limits",
                description="Monthly pool-level position-limit utilization. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/slbs/ppl/slbs_ppl_{Mon}{YYYY}.csv",
                                file_pattern="slbs_ppl_{mon}{yyyy}.csv",
                file_format="csv",
                portal_only=False,
                date_type="monthly",
                frequency="Monthly",
                columns="SYMBOL,Participant Limit (no. of shares)",
            ),

            "slb_transaction_data": DatasetConfig(
                name="SLB Transaction Data (Monthly)",
                description="Monthly SLB transaction dump with yields and turnover.",
                url_pattern="/archives/slbs/transaction/SLB_Transaction_Data_{Mon}{YYYY}.csv",
                file_pattern="SLB_Transaction_Data_{Mon}{YYYY}.csv",
                file_format="csv",
                portal_only=False,
                date_type="monthly",
                frequency="Monthly",
                columns="SYMBOL,QUANTITY,Lending Fee (Rs.),Turnover (Rs.),Weighted Average yield %,Count of Trades",
            ),
        },
    },

    # ════════════════════════════════════════════════════════════
    # DERIVATIVES
    # ════════════════════════════════════════════════════════════
    "derivatives": {

        # ── Equity Derivatives ─────────────────────────────────
        "equity": {

            "fo_bhav_udiff": DatasetConfig(
                name="F&O Bhavcopy (UDiFF format)",
                description="F&O bhavcopy in modern ISIN-keyed UDiFF format.",
                url_pattern="/content/fo/BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_pattern="BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_format="zip_csv",
                frequency="Daily",
                columns="TradDt,BizDt,Sgmt,FinInstrmId,ISIN,TckrSymb,OpnPric,HghPric,LwPric,ClsPric,TtlTradgVol,OpnIntrst",
            ),

            "fo_contract": DatasetConfig(
                name="F&O Contract Master",
                description="All active F&O contracts: lot size, strike, expiry, instrument type. GZIP CSV.",
                url_pattern="/content/fo/NSE_FO_contract_{ddmmyyyy}.csv.gz",
                file_pattern="NSE_FO_contract_{ddmmyyyy}.csv.gz",
                file_format="gz_csv",
                frequency="Daily",
                columns="Instrument,Symbol,Expiry,Strike,OptionType,LotSize,TickSize,ISIN,UnderlyingSymbol",
            ),

            "fo_secban": DatasetConfig(
                name="F&O Security Ban List",
                description="Securities in F&O ban period (crossed 95% of MWPL).",
                url_pattern="/archives/fo/sec_ban/fo_secban_{ddmmyyyy}.csv",
                file_pattern="fo_secban_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Security in ban period",
            ),

            "fovolt": DatasetConfig(
                name="F&O Volatility (FOVOLT)",
                description="Per-underlying annualized and daily volatility for F&O margin computation.",
                url_pattern="/archives/nsccl/volt/FOVOLT_{ddmmyyyy}.csv",
                file_pattern="FOVOLT_{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Date,Symbol,Underlying Price,Previous Price,Log Return,Previous Volatility,Daily Volatility,Annualised Volatility",
            ),

            "fopl": DatasetConfig(
                name="F&O Position Limits (fopl)",
                description="Monthly F&O position limit per security.",
                url_pattern="/content/nsccl/fopl_{mon}{yyyy}.csv",
                file_pattern="fopl_{mon}{yyyy}.csv",
                file_format="csv",
                date_type="monthly",
                frequency="Monthly",
                columns="F&O position limit data",
            ),

            "mpl": DatasetConfig(
                name="Member Position Limits (mpl)",
                description="Monthly member-level F&O position limits.",
                url_pattern="/content/nsccl/mpl_{mon}{yyyy}.csv",
                file_pattern="mpl_{mon}{yyyy}.csv",
                file_format="csv",
                date_type="monthly",
                frequency="Monthly",
                columns="Member position limit data",
            ),

            "tmopl": DatasetConfig(
                name="TM Open Position Limits (tmopl)",
                description="Monthly TM open position limits.",
                url_pattern="/content/nsccl/tmopl_{mon}{yyyy}.csv",
                file_pattern="tmopl_{mon}{yyyy}.csv",
                file_format="csv",
                date_type="monthly",
                frequency="Monthly",
                columns="TM open position limit data",
            ),

            "fo_impact_cost": DatasetConfig(
                name="F&O Impact Cost",
                description="Monthly F&O impact cost file.",
                url_pattern="/content/nsccl/ic_{mon}{yyyy}.csv",
                file_pattern="ic_{mon}{yyyy}.csv",
                file_format="csv",
                date_type="monthly",
                frequency="Monthly",
                columns="Impact cost data",
            ),
        },

        # ── Commodity Derivatives ──────────────────────────────
        "commodity": {

            "co_bhav_udiff": DatasetConfig(
                name="Commodity Bhavcopy (UDiFF format)",
                description="Commodity derivatives bhavcopy in UDiFF format.",
                url_pattern="/content/com/BhavCopy_NSE_CO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_pattern="BhavCopy_NSE_CO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_format="zip_csv",
                frequency="Daily",
                columns="TradDt,BizDt,Sgmt,FinInstrmId,ISIN,TckrSymb,OpnPric,HghPric,LwPric,ClsPric,TtlTradgVol,OpnIntrst",
            ),

            "co_contract": DatasetConfig(
                name="Commodity Contract Master",
                description="All active commodity contracts. GZIP CSV.",
                url_pattern="/content/com/NSE_COM_contract_{ddmmyyyy}.csv.gz",
                file_pattern="NSE_COM_contract_{ddmmyyyy}.csv.gz",
                file_format="gz_csv",
                frequency="Daily",
                columns="Instrument,Symbol,Expiry,Strike,OptionType,LotSize,TickSize",
            ),

            "payinpayout": DatasetConfig(
                name="Pay-in Pay-out Report",
                description="Monthly commodity derivatives pay-in / pay-out report. ZIP containing XLSX file in subfolder.",
                url_pattern="/archives/com/comp_reports/Payinpayout_{MON}{YYYY}.zip",
                file_pattern="Payinpayout_{MON}{YYYY}.zip",
                file_format="zip_xlsx",
                date_type="monthly",
                frequency="Monthly",
                columns="Pay-in/Pay-out data",
            ),
        },

        # ── Currency Derivatives ───────────────────────────────
        "currency": {

            "cd_bhav_udiff": DatasetConfig(
                name="Currency Derivatives Bhavcopy (UDiFF format)",
                description="Currency derivatives bhavcopy in UDiFF format. NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="BhavCopy_NSE_CD_0_0_0_{yyyymmdd}_F_0000.csv.zip",
                file_format="zip_csv",
                portal_only=True,
                frequency="Daily",
                columns="TradDt,BizDt,Sgmt,FinInstrmId,ISIN,TckrSymb,OpnPric,HghPric,LwPric,ClsPric,TtlTradgVol,OpnIntrst",
            ),

            "cd_contract": DatasetConfig(
                name="Currency Contract Master",
                description="All active currency contracts. GZIP CSV.",
                url_pattern="/content/cd/NSE_CD_contract_{ddmmyyyy}.csv.gz",
                file_pattern="NSE_CD_contract_{ddmmyyyy}.csv.gz",
                file_format="gz_csv",
                frequency="Daily",
                columns="Instrument,Symbol,Expiry,Strike,OptionType,LotSize,TickSize",
            ),

            "cd_pos_clients": DatasetConfig(
                name="CD Position of Clients",
                description="Currency derivatives position of clients. Excel XLS format. "
                            "Skip first row to get tabular data. NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="cd_pos_of_clients.xls",
                file_format="xls",
                portal_only=True,
                skip_rows=1,
                date_type="static",
                frequency="Monthly (static)",
                columns="Client positions in currency derivatives",
            ),
        },

        # ── Interest Rate Derivatives ──────────────────────────
        "interest_rate": {

            "irf_bhavcopy": DatasetConfig(
                name="IRF Bhavcopy ZIP",
                description="Interest Rate Futures bhavcopy. ZIP containing CSV files. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/ird/bhav/IRF_Bhavcopy{ddmmyy}.zip",
                                file_pattern="IRF_Bhavcopy{ddmmyy}.zip",
                file_format="zip_csv",
                portal_only=False,
                frequency="Daily",
                columns="IRF trade data",
            ),

            "i_volt": DatasetConfig(
                name="IRD Volatility (I_VOLT)",
                description="Interest Rate Derivative volatility file.",
                url_pattern="/archives/ird/volt/I_VOLT_{ddmmyyyy}.csv",
                file_pattern="I_VOLT_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Date,Symbol,Underlying Price,Previous Price,Log Return,Previous Volatility,Daily Volatility,Annualised Volatility",
            ),

            "cd_sett_irf": DatasetConfig(
                name="Currency Derivatives IRF Settlement Prices",
                description="Settlement prices for Interest Rate Futures contracts.",
                url_pattern="/archives/ird/sett/CDSett_prce_IRF_{ddmmyyyy}.csv",
                file_pattern="CDSett_prce_IRF_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Symbol,Expiry,Settlement Price",
            ),

            "ewpl": DatasetConfig(
                name="Early Warning Position Limits (EWPL)",
                description="EWPL for interest rate derivatives.",
                url_pattern="/archives/ird/ewpl/EWPL_{ddmmyyyy}.CSV",
                file_pattern="EWPL_{ddmmyyyy}.CSV",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="EWPL data",
            ),

            "fpi_long": DatasetConfig(
                name="Combined FPI Long Positions",
                description="Combined FPI long positions across derivatives. Encoding: latin-1. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/ird/fii/Combined_FPI_long_psn_{ddmmyyyy}.csv",
                                file_pattern="Combined_FPI_long_psn_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                encoding="latin-1",
                frequency="Daily",
                columns="FPI long position data",
            ),

            "fii_long": DatasetConfig(
                name="FII Long Positions",
                description="FII long positions in derivatives. Encoding: latin-1. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/ird/fii/fii_longpos_{ddmmyyyy}.csv",
                                file_pattern="fii_longpos_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                encoding="latin-1",
                frequency="Daily",
                columns="FII long position data",
            ),

            "tenure_symbol_map": DatasetConfig(
                name="Tenure-Symbol Map",
                description="Maps IRD tenures to symbols. LST fixed-width format. Date: DD-MON-YYYY uppercase e.g. 22-MAY-2026.",
                url_pattern="/content/equities/TENURE_SYMBOL_MAP_{DD-MON-YYYY}.lst",
                file_pattern="TENURE_SYMBOL_MAP_{DD-MON-YYYY}.lst",
                file_format="lst",
                download_only=True,
                portal_only=False,
                frequency="Daily",
                columns="Tenure,Symbol mapping",
            ),

            "irf_cli_oi": DatasetConfig(
                name="IRF Client OI Limit",
                description="IRF client-level open interest limits. Date: DD-MON-YYYY uppercase e.g. 22-MAY-2026.",
                url_pattern="/archives/ird/cli/i_oi_cli_limit_{DD-MON-YYYY}.lst",
                file_pattern="i_oi_cli_limit_{DD-MON-YYYY}.lst",
                file_format="lst",
                download_only=True,
                portal_only=False,
                frequency="Daily",
                columns="OI limit data",
            ),

            "irf_tm_oi": DatasetConfig(
                name="IRF TM OI Limit",
                description="IRF trading member open interest limits. Date: DD-MON-YYYY uppercase e.g. 22-MAY-2026.",
                url_pattern="/archives/ird/cli/i_oi_tm_limit_{DD-MON-YYYY}.lst",
                file_pattern="i_oi_tm_limit_{DD-MON-YYYY}.lst",
                file_format="lst",
                download_only=True,
                portal_only=False,
                frequency="Daily",
                columns="OI limit data",
            ),
        },
    },

    # ════════════════════════════════════════════════════════════
    # DEBT
    # ════════════════════════════════════════════════════════════
    "debt": {

        # ── Corporate Segment ──────────────────────────────────
        "corporate": {

            "cbm_trd": DatasetConfig(
                name="CB Daily Trades",
                description="Daily trades in corporate bonds: price, yield, value. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/debt/cbm/cbm_trd{yyyymmdd}.csv",
                                file_pattern="cbm_trd{yyyymmdd}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="Trade Date,ISIN,Last Trade Price (in Rs.),Last Trade Value (Rs. in lacs),Total Trade Value (Rs. in lacs),Last Trade Yield (YTM),Weighted Average Price,Weighted Average Yield",
            ),

            "cbm_list_man": DatasetConfig(
                name="CB Mandatory Settlement List",
                description="Mandatory-settlement corporate bond list. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cbm/cbm_list_man_{ddmmyyyy}.csv",
                                file_pattern="cbm_list_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "cbm_list_non_man": DatasetConfig(
                name="CB Non-Mandatory Settlement List",
                description="Non-mandatory corporate bond settlement list. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cbm/cbm_list_non_man_{ddmmyyyy}.csv",
                                file_pattern="cbm_list_non_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "cbm_fail": DatasetConfig(
                name="Corporate Bond Settlement Fails",
                description="Corporate bond trades that failed settlement. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cbm/cbm_fail_{ddmmyyyy}.csv",
                                file_pattern="cbm_fail_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "cbm_unlist_man": DatasetConfig(
                name="CB Unlisted Mandatory Settlement",
                description="Unlisted CB mandatory settlement list. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cbm/cbm_unlist_man_{ddmmyyyy}.csv",
                                file_pattern="cbm_unlist_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "cbm_unlist_non_man": DatasetConfig(
                name="CB Unlisted Non-Mandatory Settlement",
                description="Unlisted CB non-mandatory settlement list. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cbm/cbm_unlist_non_man_{ddmmyyyy}.csv",
                                file_pattern="cbm_unlist_non_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "sdt_fail": DatasetConfig(
                name="SDT Settlement Fails",
                description="Failed settlement direct trades. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/sdi/sdt_fail_{ddmmyyyy}.csv",
                                file_pattern="sdt_fail_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "sdt_list_man": DatasetConfig(
                name="SDT Mandatory Settlement List",
                description="Mandatory SDT settlement list. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/sdi/sdt_list_man_{ddmmyyyy}.csv",
                                file_pattern="sdt_list_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "sdt_list_non_man": DatasetConfig(
                name="SDT Non-Mandatory Settlement List",
                description="Non-mandatory SDT settlement list. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/sdi/sdt_list_non_man_{ddmmyyyy}.csv",
                                file_pattern="sdt_list_non_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "sdt_unlist_man": DatasetConfig(
                name="SDT Unlisted Mandatory",
                description="Unlisted mandatory SDT settlement. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/sdi/sdt_unlist_man_{ddmmyyyy}.csv",
                                file_pattern="sdt_unlist_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "sdt_unlist_non_man": DatasetConfig(
                name="SDT Unlisted Non-Mandatory",
                description="Unlisted non-mandatory SDT settlement. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/sdi/sdt_unlist_non_man_{ddmmyyyy}.csv",
                                file_pattern="sdt_unlist_non_man_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Description,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "cp_settlement": DatasetConfig(
                name="Commercial Paper Settlement Order Report",
                description="Settlement orders for commercial paper segment. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cd/CP_SettlementOrderReport_{ddmmyyyy}.csv",
                                file_pattern="CP_SettlementOrderReport_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Descriptor,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "cd_settlement": DatasetConfig(
                name="Convertible Debenture Settlement Order Report",
                description="Settlement orders for convertible debenture segment. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/cd/CD_SettlementOrderReport_{ddmmyyyy}.csv",
                                file_pattern="CD_SettlementOrderReport_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Descriptor,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "gsec_settlement": DatasetConfig(
                name="G-Sec Settlement Order Report",
                description="G-Sec settlement order report. NSE portal session required — not available via direct archive URL",
                url_pattern="/archives/debt/cbm/GSEC_SettlementOrderReport_{ddmmyyyy}.csv",
                                file_pattern="GSEC_SettlementOrderReport_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="ISIN,Descriptor,Trade Date,Quantity,Nominal Value,Weighted Average Price,Weighted Average Yield",
            ),

            "corporate_bond_report": DatasetConfig(
                name="Corporate Bond Monthly Report",
                description="Monthly CB market statistics. Large CSV with multiple sections. NSE portal session required — not available via direct archive URL",
                url_pattern="/content/debt/Corporate_bond_report_{dd-Mon-YYYY}.csv",
                                file_pattern="Corporate_bond_report_{dd-Mon-YYYY}.csv",
                file_format="csv",
                portal_only=False,
                frequency="Daily",
                columns="National Stock Exchange Of India Limited monthly CB data",
            ),
        },

        # ── Debt Segment ───────────────────────────────────────
        "debt_segment": {

            "wdmlist": DatasetConfig(
                name="WDM Securities List",
                description="Current WDM security list with ISIN, description, face value. NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="wdmlist_{ddmmyyyy}.csv",
                file_format="csv",
                portal_only=True,
                frequency="Daily",
                columns="WDM securities list",
            ),

            "dly_bundle": DatasetConfig(
                name="Debt Daily Bundle ZIP",
                description="WDM daily files bundle. ZIP containing daily debt market files.",
                url_pattern="/content/debt/dly{ddmmyyyy}.zip",
                base_url="https://nsearchives.nseindia.com",
                file_pattern="dly{ddmmyyyy}.zip",
                file_format="zip_csv",
                portal_only=False,
                frequency="Daily",
                columns="WDM daily files: trade report, adds, mats, settlements",
            ),

            "wkly_bundle": DatasetConfig(
                name="Debt Weekly Bundle ZIP",
                description="WDM weekly files bundle. ZIP containing weekly debt market files. NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="wkly{ddmmyyyy}.zip",
                file_format="zip_csv",
                portal_only=True,
                frequency="Weekly",
                columns="WDM weekly files",
            ),

            "accrued_interest": DatasetConfig(
                name="Accrued Interest File",
                description="Monthly accrued interest file for WDM securities. NSE portal session required — not available via direct archive URL",
                url_pattern="",
                base_url="",
                file_pattern="ACCTINT_{MON}{YYYY}.csv",
                file_format="csv",
                portal_only=True,
                date_type="monthly",
                frequency="Monthly",
                columns="Accrued interest data",
            ),
        },

        # ── Tri-Party Repo ─────────────────────────────────────
        "tri_party_repo": {

            "trm_bc": DatasetConfig(
                name="Tri-Party Repo Bhavcopy",
                description="Daily tri-party repo segment trade summary.",
                url_pattern="/content/nsccl/TRM_BC{ddmmyyyy}.csv",
                file_pattern="TRM_BC{ddmmyyyy}.csv",
                file_format="csv",
                frequency="Daily",
                columns="Tri-party repo daily trade data",
            ),
        },
    },

    # ════════════════════════════════════════════════════════════
    # EGR
    # ════════════════════════════════════════════════════════════
    "egr": {
        "egr": {
            "egr_bc": DatasetConfig(
                name="EGR Bhavcopy",
                description="Electronic Gold Receipt bhavcopy. Fixed-width DAT format.",
                url_pattern="/archives/egr/EG_BC{ddmmyyyy}.DAT",
                file_pattern="EG_BC{ddmmyyyy}.DAT",
                file_format="dat",
                download_only=True,
                frequency="Daily",
                columns="EGR trade data",
            ),
        },
    },
}


def get_config(category: str, subcategory: str, dataset: str) -> DatasetConfig:
    """Get a DatasetConfig by category/subcategory/dataset."""
    try:
        return REGISTRY[category.lower()][subcategory.lower()][dataset.lower()]
    except KeyError:
        available = list_datasets()
        raise ValueError(
            f"Unknown dataset: '{category}/{subcategory}/{dataset}'\n"
            f"Use nse.list_datasets() to see all available datasets."
        )


def list_datasets(category: str = None, subcategory: str = None) -> list:
    """List all available (category, subcategory, dataset_key, name) tuples."""
    results = []
    for cat, subs in REGISTRY.items():
        if category and cat != category.lower():
            continue
        for sub, datasets in subs.items():
            if subcategory and sub != subcategory.lower():
                continue
            for key, cfg in datasets.items():
                results.append({
                    'category': cat,
                    'subcategory': sub,
                    'dataset': key,
                    'name': cfg.name,
                    'frequency': cfg.frequency,
                    'df_supported': cfg.df_supported and not cfg.download_only,
                    'format': cfg.file_format,
                })
    return results
