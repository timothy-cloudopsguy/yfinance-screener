"""
Main Screener class for Yahoo Finance stock screening.

This module provides the primary interface for screening stocks using
Yahoo Finance's screener API with complete feature parity to the web interface.

Example:
    Basic usage with simple parameters::

        from yfinance_screener import Screener

        screener = Screener()
        symbols = screener.screen(min_price=10, max_price=100)

    Advanced usage with query builder::

        results = (screener.query()
            .price(min=10, max=100)
            .sector("Technology")
            .execute(as_dataframe=True))
"""

import asyncio
from typing import Any, Dict, List, Optional, Union

try:
    import pandas as pd
    from pandas import DataFrame

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    DataFrame = Any

from .cache_manager import CacheManager
from .constants import (
    AVAILABLE_REGIONS,
    AVAILABLE_SECTORS,
    DEFAULT_PAGE_SIZE,
    SCREENER_API_URL,
    SORT_ORDER_ASC,
)
from .exceptions import NetworkError, ResponseError, ValidationError
from .query_builder import QueryBuilder
from .session_manager import SessionManager


class Screener:
    """
    Main interface for Yahoo Finance stock screening.

    Provides both simple parameter-based screening and advanced
    query builder interface with complete feature parity to the
    Yahoo Finance web screener.

    Example:
        >>> screener = Screener()
        >>> # Simple screening
        >>> symbols = screener.screen(min_price=10, max_price=100)
        >>>
        >>> # Advanced query building
        >>> results = (screener.query()
        ...     .price(min=10, max=100)
        ...     .market_cap(min=1_000_000_000)
        ...     .sector("Technology")
        ...     .execute(as_dataframe=True))
    """

    def __init__(
        self, cache_enabled: bool = True, cache_ttl: int = 3600, headless: bool = True
    ) -> None:
        """
        Initialize screener with optional configuration.

        Args:
            cache_enabled: Enable result caching (default: True)
            cache_ttl: Cache time-to-live in seconds (default: 3600 = 1 hour)
            headless: Run browser in headless mode (default: True)
        """
        self.cache_enabled = cache_enabled
        self.headless = headless

        # Initialize cache manager
        self.cache_manager = CacheManager(ttl=cache_ttl) if cache_enabled else None

        # Session manager will be created on demand
        self._session_manager: Optional[SessionManager] = None

    def screen(
        self,
        *,
        # Price filters
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        # Market cap filters
        min_market_cap: Optional[float] = None,
        max_market_cap: Optional[float] = None,
        # Volume filters
        min_volume: Optional[int] = None,
        max_volume: Optional[int] = None,
        # Valuation filters
        min_pe_ratio: Optional[float] = None,
        max_pe_ratio: Optional[float] = None,
        min_pb_ratio: Optional[float] = None,
        max_pb_ratio: Optional[float] = None,
        min_peg_ratio: Optional[float] = None,
        max_peg_ratio: Optional[float] = None,
        # Dividend filters
        min_dividend_yield: Optional[float] = None,
        max_dividend_yield: Optional[float] = None,
        # Growth filters
        min_revenue_growth: Optional[float] = None,
        max_revenue_growth: Optional[float] = None,
        min_earnings_growth: Optional[float] = None,
        max_earnings_growth: Optional[float] = None,
        # Profitability filters
        min_profit_margin: Optional[float] = None,
        max_profit_margin: Optional[float] = None,
        min_roe: Optional[float] = None,
        max_roe: Optional[float] = None,
        min_roa: Optional[float] = None,
        max_roa: Optional[float] = None,
        # Categorical filters
        sectors: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
        regions: Optional[List[str]] = None,
        exchanges: Optional[List[str]] = None,
        # Result options
        max_results: Optional[int] = None,
        sort_by: str = "ticker",
        sort_order: str = SORT_ORDER_ASC,
        # Output format
        as_dataframe: bool = False,
    ) -> Union[List[str], DataFrame]:
        """
        Screen stocks with specified filters.

        All filters are optional. If no filters are specified, returns all stocks.
        Multiple filters are combined with AND logic.

        Args:
            min_price: Minimum stock price in dollars
            max_price: Maximum stock price in dollars
            min_market_cap: Minimum market capitalization in dollars
            max_market_cap: Maximum market capitalization in dollars
            min_volume: Minimum trading volume
            max_volume: Maximum trading volume
            min_pe_ratio: Minimum price-to-earnings ratio
            max_pe_ratio: Maximum price-to-earnings ratio
            min_pb_ratio: Minimum price-to-book ratio
            max_pb_ratio: Maximum price-to-book ratio
            min_peg_ratio: Minimum PEG ratio
            max_peg_ratio: Maximum PEG ratio
            min_dividend_yield: Minimum dividend yield percentage
            max_dividend_yield: Maximum dividend yield percentage
            min_revenue_growth: Minimum revenue growth percentage
            max_revenue_growth: Maximum revenue growth percentage
            min_earnings_growth: Minimum earnings growth percentage
            max_earnings_growth: Maximum earnings growth percentage
            min_profit_margin: Minimum profit margin percentage
            max_profit_margin: Maximum profit margin percentage
            min_roe: Minimum return on equity percentage
            max_roe: Maximum return on equity percentage
            min_roa: Minimum return on assets percentage
            max_roa: Maximum return on assets percentage
            sectors: List of sectors to include (OR logic)
            industries: List of industries to include (OR logic)
            regions: List of regions to include (OR logic). Defaults to ["us"] if not specified.
                     Pass an empty list [] to search all regions.
            exchanges: List of exchanges to include (OR logic)
            max_results: Maximum number of results to return
            sort_by: Field to sort by (default: "ticker")
            sort_order: Sort order "asc" or "desc" (default: "asc")
            as_dataframe: Return pandas DataFrame instead of symbol list

        Returns:
            List of ticker symbols or pandas DataFrame with detailed data

        Raises:
            ValidationError: If filter parameters are invalid
            AuthenticationError: If Yahoo Finance authentication fails
            NetworkError: If network communication fails
            ResponseError: If API response is unexpected
        """
        # Build query using QueryBuilder
        builder = QueryBuilder()

        # Add filters to builder
        if min_price is not None or max_price is not None:
            builder.price(min=min_price, max=max_price)

        if min_market_cap is not None or max_market_cap is not None:
            builder.market_cap(min=min_market_cap, max=max_market_cap)

        if min_volume is not None or max_volume is not None:
            builder.volume(min=min_volume, max=max_volume)

        if min_pe_ratio is not None or max_pe_ratio is not None:
            builder.pe_ratio(min=min_pe_ratio, max=max_pe_ratio)

        if min_pb_ratio is not None or max_pb_ratio is not None:
            builder.pb_ratio(min=min_pb_ratio, max=max_pb_ratio)

        if min_peg_ratio is not None or max_peg_ratio is not None:
            builder.peg_ratio(min=min_peg_ratio, max=max_peg_ratio)

        if min_dividend_yield is not None or max_dividend_yield is not None:
            builder.dividend_yield(min=min_dividend_yield, max=max_dividend_yield)

        if min_revenue_growth is not None or max_revenue_growth is not None:
            builder.revenue_growth(min=min_revenue_growth, max=max_revenue_growth)

        if min_earnings_growth is not None or max_earnings_growth is not None:
            builder.earnings_growth(min=min_earnings_growth, max=max_earnings_growth)

        if min_profit_margin is not None or max_profit_margin is not None:
            builder.profit_margin(min=min_profit_margin, max=max_profit_margin)

        if min_roe is not None or max_roe is not None:
            builder.roe(min=min_roe, max=max_roe)

        if min_roa is not None or max_roa is not None:
            builder.roa(min=min_roa, max=max_roa)

        if sectors:
            builder.sector(*sectors)

        if industries:
            builder.industry(*industries)

        # Default to US region if no regions specified
        if regions is None:
            builder.region("us")
        elif regions:
            builder.region(*regions)

        if exchanges:
            builder.exchange(*exchanges)

        # Set sort and limit
        builder.sort_by(sort_by, sort_order)
        if max_results:
            builder.limit(max_results)

        # Build query
        query = builder.build()

        # Execute query
        return asyncio.run(self._execute_query(query, max_results, as_dataframe))

    def query(self) -> QueryBuilder:
        """
        Get a QueryBuilder for advanced query construction.

        Returns:
            QueryBuilder instance for fluent query building

        Example:
            >>> screener = Screener()
            >>> query = (screener.query()
            ...     .price(min=10, max=100)
            ...     .market_cap(min=1_000_000_000)
            ...     .sector("Technology", "Healthcare")
            ...     .sort_by("marketcap", "desc")
            ...     .limit(50))
            >>> results = query.execute(as_dataframe=True)
        """
        # Create a QueryBuilder with a reference to this screener
        builder = QueryBuilder()
        # Store reference to screener for execute() method
        builder._screener = self
        return builder

    def get_available_sectors(self) -> List[str]:
        """
        Get list of available sector values.

        Returns:
            List of sector names that can be used in sector filter
        """
        return AVAILABLE_SECTORS.copy()

    def get_available_industries(self) -> List[str]:
        """
        Get list of available industry values.

        Note: Yahoo Finance has hundreds of industries. This method
        returns a representative sample. Any industry string can be
        used in the industry filter.

        Returns:
            List of common industry names
        """
        # Return a representative sample of common industries
        return [
            "Software—Application",
            "Software—Infrastructure",
            "Semiconductors",
            "Internet Content & Information",
            "Electronic Components",
            "Computer Hardware",
            "Biotechnology",
            "Drug Manufacturers—General",
            "Medical Devices",
            "Banks—Regional",
            "Banks—Diversified",
            "Insurance—Life",
            "Asset Management",
            "Auto Manufacturers",
            "Aerospace & Defense",
            "Oil & Gas E&P",
            "Utilities—Regulated Electric",
            "Real Estate—Diversified",
            "Retail—Cyclical",
            "Consumer Electronics",
        ]

    def get_available_regions(self) -> List[str]:
        """
        Get list of available region values.

        Returns:
            List of region codes that can be used in region filter
        """
        return AVAILABLE_REGIONS.copy()

    async def _execute_query(
        self, query: Dict[str, Any], max_results: Optional[int], as_dataframe: bool
    ) -> Union[List[str], DataFrame]:
        """
        Execute a query and return results.

        Args:
            query: Query dictionary from QueryBuilder
            max_results: Optional limit on total results
            as_dataframe: Return DataFrame instead of symbol list

        Returns:
            List of symbols or DataFrame
        """
        # Check cache first
        if self.cache_enabled and self.cache_manager:
            query_hash = CacheManager.hash_query(query)
            cached_results = self.cache_manager.get(query_hash)

            if cached_results is not None:
                # Apply max_results limit to cached data
                if max_results:
                    cached_results = cached_results[:max_results]

                # Transform and return
                return self._transform_results(cached_results, as_dataframe)

        # Fetch from API
        results = await self._fetch_from_api(query, max_results)

        # Cache results
        if self.cache_enabled and self.cache_manager:
            query_hash = CacheManager.hash_query(query)
            self.cache_manager.set(query_hash, results)

        # Transform and return
        return self._transform_results(results, as_dataframe)

    async def _fetch_from_api(
        self, query: Dict[str, Any], max_results: Optional[int]
    ) -> List[Dict[str, Any]]:
        """
        Fetch results from Yahoo Finance API with pagination.

        Args:
            query: Query dictionary
            max_results: Optional limit on total results

        Returns:
            List of stock dictionaries
        """
        # Get or create session
        if not self._session_manager:
            self._session_manager = SessionManager(headless=self.headless)

        try:
            page, crumb, cookies = await self._session_manager.get_session()

            # Fetch results with pagination
            all_results = []
            offset = 0
            page_size = DEFAULT_PAGE_SIZE

            while True:
                # Update query with current offset
                current_query = query.copy()
                current_query["offset"] = offset
                current_query["size"] = page_size

                # Fetch page
                page_results = await self._fetch_page(current_query, crumb, cookies)

                if not page_results:
                    break

                all_results.extend(page_results)

                # Check if we've reached the limit
                if max_results and len(all_results) >= max_results:
                    all_results = all_results[:max_results]
                    break

                # Check if there are more results
                if len(page_results) < page_size:
                    break

                offset += page_size

            return all_results

        finally:
            # Clean up session
            if self._session_manager:
                await self._session_manager.close()
                self._session_manager = None

    async def _fetch_page(
        self, query: Dict[str, Any], crumb: str, cookies: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        Fetch a single page of results from Yahoo Finance API.

        Args:
            query: Query dictionary with offset and size
            crumb: CSRF token
            cookies: Session cookies

        Returns:
            List of stock dictionaries for this page
        """
        import aiohttp

        # Prepare request
        url = f"{SCREENER_API_URL}?crumb={crumb}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession(cookies=cookies) as session, session.post(
                url, json=query, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 429:
                    # Rate limited
                    from .exceptions import RateLimitError

                    retry_after = response.headers.get("Retry-After")
                    raise RateLimitError(retry_after=int(retry_after) if retry_after else None)

                if response.status != 200:
                    raise NetworkError(f"API request failed with status {response.status}")

                data = await response.json()

                # Parse response
                try:
                    finance = data.get("finance", {})
                    result = finance.get("result", [])

                    if not result:
                        return []

                    quotes: List[Dict[str, Any]] = result[0].get("quotes", [])
                    return quotes

                except (KeyError, IndexError, TypeError) as e:
                    raise ResponseError(f"Unexpected API response format: {e}") from e

        except aiohttp.ClientError as e:
            raise NetworkError(f"Network error: {e}") from e

    def _transform_results(
        self, quotes: List[Dict[str, Any]], as_dataframe: bool
    ) -> Union[List[str], DataFrame]:
        """
        Transform API results to desired output format.

        Args:
            quotes: List of stock dictionaries from API
            as_dataframe: Return DataFrame instead of symbol list

        Returns:
            List of symbols or DataFrame
        """
        if not quotes:
            return pd.DataFrame() if (as_dataframe and HAS_PANDAS) else []

        if as_dataframe:
            if not HAS_PANDAS:
                raise ValidationError(
                    "pandas is required for DataFrame output. " "Install with: pip install pandas"
                )

            return self._to_dataframe(quotes)
        else:
            return self._to_symbol_list(quotes)

    def _to_symbol_list(self, quotes: List[Dict[str, Any]]) -> List[str]:
        """
        Extract ticker symbols from quotes.

        Args:
            quotes: List of stock dictionaries

        Returns:
            List of ticker symbols
        """
        return [quote.get("symbol", "") for quote in quotes if quote.get("symbol")]

    def _to_dataframe(self, quotes: List[Dict[str, Any]]) -> DataFrame:
        """
        Convert quotes to pandas DataFrame with yfinance-compatible columns.

        Args:
            quotes: List of stock dictionaries

        Returns:
            pandas DataFrame
        """
        if not HAS_PANDAS:
            raise ValidationError("pandas is not installed")

        # Normalize field names to be more user-friendly
        normalized_quotes = []
        for quote in quotes:
            normalized = {
                "symbol": quote.get("symbol", ""),
                "name": quote.get("longName") or quote.get("shortName", ""),
                "price": quote.get("regularMarketPrice"),
                "marketCap": quote.get("marketCap"),
                "volume": quote.get("volume"),
                "avgVolume": quote.get("averageVolume"),
                "pe": quote.get("trailingPE"),
                "forwardPE": quote.get("forwardPE"),
                "dividendYield": quote.get("dividendYield"),
                "sector": quote.get("sector"),
                "industry": quote.get("industry"),
                "exchange": quote.get("exchange"),
                "52WeekHigh": quote.get("fiftyTwoWeekHigh"),
                "52WeekLow": quote.get("fiftyTwoWeekLow"),
            }
            normalized_quotes.append(normalized)

        return pd.DataFrame(normalized_quotes)
