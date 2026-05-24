"""
MCX Dataset Registry — single source of truth for all supported datasets.

Structure mirrors nse-data registry pattern.
"""

from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class DatasetConfig:
    """Configuration for a single MCX dataset."""
    name: str
    description: str
    url_pattern: str
    base_url: str = "https://www.mcxindia.com"
    file_pattern: str = ""
    file_format: str = "csv"
    date_type: Literal["daily", "monthly", "static"] = "daily"
    df_supported: bool = True
    download_only: bool = False
    portal_only: bool = False
    skip_rows: int = 0
    encoding: str = "utf-8"
    zip_extract: Optional[str] = None
    frequency: str = "Daily"
    columns: str = ""


MCX_BASE = "https://www.mcxindia.com"

# ─── REGISTRY ─────────────────────────────────────────────────────────────
# Placeholder — will be populated once MCX URLs are confirmed
# Structure: REGISTRY[category][subcategory][dataset_key]

REGISTRY = {
    # ===== Commodity =====
    "commodity": {
        # Add MCX datasets here once URLs are confirmed from mcxindia.com
        # Example structure:
        # "bhavcopy": DatasetConfig(
        #     name="MCX Bhavcopy",
        #     description="End-of-day commodity futures price data",
        #     url_pattern="/MarketData/MCXBhavcopy/{DDMMYYYY}_MCXBhavcopy.csv",
        #     file_format="csv",
        #     frequency="Daily",
        # ),
    },
}


def get_config(category: str, subcategory: str, dataset: str) -> DatasetConfig:
    try:
        return REGISTRY[category.lower()][subcategory.lower()][dataset.lower()]
    except KeyError:
        raise ValueError(
            f"Unknown MCX dataset: '{category}/{subcategory}/{dataset}'. "
            f"Use mcx.list_datasets() to see available datasets."
        )


def list_datasets(category: str = None) -> list:
    results = []
    for cat, subs in REGISTRY.items():
        if category and cat != category.lower():
            continue
        for sub, datasets in subs.items():
            for key, cfg in datasets.items():
                results.append({
                    'category': cat, 'subcategory': sub, 'dataset': key,
                    'name': cfg.name, 'frequency': cfg.frequency,
                    'df_supported': cfg.df_supported and not cfg.download_only,
                    'format': cfg.file_format,
                })
    return results
