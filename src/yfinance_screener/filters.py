"""
Filter definitions and validation for Yahoo Finance screener.

This module provides filter definitions, validation logic, and the filter
registry for all supported Yahoo Finance screener filters.

The module includes:
- FilterType enum for categorizing filter types
- FilterDefinition dataclass for defining filter properties
- FILTERS registry with all available filters
- FilterValidator class for validating filter values

Example:
    Accessing filter definitions::

        from yfinance_screener.filters import FILTERS, FilterValidator

        # Get filter definition
        price_filter = FILTERS['price']
        print(price_filter.description)

        # Validate a filter value
        FilterValidator.validate('price', 50.0)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

from .constants import (
    AVAILABLE_REGIONS,
    AVAILABLE_SECTORS,
    FIELD_DIVIDEND_YIELD,
    FIELD_EARNINGS_GROWTH,
    FIELD_EXCHANGE,
    FIELD_INDUSTRY,
    FIELD_MARKET_CAP,
    FIELD_PB_RATIO,
    FIELD_PE_RATIO,
    FIELD_PEG_RATIO,
    FIELD_PRICE,
    FIELD_PROFIT_MARGIN,
    FIELD_REGION,
    FIELD_REVENUE_GROWTH,
    FIELD_ROA,
    FIELD_ROE,
    FIELD_SECTOR,
    FIELD_VOLUME,
)
from .exceptions import ValidationError


class FilterType(Enum):
    """Types of filters supported by the screener."""

    NUMERIC_RANGE = "numeric_range"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"


@dataclass
class FilterDefinition:
    """Definition of a screener filter with validation rules."""

    name: str
    field: str  # Yahoo Finance API field name
    type: FilterType
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[str]] = None
    description: str = ""


# Filter registry with all supported filters
FILTERS = {
    "price": FilterDefinition(
        name="price",
        field=FIELD_PRICE,
        type=FilterType.NUMERIC_RANGE,
        min_value=0.01,
        description="Stock price in dollars",
    ),
    "market_cap": FilterDefinition(
        name="market_cap",
        field=FIELD_MARKET_CAP,
        type=FilterType.NUMERIC_RANGE,
        min_value=0,
        description="Market capitalization in dollars",
    ),
    "volume": FilterDefinition(
        name="volume",
        field=FIELD_VOLUME,
        type=FilterType.NUMERIC_RANGE,
        min_value=0,
        description="Trading volume (number of shares)",
    ),
    "pe_ratio": FilterDefinition(
        name="pe_ratio",
        field=FIELD_PE_RATIO,
        type=FilterType.NUMERIC_RANGE,
        description="Price-to-earnings ratio",
    ),
    "pb_ratio": FilterDefinition(
        name="pb_ratio",
        field=FIELD_PB_RATIO,
        type=FilterType.NUMERIC_RANGE,
        min_value=0,
        description="Price-to-book ratio",
    ),
    "peg_ratio": FilterDefinition(
        name="peg_ratio",
        field=FIELD_PEG_RATIO,
        type=FilterType.NUMERIC_RANGE,
        description="Price/earnings to growth ratio",
    ),
    "dividend_yield": FilterDefinition(
        name="dividend_yield",
        field=FIELD_DIVIDEND_YIELD,
        type=FilterType.NUMERIC_RANGE,
        min_value=0,
        max_value=100,
        description="Dividend yield percentage",
    ),
    "revenue_growth": FilterDefinition(
        name="revenue_growth",
        field=FIELD_REVENUE_GROWTH,
        type=FilterType.NUMERIC_RANGE,
        description="Revenue growth rate percentage",
    ),
    "earnings_growth": FilterDefinition(
        name="earnings_growth",
        field=FIELD_EARNINGS_GROWTH,
        type=FilterType.NUMERIC_RANGE,
        description="Earnings growth rate percentage",
    ),
    "profit_margin": FilterDefinition(
        name="profit_margin",
        field=FIELD_PROFIT_MARGIN,
        type=FilterType.NUMERIC_RANGE,
        min_value=0,
        max_value=100,
        description="Profit margin percentage",
    ),
    "roe": FilterDefinition(
        name="roe",
        field=FIELD_ROE,
        type=FilterType.NUMERIC_RANGE,
        description="Return on equity percentage",
    ),
    "roa": FilterDefinition(
        name="roa",
        field=FIELD_ROA,
        type=FilterType.NUMERIC_RANGE,
        description="Return on assets percentage",
    ),
    "sector": FilterDefinition(
        name="sector",
        field=FIELD_SECTOR,
        type=FilterType.CATEGORICAL,
        allowed_values=AVAILABLE_SECTORS,
        description="Business sector",
    ),
    "industry": FilterDefinition(
        name="industry",
        field=FIELD_INDUSTRY,
        type=FilterType.CATEGORICAL,
        allowed_values=None,  # Too many industries to enumerate
        description="Business industry",
    ),
    "region": FilterDefinition(
        name="region",
        field=FIELD_REGION,
        type=FilterType.CATEGORICAL,
        allowed_values=AVAILABLE_REGIONS,
        description="Geographic region",
    ),
    "exchange": FilterDefinition(
        name="exchange",
        field=FIELD_EXCHANGE,
        type=FilterType.CATEGORICAL,
        allowed_values=None,  # Many exchanges available
        description="Stock exchange",
    ),
}


class FilterValidator:
    """Validates filter values against filter definitions."""

    @staticmethod
    def validate(filter_name: str, value: Any) -> None:
        """
        Validate a filter value against its definition.

        Args:
            filter_name: Name of the filter to validate
            value: Value to validate

        Raises:
            ValidationError: If the filter name is unknown or value is invalid
        """
        # Check if filter exists
        if filter_name not in FILTERS:
            raise ValidationError(
                f"Unknown filter: '{filter_name}'. "
                f"Available filters: {', '.join(FILTERS.keys())}"
            )

        filter_def = FILTERS[filter_name]

        # Validate based on filter type
        if filter_def.type == FilterType.NUMERIC_RANGE:
            FilterValidator._validate_numeric(filter_name, value, filter_def)
        elif filter_def.type == FilterType.CATEGORICAL:
            FilterValidator._validate_categorical(filter_name, value, filter_def)
        elif filter_def.type == FilterType.BOOLEAN:
            FilterValidator._validate_boolean(filter_name, value, filter_def)

    @staticmethod
    def _validate_numeric(filter_name: str, value: Any, filter_def: FilterDefinition) -> None:
        """
        Validate a numeric filter value.

        Args:
            filter_name: Name of the filter
            value: Value to validate
            filter_def: Filter definition

        Raises:
            ValidationError: If value is invalid
        """
        # Check type
        if not isinstance(value, (int, float)):
            raise ValidationError(
                f"Filter '{filter_name}' expects a numeric value, " f"got {type(value).__name__}"
            )

        # Check minimum value
        if filter_def.min_value is not None and value < filter_def.min_value:
            raise ValidationError(
                f"Filter '{filter_name}' value {value} is below minimum "
                f"allowed value {filter_def.min_value}"
            )

        # Check maximum value
        if filter_def.max_value is not None and value > filter_def.max_value:
            raise ValidationError(
                f"Filter '{filter_name}' value {value} exceeds maximum "
                f"allowed value {filter_def.max_value}"
            )

    @staticmethod
    def _validate_categorical(filter_name: str, value: Any, filter_def: FilterDefinition) -> None:
        """
        Validate a categorical filter value.

        Args:
            filter_name: Name of the filter
            value: Value to validate (can be single value or list)
            filter_def: Filter definition

        Raises:
            ValidationError: If value is invalid
        """
        # Convert single value to list for uniform processing
        values = [value] if not isinstance(value, list) else value

        # Check that we have at least one value
        if not values:
            raise ValidationError(f"Filter '{filter_name}' requires at least one value")

        # Check type of each value
        for val in values:
            if not isinstance(val, str):
                raise ValidationError(
                    f"Filter '{filter_name}' expects string values, " f"got {type(val).__name__}"
                )

        # Check against allowed values if specified
        if filter_def.allowed_values is not None:
            for val in values:
                if val not in filter_def.allowed_values:
                    raise ValidationError(
                        f"Filter '{filter_name}' value '{val}' is not valid. "
                        f"Allowed values: {', '.join(filter_def.allowed_values)}"
                    )

    @staticmethod
    def _validate_boolean(filter_name: str, value: Any, filter_def: FilterDefinition) -> None:
        """
        Validate a boolean filter value.

        Args:
            filter_name: Name of the filter
            value: Value to validate
            filter_def: Filter definition

        Raises:
            ValidationError: If value is invalid
        """
        if not isinstance(value, bool):
            raise ValidationError(
                f"Filter '{filter_name}' expects a boolean value, " f"got {type(value).__name__}"
            )

    @staticmethod
    def validate_range(
        filter_name: str, min_value: Optional[float], max_value: Optional[float]
    ) -> None:
        """
        Validate a range filter (min/max pair).

        Args:
            filter_name: Name of the filter
            min_value: Minimum value (optional)
            max_value: Maximum value (optional)

        Raises:
            ValidationError: If range is invalid
        """
        # Check if filter exists
        if filter_name not in FILTERS:
            raise ValidationError(
                f"Unknown filter: '{filter_name}'. "
                f"Available filters: {', '.join(FILTERS.keys())}"
            )

        filter_def = FILTERS[filter_name]

        # Check that filter supports ranges
        if filter_def.type != FilterType.NUMERIC_RANGE:
            raise ValidationError(f"Filter '{filter_name}' does not support range queries")

        # Validate individual values
        if min_value is not None:
            FilterValidator._validate_numeric(filter_name, min_value, filter_def)

        if max_value is not None:
            FilterValidator._validate_numeric(filter_name, max_value, filter_def)

        # Check that min <= max
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValidationError(
                f"Filter '{filter_name}' minimum value {min_value} "
                f"cannot be greater than maximum value {max_value}"
            )
