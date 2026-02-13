"""
Data transformation utilities for yfinance-screener.

This module provides the DataTransformer class for converting Yahoo Finance
API responses into various output formats including:
- Symbol lists (List[str])
- Pandas DataFrames with yfinance-compatible column names
- yfinance Ticker.info compatible dictionaries

The transformer ensures data compatibility with the yfinance library ecosystem
and provides consistent field naming conventions.

Example:
    Transform API response to DataFrame::

        from yfinance_screener.data_transformer import DataTransformer

        quotes = [
            {"symbol": "AAPL", "regularMarketPrice": 175.43, ...},
            {"symbol": "MSFT", "regularMarketPrice": 378.91, ...}
        ]
        
        df = DataTransformer.to_dataframe(quotes)
        symbols = DataTransformer.to_symbol_list(quotes)
"""

from typing import Any, Dict, List, Optional

import pandas as pd

from .constants import YFINANCE_FIELD_MAPPINGS


class DataTransformer:
    """
    Transforms Yahoo Finance API responses into various output formats.

    This class provides static methods for converting raw API responses
    into user-friendly formats compatible with the yfinance library.
    All methods are stateless and can be called without instantiation.
    """

    @staticmethod
    def to_symbol_list(quotes: List[Dict[str, Any]]) -> List[str]:
        """
        Extract ticker symbols from quotes.

        Args:
            quotes: List of quote dictionaries from Yahoo Finance API

        Returns:
            List of ticker symbols as strings

        Example:
            >>> quotes = [{"symbol": "AAPL"}, {"symbol": "MSFT"}]
            >>> DataTransformer.to_symbol_list(quotes)
            ['AAPL', 'MSFT']
        """
        return [quote.get("symbol", "") for quote in quotes if quote.get("symbol")]

    @staticmethod
    def to_dataframe(quotes: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert quotes to pandas DataFrame with yfinance-compatible columns.

        Transforms Yahoo Finance API response data into a pandas DataFrame
        with normalized column names matching yfinance conventions. Handles
        missing fields gracefully by filling with None/NaN values.

        Args:
            quotes: List of quote dictionaries from Yahoo Finance API

        Returns:
            DataFrame with columns: symbol, longName, currentPrice, marketCap,
            volume, averageVolume, fiftyTwoWeekHigh, fiftyTwoWeekLow,
            trailingPE, forwardPE, dividendYield, sector, industry, exchange

        Example:
            >>> quotes = [
            ...     {
            ...         "symbol": "AAPL",
            ...         "longName": "Apple Inc.",
            ...         "regularMarketPrice": 175.43,
            ...         "marketCap": 2750000000000
            ...     }
            ... ]
            >>> df = DataTransformer.to_dataframe(quotes)
            >>> df.columns.tolist()
            ['symbol', 'longName', 'currentPrice', 'marketCap', ...]
        """
        if not quotes:
            # Return empty DataFrame with expected columns
            return pd.DataFrame(
                columns=[
                    "symbol",
                    "longName",
                    "shortName",
                    "currentPrice",
                    "marketCap",
                    "volume",
                    "averageVolume",
                    "fiftyTwoWeekHigh",
                    "fiftyTwoWeekLow",
                    "trailingPE",
                    "forwardPE",
                    "dividendYield",
                    "sector",
                    "industry",
                    "exchange",
                    "quoteType",
                ]
            )

        # Normalize each quote
        normalized_quotes = [
            DataTransformer.normalize_field_names(quote) for quote in quotes
        ]

        # Create DataFrame
        df = pd.DataFrame(normalized_quotes)

        # Ensure expected columns exist (fill missing with None)
        expected_columns = [
            "symbol",
            "longName",
            "shortName",
            "currentPrice",
            "marketCap",
            "volume",
            "averageVolume",
            "fiftyTwoWeekHigh",
            "fiftyTwoWeekLow",
            "trailingPE",
            "forwardPE",
            "dividendYield",
            "sector",
            "industry",
            "exchange",
            "quoteType",
        ]

        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        # Reorder columns to match expected order
        available_columns = [col for col in expected_columns if col in df.columns]
        df = df[available_columns]

        return df

    @staticmethod
    def to_yfinance_info(quote: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a single quote to yfinance Ticker.info format.

        Transforms a Yahoo Finance API quote dictionary into a format
        compatible with yfinance.Ticker().info, using the same field
        names and structure.

        Args:
            quote: Single quote dictionary from Yahoo Finance API

        Returns:
            Dictionary matching yfinance.Ticker().info structure

        Example:
            >>> quote = {
            ...     "symbol": "AAPL",
            ...     "regularMarketPrice": 175.43,
            ...     "marketCap": 2750000000000
            ... }
            >>> info = DataTransformer.to_yfinance_info(quote)
            >>> info['currentPrice']
            175.43
            >>> info['symbol']
            'AAPL'
        """
        return DataTransformer.normalize_field_names(quote)

    @staticmethod
    def normalize_field_names(quote: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Yahoo Finance field names to yfinance conventions.

        Maps Yahoo Finance API field names to yfinance library conventions.
        For example, 'regularMarketPrice' becomes 'currentPrice' to match
        the field name used in yfinance.Ticker().info.

        Args:
            quote: Quote dictionary with Yahoo Finance API field names

        Returns:
            Dictionary with normalized field names matching yfinance conventions

        Example:
            >>> quote = {"regularMarketPrice": 175.43, "symbol": "AAPL"}
            >>> normalized = DataTransformer.normalize_field_names(quote)
            >>> normalized['currentPrice']
            175.43
        """
        normalized = {}

        for yahoo_field, yfinance_field in YFINANCE_FIELD_MAPPINGS.items():
            if yahoo_field in quote:
                normalized[yfinance_field] = quote[yahoo_field]

        # Include any additional fields not in the mapping
        for key, value in quote.items():
            if key not in YFINANCE_FIELD_MAPPINGS and key not in normalized:
                normalized[key] = value

        return normalized

