"""
BSE Dataset Registry.

All 50+ BSE indices available via the API.
Single source of truth for index names and metadata.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class IndexConfig:
    """Configuration for one BSE index."""
    name: str           # Display name
    api_key: str        # Key used in BSE API calls (index= param)
    category: str       # Broad Market / Sectoral / Thematic / Strategy / Global
    description: str    # What this index tracks


# ── All BSE indices available via GetIndexData API ────────────────────────────
BSE_INDICES: dict[str, IndexConfig] = {

    # ── Broad Market ──────────────────────────────────────────────────────────
    "SENSEX": IndexConfig(
        "SENSEX", "SENSEX", "Broad Market",
        "BSE's flagship index — top 30 large-cap companies by free-float market cap. "
        "India's most tracked equity benchmark since 1986."
    ),
    "SENSEX50": IndexConfig(
        "SENSEX 50", "SENSEX50", "Broad Market",
        "Top 50 companies by free-float market cap on BSE."
    ),
    "SENSEXNXT50": IndexConfig(
        "SENSEX NEXT 50", "SENSEXNXT50", "Broad Market",
        "Next 50 companies after SENSEX 50 — mid-large cap segment."
    ),
    "BSE100": IndexConfig(
        "BSE 100", "BSE100", "Broad Market",
        "Top 100 companies by free-float market cap. Covers ~80% of BSE market cap."
    ),
    "BSE200": IndexConfig(
        "BSE 200", "BSE200", "Broad Market",
        "Top 200 companies. Broad representation of the Indian equity market."
    ),
    "BSE500": IndexConfig(
        "BSE 500", "BSE500", "Broad Market",
        "Top 500 companies — covers ~93% of total BSE market cap. Most comprehensive index."
    ),
    "BSEALLCAP": IndexConfig(
        "BSE ALLCAP", "BSEALLCAP", "Broad Market",
        "All listed companies with adequate liquidity. Widest market coverage."
    ),
    "BSEMIDCAP": IndexConfig(
        "BSE MIDCAP", "BSEMIDCAP", "Broad Market",
        "Mid-cap companies — ranked 101–300 by full market cap."
    ),
    "BSESMALLCAP": IndexConfig(
        "BSE SMALLCAP", "BSESMALLCAP", "Broad Market",
        "Small-cap companies — ranked 301+ by full market cap."
    ),
    "BSE150MIDCAP": IndexConfig(
        "BSE 150 MIDCAP", "BSE150MIDCAP", "Broad Market",
        "Top 150 mid-cap companies by free-float market cap."
    ),
    "BSE250SMALLCAP": IndexConfig(
        "BSE 250 SMALLCAP", "BSE250SMALLCAP", "Broad Market",
        "Top 250 small-cap companies."
    ),
    "BSE400MIDSMALLCAP": IndexConfig(
        "BSE 400 MID & SMALLCAP", "BSE400MIDSMALLCAP", "Broad Market",
        "Combined mid and small-cap index — 400 companies."
    ),
    "BSE250LARGEMIDCAP": IndexConfig(
        "BSE 250 LARGE & MIDCAP", "BSE250LARGEMIDCAP", "Broad Market",
        "Top 250 large and mid-cap companies."
    ),
    "BSE100LARGECAPTMC": IndexConfig(
        "BSE 100 LARGECAP TMC", "BSE100LARGECAPTMC", "Broad Market",
        "Top 100 large-cap companies by total market cap."
    ),
    "BSEMIDCAPSELECT": IndexConfig(
        "BSE MIDCAP SELECT", "BSEMIDCAPSELECT", "Broad Market",
        "Select mid-cap companies with strong fundamentals."
    ),
    "BSESMALLCAPSELECT": IndexConfig(
        "BSE SMALLCAP SELECT", "BSESMALLCAPSELECT", "Broad Market",
        "Select small-cap companies with strong fundamentals."
    ),
    "BSELARGECAP": IndexConfig(
        "BSE LARGECAP", "BSELARGECAP", "Broad Market",
        "Large-cap companies — top 100 by full market cap."
    ),

    # ── Sectoral ──────────────────────────────────────────────────────────────
    "BANKEX": IndexConfig(
        "BANKEX", "BANKEX", "Sectoral",
        "Top banking sector companies on BSE. Tracks performance of Indian banks."
    ),
    "BSEAUTO": IndexConfig(
        "BSE AUTO", "BSEAUTO", "Sectoral",
        "Automobile and auto-ancillary companies."
    ),
    "BSECG": IndexConfig(
        "BSE CAPITAL GOODS", "BSECG", "Sectoral",
        "Capital goods and industrial machinery companies."
    ),
    "BSECD": IndexConfig(
        "BSE CONSUMER DISCRETIONARY", "BSECD", "Sectoral",
        "Consumer discretionary sector — retail, media, leisure."
    ),
    "BSECDGS": IndexConfig(
        "BSE CONSUMER DURABLES", "BSECDGS", "Sectoral",
        "Consumer durables companies — appliances, electronics."
    ),
    "BSEENERGY": IndexConfig(
        "BSE ENERGY", "BSEENERGY", "Sectoral",
        "Energy sector — oil, gas, power generation and distribution."
    ),
    "BSEFMCG": IndexConfig(
        "BSE FMCG", "BSEFMCG", "Sectoral",
        "Fast-moving consumer goods companies."
    ),
    "BSEFINANCE": IndexConfig(
        "BSE FINANCIAL SERVICES", "BSEFINANCE", "Sectoral",
        "Financial services — banks, NBFCs, insurance, AMCs."
    ),
    "BSEHC": IndexConfig(
        "BSE HEALTHCARE", "BSEHC", "Sectoral",
        "Healthcare sector — pharma, hospitals, diagnostics."
    ),
    "BSEIT": IndexConfig(
        "BSE IT", "BSEIT", "Sectoral",
        "Information technology companies — software, IT services."
    ),
    "BSEINDUSTRIALS": IndexConfig(
        "BSE INDUSTRIALS", "BSEINDUSTRIALS", "Sectoral",
        "Industrial companies — engineering, defence, aerospace."
    ),
    "BSEMETAL": IndexConfig(
        "BSE METAL", "BSEMETAL", "Sectoral",
        "Metals and mining companies — steel, aluminium, copper."
    ),
    "BSEOILGAS": IndexConfig(
        "BSE OIL & GAS", "BSEOILGAS", "Sectoral",
        "Oil and gas sector — exploration, refining, distribution."
    ),
    "BSEPOWER": IndexConfig(
        "BSE POWER", "BSEPOWER", "Sectoral",
        "Power sector — generation, transmission, distribution."
    ),
    "BSEPRIVATEBANKS": IndexConfig(
        "BSE PRIVATE BANKS", "BSEPRIVATEBANKS", "Sectoral",
        "Private sector banks listed on BSE."
    ),
    "BSEPSU": IndexConfig(
        "BSE PSU", "BSEPSU", "Sectoral",
        "Public sector undertakings — government-owned companies."
    ),
    "BSEREALTY": IndexConfig(
        "BSE REALTY", "BSEREALTY", "Sectoral",
        "Real estate companies — developers, REITs."
    ),
    "BSESERVICES": IndexConfig(
        "BSE SERVICES", "BSESERVICES", "Sectoral",
        "Services sector — logistics, hospitality, media."
    ),
    "BSETECK": IndexConfig(
        "BSE TECK", "BSETECK", "Sectoral",
        "Technology, media and telecom companies."
    ),
    "BSETELECOM": IndexConfig(
        "BSE TELECOMMUNICATION", "BSETELECOM", "Sectoral",
        "Telecom companies — mobile, broadband, infrastructure."
    ),
    "BSEUTILS": IndexConfig(
        "BSE UTILITIES", "BSEUTILS", "Sectoral",
        "Utility companies — power, water, gas distribution."
    ),

    # ── Thematic ──────────────────────────────────────────────────────────────
    "BSECPSE": IndexConfig(
        "BSE CPSE", "BSECPSE", "Thematic",
        "Central Public Sector Enterprises — government disinvestment index."
    ),
    "BSEIPO": IndexConfig(
        "BSE IPO", "BSEIPO", "Thematic",
        "Recently listed IPO companies — tracks post-listing performance."
    ),
    "BSESMEIPO": IndexConfig(
        "BSE SME IPO", "BSESMEIPO", "Thematic",
        "SME IPO companies listed on BSE SME platform."
    ),
    "BSEGREENEX": IndexConfig(
        "BSE GREENEX", "BSEGREENEX", "Thematic",
        "Companies with strong environmental/green credentials."
    ),
    "BSECARBONEX": IndexConfig(
        "BSE CARBONEX", "BSECARBONEX", "Thematic",
        "Companies with low carbon footprint and sustainability focus."
    ),
    "BSEINFRA": IndexConfig(
        "BSE INDIA INFRASTRUCTURE", "BSEINFRA", "Thematic",
        "Infrastructure companies — roads, ports, airports, utilities."
    ),
    "BSEMANUFACTURING": IndexConfig(
        "BSE INDIA MANUFACTURING", "BSEMANUFACTURING", "Thematic",
        "Manufacturing sector companies — Make in India theme."
    ),
    "BHARAT22": IndexConfig(
        "BHARAT 22", "BHARAT22", "Thematic",
        "22 government-owned companies selected for disinvestment. ETF benchmark."
    ),

    # ── Strategy / Factor ─────────────────────────────────────────────────────
    "BSEMOMENTUM": IndexConfig(
        "BSE MOMENTUM", "BSEMOMENTUM", "Strategy",
        "High-momentum stocks — companies with strong recent price performance."
    ),
    "BSEQUALITY": IndexConfig(
        "BSE QUALITY", "BSEQUALITY", "Strategy",
        "High-quality companies — strong ROE, low debt, stable earnings."
    ),
    "BSEVALUE": IndexConfig(
        "BSE ENHANCED VALUE", "BSEVALUE", "Strategy",
        "Value stocks — companies trading at discount to intrinsic value."
    ),
    "BSELOWVOL": IndexConfig(
        "BSE LOW VOLATILITY", "BSELOWVOL", "Strategy",
        "Low-volatility stocks — defensive portfolio with lower drawdowns."
    ),
    "BSEDIVSTAB": IndexConfig(
        "BSE DIVIDEND STABILITY", "BSEDIVSTAB", "Strategy",
        "Companies with consistent dividend payment history."
    ),
    "BSE100ESG": IndexConfig(
        "BSE 100 ESG", "BSE100ESG", "Strategy",
        "Top 100 companies screened for ESG (Environmental, Social, Governance) criteria."
    ),

    # ── Global / Dollar ───────────────────────────────────────────────────────
    "DOLLEX30": IndexConfig(
        "DOLLEX-30", "DOLLEX30", "Global",
        "SENSEX in USD terms — tracks SENSEX performance for foreign investors."
    ),
    "DOLLEX100": IndexConfig(
        "DOLLEX-100", "DOLLEX100", "Global",
        "BSE 100 in USD terms."
    ),
    "DOLLEX200": IndexConfig(
        "DOLLEX-200", "DOLLEX200", "Global",
        "BSE 200 in USD terms."
    ),
}


def get_index_config(index_key: str) -> IndexConfig:
    """Look up IndexConfig by API key. Case-insensitive."""
    key = index_key.upper().strip()
    if key in BSE_INDICES:
        return BSE_INDICES[key]
    # Try partial match on api_key
    for k, cfg in BSE_INDICES.items():
        if cfg.api_key.upper() == key:
            return cfg
    raise ValueError(
        f"Unknown BSE index: '{index_key}'. "
        f"Use bse.list_indices() to see all supported indices."
    )


def list_all_indices() -> list:
    """Return list of dicts for all registered BSE indices."""
    return [
        {
            "api_key":     cfg.api_key,
            "name":        cfg.name,
            "category":    cfg.category,
            "description": cfg.description,
        }
        for cfg in BSE_INDICES.values()
    ]
