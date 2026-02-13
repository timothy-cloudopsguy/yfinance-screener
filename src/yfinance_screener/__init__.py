"""
yfinance-screener: Yahoo Finance stock screener with complete feature parity.

A Python package providing programmatic access to Yahoo Finance's stock screener
functionality with a clean, yfinance-compatible API.

Basic Usage:
    Simple screening for stocks::

        from yfinance_screener import Screener

        screener = Screener()
        symbols = screener.screen(
            min_price=10,
            max_price=100,
            min_market_cap=1_000_000_000,
            max_results=50
        )

    Advanced query building::

        results = (screener.query()
            .price(min=10, max=100)
            .market_cap(min=1_000_000_000)
            .sector("Technology", "Healthcare")
            .sort_by("marketcap", "desc")
            .limit(50)
            .execute(as_dataframe=True))

Main Classes:
    - Screener: Main interface for stock screening
    - QueryBuilder: Fluent interface for building complex queries
    - YFinanceScreenerFetcher: Legacy compatibility class (deprecated)

Exceptions:
    - YFinanceScreenerError: Base exception
    - ValidationError: Invalid filter parameters
    - AuthenticationError: Yahoo Finance authentication failure
    - NetworkError: Network communication failure
    - RateLimitError: Rate limit exceeded
    - BrowserError: Browser automation failure
    - ResponseError: Unexpected API response

For more information, see the documentation at:
https://github.com/yourusername/yfinance-screener
"""

__version__ = "1.0.0"

# Import exceptions for easy access
from .exceptions import (
    AuthenticationError,
    BrowserError,
    NetworkError,
    RateLimitError,
    ResponseError,
    ValidationError,
    YFinanceScreenerError,
)
from .legacy import YFinanceScreenerFetcher
from .query_builder import QueryBuilder

# Main classes
from .screener import Screener
from .data_transformer import DataTransformer

__all__ = [
    # Version
    "__version__",
    # Exceptions
    "YFinanceScreenerError",
    "AuthenticationError",
    "RateLimitError",
    "NetworkError",
    "ValidationError",
    "BrowserError",
    "ResponseError",
    # Main classes
    "Screener",
    "QueryBuilder",
    "YFinanceScreenerFetcher",
    "DataTransformer",
]
