"""
MCX Dataset Registry — single source of truth for all supported datasets.

Each DatasetConfig describes how to fetch one dataset:
  - page_url:       MCX page URL to load (for WebForms scraping)
  - export_target:  __doPostBack target for Excel export (or None for HTML parse)
  - commodity_id:   Select element ID for commodity filter
  - location_id:    Select element ID for location filter
  - date_field_id:  Input ID for date/from-date
  - to_date_id:     Input ID for to-date (archive only)
  - date_type:      "daily" | "monthly" | "range" | "static"
  - df_supported:   True if data can be returned as DataFrame (parsed table)
  - download_only:  True if only Excel export is supported

Naming convention mirrors nse-data: REGISTRY[category][subcategory][dataset_key]
"""

from dataclasses import dataclass, field
from typing import Optional, Literal


@dataclass
class DatasetConfig:
    """Configuration for one MCX dataset."""
    name: str
    description: str
    page_url: str                         # MCX page to load
    table_id: Optional[str] = None        # HTML table ID to parse (None = first table)
    export_target: Optional[str] = None   # __doPostBack target for Excel export
    commodity_field: Optional[str] = None # Form field name for commodity filter
    location_field: Optional[str] = None  # Form field name for location filter
    date_field: Optional[str] = None      # Form field name for (from-)date
    to_date_field: Optional[str] = None   # Form field name for to-date (range)
    commodity_select_id: Optional[str] = None  # <select> element ID
    location_select_id: Optional[str] = None   # <select> element ID
    date_type: Literal["recent", "daily", "range", "monthly", "static"] = "recent"
    date_format: str = "%d/%m/%Y"         # How MCX expects dates in POST
    file_format: str = "html"             # "html" (parse table) or "excel"
    df_supported: bool = True
    download_only: bool = False
    portal_only: bool = False
    skip_rows: int = 0
    frequency: str = "Daily"
    notes: str = ""


MCX_BASE = "https://www.mcxindia.com"

# ─── REGISTRY ──────────────────────────────────────────────────────────────────
REGISTRY: dict = {

    # ══════════════════════════════════════════════════════════════════════════
    # SPOT MARKET
    # URL: https://www.mcxindia.com/market-data/spot-market-price
    #
    # "Recent" tab: shows today's spot prices (all commodities + locations)
    #   — No filters, just load the page and parse the table
    #
    # "Archives" tab: filter by Commodity + date range → Excel export
    #   — POST form with __doPostBack export target
    # ══════════════════════════════════════════════════════════════════════════
    "spot": {
        "market": {

            # Recent spot prices (today's data — no date param needed)
            "spot_recent": DatasetConfig(
                name="Spot Market Price — Recent",
                description=(
                    "Current day spot prices for all commodities and locations. "
                    "Commodity, Unit, Location, Spot Price (Rs.), and Up/Down."
                ),
                page_url=f"{MCX_BASE}/market-data/spot-market-price",
                table_id=None,  # parse first data table
                export_target="ctl00$cph_InnerContainerRight$C004$lnkExpToExcel",
                commodity_field="ctl00$cph_InnerContainerRight$C004$ddlCommodity",
                location_field="ctl00$cph_InnerContainerRight$C004$ddlLocation",
                date_type="recent",
                file_format="html",
                df_supported=True,
                frequency="Daily (intraday)",
                notes="Recent tab — no date filter. Exports all commodity spot prices as of market close.",
            ),

            # Archive spot prices (historical — date range + commodity filter)
            "spot_archive": DatasetConfig(
                name="Spot Market Price — Archive",
                description=(
                    "Historical spot prices with date range and optional commodity filter. "
                    "Returns daily spot price series per commodity."
                ),
                page_url=f"{MCX_BASE}/market-data/spot-market-price",
                export_target="ctl00$cph_InnerContainerRight$C004$lnkExpToExcelArchive",
                commodity_field="ctl00$cph_InnerContainerRight$C004$ddlCommodityArchive",
                date_field="ctl00$cph_InnerContainerRight$C004$txtFromDate",
                to_date_field="ctl00$cph_InnerContainerRight$C004$txtToDate",
                commodity_select_id="cph_InnerContainerRight_C004_ddlCommodityArchive",
                date_type="range",
                date_format="%d/%m/%Y",
                file_format="html",
                df_supported=True,
                frequency="Daily",
                notes=(
                    "Archives tab — requires from_date + to_date (DD/MM/YYYY). "
                    "Commodity filter: use 'ALL' for all commodities or specific name e.g. 'GOLD'."
                ),
            ),
        },
    },
}


# ─── Helper functions ─────────────────────────────────────────────────────────

def get_config(category: str, subcategory: str, dataset: str) -> DatasetConfig:
    """Look up a DatasetConfig by path. Raises ValueError if not found."""
    try:
        return REGISTRY[category.lower()][subcategory.lower()][dataset.lower()]
    except KeyError:
        available = list_datasets()
        opts = [f"{r['category']}/{r['subcategory']}/{r['dataset']}" for r in available]
        raise ValueError(
            f"Unknown MCX dataset: '{category}/{subcategory}/{dataset}'.\n"
            f"Available: {opts}"
        )


def list_datasets(category: str = None) -> list:
    """Return list of dicts describing all registered datasets."""
    results = []
    for cat, subs in REGISTRY.items():
        if category and cat != category.lower():
            continue
        for sub, datasets in subs.items():
            for key, cfg in datasets.items():
                results.append({
                    "category":    cat,
                    "subcategory": sub,
                    "dataset":     key,
                    "name":        cfg.name,
                    "description": cfg.description,
                    "frequency":   cfg.frequency,
                    "date_type":   cfg.date_type,
                    "df_supported": cfg.df_supported and not cfg.download_only,
                    "format":      cfg.file_format,
                    "notes":       cfg.notes,
                })
    return results
