"""
Session management for Yahoo Finance API authentication.

This module handles browser automation, session management, and authentication
with Yahoo Finance using Playwright with stealth mode to bypass bot detection.

The SessionManager class manages:
- Browser lifecycle (launch, context, page)
- CSRF crumb extraction
- Cookie management
- Session persistence and refresh

Example:
    Using SessionManager directly (advanced usage)::

        from yfinance_screener.session_manager import SessionManager

        async with SessionManager(headless=True) as manager:
            page, crumb, cookies = await manager.get_session()
            # Use session for API calls
"""

import re
from typing import Any, Dict, Optional, Tuple

from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright
from playwright_stealth import Stealth

from .constants import CRUMB_URL, USER_AGENT, YAHOO_FINANCE_URL
from .exceptions import AuthenticationError, BrowserError


class SessionManager:
    """
    Manages browser sessions and Yahoo Finance authentication.

    Handles crumb extraction, cookie management, and session lifecycle.
    Uses playwright-stealth to bypass bot detection.
    """

    def __init__(self, headless: bool = True) -> None:
        """
        Initialize session manager.

        Args:
            headless: Run browser in headless mode (default: True)
        """
        self.headless = headless
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._crumb: Optional[str] = None
        self._cookies: Optional[Dict[str, str]] = None

    async def get_session(self) -> Tuple[Page, str, Dict[str, str]]:
        """
        Get or create an active session with crumb and cookies.

        Returns:
            Tuple of (page, crumb, cookies)

        Raises:
            BrowserError: If browser launch fails
            AuthenticationError: If crumb extraction fails
        """
        if self._page and self._crumb and self._cookies:
            # Return existing session
            return self._page, self._crumb, self._cookies

        # Create new session
        await self._initialize_browser()
        await self._extract_crumb_and_cookies()

        if not self._crumb or not self._cookies or not self._page:
            raise AuthenticationError(
                "Failed to extract crumb and cookies from Yahoo Finance. "
                "This may be due to network issues or changes in Yahoo's authentication."
            )

        return self._page, self._crumb, self._cookies

    async def refresh_session(self) -> Tuple[Page, str, Dict[str, str]]:
        """
        Force refresh the session and get new crumb.

        Returns:
            Tuple of (page, crumb, cookies)

        Raises:
            BrowserError: If browser launch fails
            AuthenticationError: If crumb extraction fails
        """
        # Close existing session
        await self.close()

        # Create new session
        return await self.get_session()

    async def close(self) -> None:
        """Close browser and cleanup resources."""
        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None
        self._crumb = None
        self._cookies = None

    async def __aenter__(self) -> "SessionManager":
        """Context manager entry."""
        await self.get_session()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        await self.close()

    async def _initialize_browser(self) -> None:
        """
        Initialize browser with stealth configuration.

        Raises:
            BrowserError: If browser launch fails
        """
        try:
            # Use playwright-stealth to bypass bot detection
            self._playwright = await Stealth().use_async(async_playwright()).__aenter__()

            # Launch browser with anti-detection arguments
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                ],
            )

            # Create context with realistic viewport and user agent
            self._context = await self._browser.new_context(
                viewport={"width": 1920, "height": 1080}, user_agent=USER_AGENT
            )

            # Create page
            self._page = await self._context.new_page()

        except Exception as e:
            raise BrowserError(
                f"Failed to initialize browser: {e}. "
                "Ensure playwright is installed: playwright install chromium"
            ) from e

    async def _extract_crumb_and_cookies(self) -> None:
        """
        Extract CSRF crumb and cookies from Yahoo Finance.

        Tries multiple methods:
        1. Direct API endpoint (/v1/test/getcrumb)
        2. Page scraping from screener page

        Raises:
            AuthenticationError: If all methods fail
        """
        # Method 1: Try to get crumb from API endpoint
        crumb = await self._get_crumb_from_api()
        if crumb:
            self._crumb = crumb
            self._cookies = await self._get_cookies()
            return

        # Method 2: Navigate to Yahoo Finance and extract from page
        crumb = await self._get_crumb_from_page()
        if crumb:
            self._crumb = crumb
            self._cookies = await self._get_cookies()
            return

        raise AuthenticationError(
            "Could not extract crumb from Yahoo Finance using any method. "
            "Yahoo Finance may have changed their authentication mechanism."
        )

    async def _get_crumb_from_api(self) -> Optional[str]:
        """
        Try to get crumb from Yahoo Finance API endpoint.

        Returns:
            Crumb string if successful, None otherwise
        """
        if not self._page:
            return None

        try:
            response = await self._page.goto(
                CRUMB_URL, wait_until="domcontentloaded", timeout=10000
            )

            if response and response.ok:
                crumb = await response.text()
                crumb = crumb.strip()

                if crumb and len(crumb) > 0:
                    return crumb

        except Exception:
            # Silently fail and try next method
            pass

        return None

    async def _get_crumb_from_page(self) -> Optional[str]:
        """
        Extract crumb from Yahoo Finance screener page content.

        Returns:
            Crumb string if successful, None otherwise
        """
        if not self._page:
            return None

        try:
            # Navigate to Yahoo Finance screener page
            await self._page.goto(
                f"{YAHOO_FINANCE_URL}/screener/new", wait_until="load", timeout=30000
            )

            # Wait for page to fully load
            await self._page.wait_for_timeout(3000)

            # Get page content
            content = await self._page.content()

            # Try multiple regex patterns to find crumb
            patterns = [
                r'"crumb":"([^"]+)"',
                r'crumb["\']?\s*:\s*["\']([^"\']+)["\']',
                r'CrumbStore.*?"crumb":"([^"]+)"',
            ]

            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    crumb = match.group(1)
                    if crumb and len(crumb) > 0:
                        return crumb

        except Exception:
            # Silently fail
            pass

        return None

    async def _get_cookies(self) -> Dict[str, str]:
        """
        Get cookies from current browser context.

        Returns:
            Dictionary of cookie name-value pairs
        """
        if not self._context:
            return {}

        cookies = await self._context.cookies()
        return {cookie["name"]: cookie["value"] for cookie in cookies}
