"""
Constants for Yahoo Finance screener API.

This module contains all constants used throughout the package including:
- API URLs and endpoints
- Query operators
- Field name mappings
- Available sectors and regions
- Default configuration values

These constants ensure consistency across the package and provide
a single source of truth for API-related values.
"""

# API URLs
SCREENER_API_URL = "https://query2.finance.yahoo.com/v1/finance/screener"
CRUMB_URL = "https://query2.finance.yahoo.com/v1/test/getcrumb"
YAHOO_FINANCE_URL = "https://finance.yahoo.com"

# API Configuration
DEFAULT_PAGE_SIZE = 250
MAX_PAGE_SIZE = 250
DEFAULT_TIMEOUT = 30

# Query Operators
OPERATOR_GT = "GT"  # Greater than
OPERATOR_LT = "LT"  # Less than
OPERATOR_GTE = "GTE"  # Greater than or equal
OPERATOR_LTE = "LTE"  # Less than or equal
OPERATOR_EQ = "EQ"  # Equal
OPERATOR_BTWN = "BTWN"  # Between
OPERATOR_AND = "AND"  # Logical AND
OPERATOR_OR = "OR"  # Logical OR

# Yahoo Finance API field names
FIELD_PRICE = "intradayprice"
FIELD_MARKET_CAP = "marketcap"
FIELD_VOLUME = "volume"
FIELD_PE_RATIO = "peratio"
FIELD_PB_RATIO = "pbratio"
FIELD_PEG_RATIO = "pegratio"
FIELD_DIVIDEND_YIELD = "dividendyield"
FIELD_REVENUE_GROWTH = "revenuegrowth"
FIELD_EARNINGS_GROWTH = "earningsgrowth"
FIELD_PROFIT_MARGIN = "profitmargin"
FIELD_ROE = "returnonequity"
FIELD_ROA = "returnonassets"
FIELD_SECTOR = "sector"
FIELD_INDUSTRY = "industry"
FIELD_REGION = "region"
FIELD_EXCHANGE = "exchange"

# Field mappings: user-friendly name -> Yahoo Finance API field
FIELD_MAPPINGS = {
    "price": FIELD_PRICE,
    "market_cap": FIELD_MARKET_CAP,
    "volume": FIELD_VOLUME,
    "pe_ratio": FIELD_PE_RATIO,
    "pb_ratio": FIELD_PB_RATIO,
    "peg_ratio": FIELD_PEG_RATIO,
    "dividend_yield": FIELD_DIVIDEND_YIELD,
    "revenue_growth": FIELD_REVENUE_GROWTH,
    "earnings_growth": FIELD_EARNINGS_GROWTH,
    "profit_margin": FIELD_PROFIT_MARGIN,
    "roe": FIELD_ROE,
    "roa": FIELD_ROA,
    "sector": FIELD_SECTOR,
    "industry": FIELD_INDUSTRY,
    "region": FIELD_REGION,
    "exchange": FIELD_EXCHANGE,
}

# Reverse mapping: Yahoo Finance API field -> user-friendly name
REVERSE_FIELD_MAPPINGS = {v: k for k, v in FIELD_MAPPINGS.items()}

# YFinance-compatible field name mappings
# Maps Yahoo Finance API response fields to yfinance Ticker.info field names
YFINANCE_FIELD_MAPPINGS = {
    "symbol": "symbol",
    "longName": "longName",
    "shortName": "shortName",
    "regularMarketPrice": "currentPrice",
    "marketCap": "marketCap",
    "volume": "volume",
    "averageVolume": "averageVolume",
    "fiftyTwoWeekHigh": "fiftyTwoWeekHigh",
    "fiftyTwoWeekLow": "fiftyTwoWeekLow",
    "trailingPE": "trailingPE",
    "forwardPE": "forwardPE",
    "dividendYield": "dividendYield",
    "sector": "sector",
    "industry": "industry",
    "exchange": "exchange",
    "quoteType": "quoteType",
}

# Available sectors (from Yahoo Finance)
AVAILABLE_SECTORS = [
    "Technology",
    "Healthcare",
    "Financial Services",
    "Consumer Cyclical",
    "Industrials",
    "Communication Services",
    "Consumer Defensive",
    "Energy",
    "Real Estate",
    "Basic Materials",
    "Utilities",
]

# Available regions (from Yahoo Finance)
AVAILABLE_REGIONS = [
    "us",  # United States
    "eu",  # Europe
    "asia",  # Asia
    "au",  # Australia
    "ca",  # Canada
    "gb",  # United Kingdom
]

# Sort fields
SORT_FIELD_TICKER = "ticker"
SORT_FIELD_PRICE = "intradayprice"
SORT_FIELD_MARKET_CAP = "marketcap"
SORT_FIELD_VOLUME = "volume"
SORT_FIELD_PE_RATIO = "peratio"

# Sort orders
SORT_ORDER_ASC = "asc"
SORT_ORDER_DESC = "desc"

# Cache configuration
DEFAULT_CACHE_DIR = "~/.yfinance_screener/cache"
DEFAULT_CACHE_TTL = 3600  # 1 hour in seconds

# Browser configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
