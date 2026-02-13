"""
Legacy compatibility layer for backward compatibility.

This module provides the YFinanceScreenerFetcher class that maintains
the original API from yfinance_screener_fetcher.py for backward compatibility.

All methods delegate to the new Screener class while maintaining the
original interface and behavior.
"""

import warnings
from typing import Any, Dict, List, Optional

from .screener import Screener


class YFinanceScreenerFetcher:
    """
    Legacy interface for backward compatibility.

    This class maintains the original API from yfinance_screener_fetcher.py
    and delegates all operations to the new Screener class.

    .. deprecated:: 1.0.0
        Use :class:`Screener` instead. This class is provided for backward
        compatibility only and may be removed in a future version.

    Example:
        >>> # Legacy usage (deprecated)
        >>> fetcher = YFinanceScreenerFetcher()
        >>> symbols = fetcher.fetch_stocks(min_price=10, max_price=100)
        >>>
        >>> # New recommended usage
        >>> from yfinance_screener import Screener
        >>> screener = Screener()
        >>> symbols = screener.screen(min_price=10, max_price=100)
    """

    def __init__(self) -> None:
        """
        Initialize fetcher.

        Delegates to the new Screener class internally.

        .. deprecated:: 1.0.0
            Use :class:`Screener` instead.
        """
        self._screener = Screener()

        # Issue deprecation warning on instantiation
        warnings.warn(
            "YFinanceScreenerFetcher is deprecated and will be removed in version 2.0.0. "
            "Use the Screener class instead: "
            "from yfinance_screener import Screener; screener = Screener()",
            DeprecationWarning,
            stacklevel=2,
        )

    def fetch_stocks(
        self,
        min_price: float = 10.0,
        max_price: float = 100.0,
        min_market_cap: float = 10_000_000_000,
        max_results: Optional[int] = None,
    ) -> List[str]:
        """
        Fetch stock symbols matching the criteria.

        This is a convenience method that extracts just the symbols from the
        detailed stock data. It makes a single browser session and fetches
        only the requested number of stocks.

        .. deprecated:: 1.0.0
            Use :meth:`Screener.screen` instead.

        Args:
            min_price: Minimum stock price (default: $10)
            max_price: Maximum stock price (default: $100)
            min_market_cap: Minimum market cap in dollars (default: $10B)
            max_results: Maximum number of stocks to return (default: None = all)
                        If None, fetches all available stocks
                        Recommended: Set to a reasonable number like 100-1000 for faster results

        Returns:
            List of stock symbols (e.g., ['AAPL', 'MSFT', ...])

        Example:
            >>> # Legacy usage (deprecated)
            >>> fetcher = YFinanceScreenerFetcher()
            >>> symbols = fetcher.fetch_stocks(max_results=100)
            >>>
            >>> # New recommended usage
            >>> screener = Screener()
            >>> symbols = screener.screen(
            ...     min_price=10,
            ...     max_price=100,
            ...     min_market_cap=10_000_000_000,
            ...     max_results=100
            ... )
        """
        # Delegate to new Screener.screen() method
        return self._screener.screen(
            min_price=min_price,
            max_price=max_price,
            min_market_cap=min_market_cap,
            max_results=max_results,
            as_dataframe=False,
        )

    def fetch_stocks_detailed(
        self,
        min_price: float = 10.0,
        max_price: float = 100.0,
        min_market_cap: float = 10_000_000_000,
        max_results: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch detailed stock data matching the criteria.

        Returns full stock information including symbol, name, price, market cap,
        and other available fields from Yahoo Finance.

        .. deprecated:: 1.0.0
            Use :meth:`Screener.screen` with ``as_dataframe=True`` instead.

        Args:
            min_price: Minimum stock price (default: $10)
            max_price: Maximum stock price (default: $100)
            min_market_cap: Minimum market cap in dollars (default: $10B)
            max_results: Maximum number of stocks to return (default: None = all)
                        If None, fetches all available stocks
                        Recommended: Set to a reasonable number like 100-1000 for faster results

        Returns:
            List of stock dictionaries with full data. Each dict contains:
            - symbol: Stock ticker (e.g., 'AAPL')
            - name: Company name
            - price: Current price
            - marketCap: Market capitalization
            - And other available fields

        Example:
            >>> # Legacy usage (deprecated)
            >>> fetcher = YFinanceScreenerFetcher()
            >>> stocks = fetcher.fetch_stocks_detailed(max_results=50)
            >>>
            >>> # New recommended usage
            >>> screener = Screener()
            >>> df = screener.screen(
            ...     min_price=10,
            ...     max_price=100,
            ...     min_market_cap=10_000_000_000,
            ...     max_results=50,
            ...     as_dataframe=True
            ... )
            >>> stocks = df.to_dict('records')
        """
        # Delegate to new Screener.screen() method with DataFrame output
        result = self._screener.screen(
            min_price=min_price,
            max_price=max_price,
            min_market_cap=min_market_cap,
            max_results=max_results,
            as_dataframe=True,
        )

        # Convert DataFrame to list of dictionaries to match original interface
        # Type narrowing: we know result is DataFrame when as_dataframe=True
        if not isinstance(result, list):
            return result.to_dict("records")  # type: ignore[no-any-return]

        # This shouldn't happen, but handle it gracefully
        return []
