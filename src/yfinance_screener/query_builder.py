"""
Query builder for Yahoo Finance screener with fluent interface.

This module provides the QueryBuilder class for constructing complex
screening queries using a fluent, chainable API.

Example:
    Building a complex query::

        from yfinance_screener import Screener

        screener = Screener()
        results = (screener.query()
            .price(min=10, max=100)
            .market_cap(min=1_000_000_000)
            .pe_ratio(max=25)
            .sector("Technology", "Healthcare")
            .sort_by("marketcap", "desc")
            .limit(50)
            .execute(as_dataframe=True))
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from pandas import DataFrame
else:
    DataFrame = Any  # type: ignore[misc, assignment]

from .constants import (
    OPERATOR_AND,
    OPERATOR_BTWN,
    OPERATOR_EQ,
    OPERATOR_GTE,
    OPERATOR_LTE,
    OPERATOR_OR,
    SORT_ORDER_ASC,
    SORT_ORDER_DESC,
)
from .exceptions import ValidationError
from .filters import FILTERS, FilterValidator


class QueryBuilder:
    """
    Fluent interface for building complex screening queries.

    Supports method chaining and logical operators for constructing
    Yahoo Finance screener queries.

    Example:
        >>> builder = QueryBuilder()
        >>> query = (builder
        ...     .price(min=10, max=100)
        ...     .market_cap(min=1_000_000_000)
        ...     .sector("Technology", "Healthcare")
        ...     .sort_by("marketcap", "desc")
        ...     .limit(50)
        ...     .build())
    """

    def __init__(self) -> None:
        """Initialize query builder with empty operands."""
        self._operands: List[Dict[str, Any]] = []
        self._sort_field: str = "ticker"
        self._sort_order: str = SORT_ORDER_ASC
        self._max_results: Optional[int] = None
        self._screener: Optional[Any] = None  # Reference to Screener instance

    def price(self, min: Optional[float] = None, max: Optional[float] = None) -> "QueryBuilder":
        """
        Add price range filter.

        Args:
            min: Minimum price in dollars
            max: Maximum price in dollars

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("price", min, max)

    def market_cap(
        self, min: Optional[float] = None, max: Optional[float] = None
    ) -> "QueryBuilder":
        """
        Add market capitalization filter.

        Args:
            min: Minimum market cap in dollars
            max: Maximum market cap in dollars

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("market_cap", min, max)

    def volume(self, min: Optional[int] = None, max: Optional[int] = None) -> "QueryBuilder":
        """
        Add trading volume filter.

        Args:
            min: Minimum volume
            max: Maximum volume

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("volume", min, max)

    def pe_ratio(self, min: Optional[float] = None, max: Optional[float] = None) -> "QueryBuilder":
        """
        Add price-to-earnings ratio filter.

        Args:
            min: Minimum P/E ratio
            max: Maximum P/E ratio

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("pe_ratio", min, max)

    def pb_ratio(self, min: Optional[float] = None, max: Optional[float] = None) -> "QueryBuilder":
        """
        Add price-to-book ratio filter.

        Args:
            min: Minimum P/B ratio
            max: Maximum P/B ratio

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("pb_ratio", min, max)

    def peg_ratio(self, min: Optional[float] = None, max: Optional[float] = None) -> "QueryBuilder":
        """
        Add PEG ratio filter.

        Args:
            min: Minimum PEG ratio
            max: Maximum PEG ratio

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("peg_ratio", min, max)

    def dividend_yield(
        self, min: Optional[float] = None, max: Optional[float] = None
    ) -> "QueryBuilder":
        """
        Add dividend yield filter.

        Args:
            min: Minimum dividend yield percentage
            max: Maximum dividend yield percentage

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("dividend_yield", min, max)

    def revenue_growth(
        self, min: Optional[float] = None, max: Optional[float] = None
    ) -> "QueryBuilder":
        """
        Add revenue growth filter.

        Args:
            min: Minimum revenue growth percentage
            max: Maximum revenue growth percentage

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("revenue_growth", min, max)

    def earnings_growth(
        self, min: Optional[float] = None, max: Optional[float] = None
    ) -> "QueryBuilder":
        """
        Add earnings growth filter.

        Args:
            min: Minimum earnings growth percentage
            max: Maximum earnings growth percentage

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("earnings_growth", min, max)

    def profit_margin(
        self, min: Optional[float] = None, max: Optional[float] = None
    ) -> "QueryBuilder":
        """
        Add profit margin filter.

        Args:
            min: Minimum profit margin percentage
            max: Maximum profit margin percentage

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("profit_margin", min, max)

    def roe(self, min: Optional[float] = None, max: Optional[float] = None) -> "QueryBuilder":
        """
        Add return on equity filter.

        Args:
            min: Minimum ROE percentage
            max: Maximum ROE percentage

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("roe", min, max)

    def roa(self, min: Optional[float] = None, max: Optional[float] = None) -> "QueryBuilder":
        """
        Add return on assets filter.

        Args:
            min: Minimum ROA percentage
            max: Maximum ROA percentage

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        return self._add_range_filter("roa", min, max)

    def sector(self, *sectors: str) -> "QueryBuilder":
        """
        Add sector filter (OR logic for multiple sectors).

        Args:
            *sectors: One or more sector names

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If sector values are invalid
        """
        return self._add_categorical_filter("sector", list(sectors))

    def industry(self, *industries: str) -> "QueryBuilder":
        """
        Add industry filter (OR logic for multiple industries).

        Args:
            *industries: One or more industry names

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If industry values are invalid
        """
        return self._add_categorical_filter("industry", list(industries))

    def region(self, *regions: str) -> "QueryBuilder":
        """
        Add region filter (OR logic for multiple regions).

        Args:
            *regions: One or more region codes (e.g., 'us', 'eu', 'asia')

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If region values are invalid
        """
        return self._add_categorical_filter("region", list(regions))

    def exchange(self, *exchanges: str) -> "QueryBuilder":
        """
        Add exchange filter (OR logic for multiple exchanges).

        Args:
            *exchanges: One or more exchange codes

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If exchange values are invalid
        """
        return self._add_categorical_filter("exchange", list(exchanges))

    def sort_by(self, field: str, order: str = SORT_ORDER_ASC) -> "QueryBuilder":
        """
        Set sort field and order.

        Args:
            field: Field to sort by (e.g., 'ticker', 'price', 'marketcap')
            order: Sort order ('asc' or 'desc')

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If sort order is invalid
        """
        if order not in (SORT_ORDER_ASC, SORT_ORDER_DESC):
            raise ValidationError(f"Invalid sort order '{order}'. Must be 'asc' or 'desc'")

        self._sort_field = field
        self._sort_order = order
        return self

    def limit(self, max_results: int) -> "QueryBuilder":
        """
        Limit number of results.

        Args:
            max_results: Maximum number of results to return

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If max_results is invalid
        """
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValidationError(f"max_results must be a positive integer, got {max_results}")

        self._max_results = max_results
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build and return the query dictionary.

        Validates the query and generates the Yahoo Finance API query structure.

        Returns:
            Query dictionary ready for API submission

        Raises:
            ValidationError: If query is invalid
        """
        # Validate that we have at least one filter
        if not self._operands:
            raise ValidationError(
                "Query must have at least one filter. "
                "Use methods like price(), market_cap(), sector(), etc."
            )

        # Build the query structure
        query: Dict[str, Any] = {
            "size": 250,  # Results per page (will be handled by API client)
            "offset": 0,  # Starting offset (will be handled by API client)
            "sortField": self._sort_field,
            "sortType": self._sort_order,
            "quoteType": "EQUITY",
            "userId": "",
            "userIdType": "guid",
        }

        # Add query operands
        if len(self._operands) == 1:
            # Single filter - no need for AND wrapper
            query["query"] = self._operands[0]
        else:
            # Multiple filters - wrap in AND operator
            query["query"] = {"operator": OPERATOR_AND, "operands": self._operands}

        return query

    def execute(self, as_dataframe: bool = False) -> Union[List[str], DataFrame]:
        """
        Execute the query and return results.

        Args:
            as_dataframe: If True, return pandas DataFrame; otherwise list of symbols

        Returns:
            List of ticker symbols or DataFrame with detailed data

        Raises:
            RuntimeError: If QueryBuilder is not associated with a Screener instance
        """
        if not self._screener:
            raise RuntimeError(
                "QueryBuilder must be created via Screener.query() to use execute(). "
                "Alternatively, use build() to get the query dictionary."
            )

        # Build the query
        query = self.build()

        # Execute via screener
        import asyncio

        return asyncio.run(self._screener._execute_query(query, self._max_results, as_dataframe))

    def _add_range_filter(
        self, filter_name: str, min_value: Optional[float], max_value: Optional[float]
    ) -> "QueryBuilder":
        """
        Add a numeric range filter to the query.

        Args:
            filter_name: Name of the filter
            min_value: Minimum value (optional)
            max_value: Maximum value (optional)

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        # Validate the range
        FilterValidator.validate_range(filter_name, min_value, max_value)

        # Get filter definition
        filter_def = FILTERS[filter_name]
        field = filter_def.field

        # Add operands based on what's specified
        if min_value is not None and max_value is not None:
            # Both min and max specified - use BTWN operator
            self._operands.append(
                {"operator": OPERATOR_BTWN, "operands": [field, min_value, max_value]}
            )
        elif min_value is not None:
            # Only min specified - use GTE operator
            self._operands.append({"operator": OPERATOR_GTE, "operands": [field, min_value]})
        elif max_value is not None:
            # Only max specified - use LTE operator
            self._operands.append({"operator": OPERATOR_LTE, "operands": [field, max_value]})
        else:
            # Neither specified - this is a no-op, but we'll allow it
            pass

        return self

    def _add_categorical_filter(self, filter_name: str, values: List[str]) -> "QueryBuilder":
        """
        Add a categorical filter to the query.

        Uses OR logic when multiple values are specified.

        Args:
            filter_name: Name of the filter
            values: List of values to filter by

        Returns:
            Self for method chaining

        Raises:
            ValidationError: If values are invalid
        """
        # Validate the values
        FilterValidator.validate(filter_name, values)

        # Get filter definition
        filter_def = FILTERS[filter_name]
        field = filter_def.field

        if len(values) == 1:
            # Single value - use EQ operator
            self._operands.append({"operator": OPERATOR_EQ, "operands": [field, values[0]]})
        else:
            # Multiple values - use OR operator with EQ for each value
            or_operands = [
                {"operator": OPERATOR_EQ, "operands": [field, value]} for value in values
            ]
            self._operands.append({"operator": OPERATOR_OR, "operands": or_operands})

        return self
