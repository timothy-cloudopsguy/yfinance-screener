"""
Custom exception classes for yfinance-screener package.

This module defines all custom exceptions used throughout the package,
providing specific error types for different failure scenarios.

Exception Hierarchy:
    YFinanceScreenerError (base)
    ├── ValidationError
    ├── AuthenticationError
    ├── NetworkError
    ├── RateLimitError
    ├── BrowserError
    └── ResponseError

Example:
    Handling specific exceptions::

        from yfinance_screener import Screener
        from yfinance_screener import ValidationError, RateLimitError

        screener = Screener()
        try:
            results = screener.screen(min_price=10)
        except ValidationError as e:
            print(f"Invalid parameters: {e}")
        except RateLimitError as e:
            print(f"Rate limited. Retry after {e.retry_after}s")
"""

from typing import Optional


class YFinanceScreenerError(Exception):
    """Base exception for yfinance-screener package."""

    pass


class AuthenticationError(YFinanceScreenerError):
    """Raised when authentication with Yahoo Finance fails."""

    pass


class RateLimitError(YFinanceScreenerError):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: Optional[int] = None) -> None:
        """
        Initialize rate limit error.

        Args:
            retry_after: Seconds to wait before retrying
        """
        self.retry_after = retry_after
        message = (
            f"Rate limit exceeded. Retry after {retry_after}s"
            if retry_after
            else "Rate limit exceeded"
        )
        super().__init__(message)


class NetworkError(YFinanceScreenerError):
    """Raised when network communication fails."""

    pass


class ValidationError(YFinanceScreenerError):
    """Raised when filter validation fails."""

    pass


class BrowserError(YFinanceScreenerError):
    """Raised when browser automation fails."""

    pass


class ResponseError(YFinanceScreenerError):
    """Raised when API response format is unexpected."""

    pass
