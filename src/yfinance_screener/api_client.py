"""
API client for Yahoo Finance screener.

This module handles communication with the Yahoo Finance screener API,
including request formatting, pagination, response parsing, and error handling.

The APIClient class manages:
- Request formatting with proper headers and credentials
- Automatic pagination to fetch all results
- Response parsing and validation
- Error handling for network and API errors

Example:
    Using APIClient directly (advanced usage)::

        from yfinance_screener.api_client import APIClient
        from yfinance_screener.session_manager import SessionManager

        async with SessionManager() as session_manager:
            client = APIClient(session_manager)
            query = {
                "size": 250,
                "offset": 0,
                "sortField": "ticker",
                "sortType": "asc",
                "quoteType": "EQUITY",
                "query": {
                    "operator": "BTWN",
                    "operands": ["intradayprice", 10, 100]
                }
            }
            results = await client.fetch_screener_results(query, max_results=50)
"""

import json
from typing import Any, Dict, List, Optional

from playwright.async_api import Page

from .constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, SCREENER_API_URL
from .exceptions import AuthenticationError, NetworkError, RateLimitError, ResponseError
from .session_manager import SessionManager


class APIClient:
    """
    Handles Yahoo Finance screener API communication.

    Manages request formatting, pagination, and response parsing.
    """

    def __init__(self, session_manager: SessionManager) -> None:
        """
        Initialize API client with session manager.

        Args:
            session_manager: SessionManager instance for authentication
        """
        self.session_manager = session_manager

    async def fetch_screener_results(
        self, query: Dict[str, Any], max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch screener results with automatic pagination.

        Automatically handles pagination to fetch all results up to max_results.
        Stops early if max_results is reached or no more results are available.

        Args:
            query: Query dictionary from QueryBuilder
            max_results: Optional limit on total results

        Returns:
            List of stock dictionaries

        Raises:
            AuthenticationError: If authentication fails
            NetworkError: If network communication fails
            RateLimitError: If rate limit is exceeded
            ResponseError: If response format is unexpected
        """
        all_quotes: List[Dict[str, Any]] = []
        offset = 0
        page_size = DEFAULT_PAGE_SIZE

        # Adjust page size if max_results is smaller
        if max_results and max_results < page_size:
            page_size = min(max_results, MAX_PAGE_SIZE)

        while True:
            # Fetch a page of results
            response = await self._fetch_page(query, offset, page_size)

            # Extract quotes from response
            quotes = response.get("quotes", [])
            if not quotes:
                # No more results
                break

            # Add quotes to results
            all_quotes.extend(quotes)

            # Check if we've reached max_results
            if max_results and len(all_quotes) >= max_results:
                # Trim to exact max_results
                all_quotes = all_quotes[:max_results]
                break

            # Check if we've fetched all available results
            total = response.get("total", 0)
            if len(all_quotes) >= total:
                break

            # Move to next page
            offset += page_size

            # Adjust page size for last page if needed
            if max_results:
                remaining = max_results - len(all_quotes)
                if remaining < page_size:
                    page_size = min(remaining, MAX_PAGE_SIZE)

        return all_quotes

    async def _fetch_page(
        self, query: Dict[str, Any], offset: int, size: int
    ) -> Dict[str, Any]:
        """
        Fetch a single page of results.

        Args:
            query: Query dictionary from QueryBuilder
            offset: Starting offset for pagination
            size: Number of results per page

        Returns:
            Response dictionary with quotes and total count

        Raises:
            AuthenticationError: If authentication fails
            NetworkError: If network communication fails
            RateLimitError: If rate limit is exceeded
            ResponseError: If response format is unexpected
        """
        # Get session with crumb and cookies
        page, crumb, cookies = await self.session_manager.get_session()

        # Update query with pagination parameters
        paginated_query = query.copy()
        paginated_query["offset"] = offset
        paginated_query["size"] = size

        # Make the API request
        try:
            response = await self._make_request(page, paginated_query, crumb, cookies)
        except AuthenticationError:
            # Try refreshing session once
            page, crumb, cookies = await self.session_manager.refresh_session()
            response = await self._make_request(page, paginated_query, crumb, cookies)

        # Parse and validate response
        return self._parse_response(response)

    async def _make_request(
        self, page: Page, query: Dict[str, Any], crumb: str, cookies: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Yahoo Finance API.

        Args:
            page: Playwright page instance
            query: Query dictionary
            crumb: CSRF crumb for authentication
            cookies: Session cookies

        Returns:
            Response dictionary

        Raises:
            AuthenticationError: If authentication fails
            NetworkError: If network communication fails
            RateLimitError: If rate limit is exceeded
        """
        # Build request URL with crumb
        url = f"{SCREENER_API_URL}?crumb={crumb}"

        # Prepare request body
        body = json.dumps(query)

        try:
            # Make POST request using playwright's page.evaluate
            # This ensures we use the same browser context with cookies
            response_text = await page.evaluate(
                """
                async ({ url, body, cookies }) => {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                        },
                        body: body,
                        credentials: 'include'
                    });
                    
                    if (!response.ok) {
                        return {
                            error: true,
                            status: response.status,
                            statusText: response.statusText,
                            text: await response.text()
                        };
                    }
                    
                    return {
                        error: false,
                        text: await response.text()
                    };
                }
                """,
                {"url": url, "body": body, "cookies": cookies},
            )

            # Check for errors
            if response_text.get("error"):
                status = response_text.get("status", 0)
                status_text = response_text.get("statusText", "Unknown error")
                error_text = response_text.get("text", "")

                if status == 401 or status == 403:
                    raise AuthenticationError(
                        f"Authentication failed: {status} {status_text}. "
                        "The crumb may have expired. Try again."
                    )
                elif status == 429:
                    raise RateLimitError(retry_after=60)
                else:
                    raise NetworkError(
                        f"API request failed: {status} {status_text}. "
                        f"Response: {error_text[:200]}"
                    )

            # Parse JSON response
            response_json = json.loads(response_text["text"])
            return response_json

        except json.JSONDecodeError as e:
            raise ResponseError(f"Failed to parse JSON response: {e}") from e
        except Exception as e:
            if isinstance(e, (AuthenticationError, NetworkError, RateLimitError, ResponseError)):
                raise
            raise NetworkError(f"Network request failed: {e}") from e

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate API response.

        Args:
            response: Raw API response dictionary

        Returns:
            Parsed response with quotes and total count

        Raises:
            ResponseError: If response format is unexpected
        """
        try:
            # Navigate response structure
            finance = response.get("finance")
            if not finance:
                raise ResponseError("Response missing 'finance' key")

            result = finance.get("result")
            if not result or not isinstance(result, list) or len(result) == 0:
                raise ResponseError("Response missing 'finance.result' array")

            result_data = result[0]

            # Extract quotes and total
            quotes = result_data.get("quotes", [])
            total = result_data.get("total", 0)

            return {"quotes": quotes, "total": total}

        except (KeyError, IndexError, TypeError) as e:
            raise ResponseError(f"Unexpected response format: {e}") from e
