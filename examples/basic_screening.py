"""
Basic Stock Screening Examples

This module demonstrates simple stock screening using the yfinance-screener package.
Examples cover common screening scenarios with straightforward parameter-based filtering.
"""

from yfinance_screener import Screener


def example_1_simple_price_filter():
    """Screen stocks by price range."""
    print("\n=== Example 1: Simple Price Filter ===")
    
    screener = Screener()
    
    # Find stocks priced between $10 and $100
    symbols = screener.screen(
        min_price=10,
        max_price=100,
        max_results=10
    )
    
    print(f"Found {len(symbols)} stocks between $10 and $100:")
    print(symbols)


def example_2_market_cap_filter():
    """Screen stocks by market capitalization."""
    print("\n=== Example 2: Market Cap Filter ===")
    
    screener = Screener()
    
    # Find large-cap stocks (market cap > $10 billion)
    symbols = screener.screen(
        min_market_cap=10_000_000_000,  # $10 billion
        max_results=20
    )
    
    print(f"Found {len(symbols)} large-cap stocks:")
    print(symbols[:10])  # Show first 10


def example_3_sector_filter():
    """Screen stocks by sector."""
    print("\n=== Example 3: Sector Filter ===")
    
    screener = Screener()
    
    # Find technology stocks
    symbols = screener.screen(
        sectors=["Technology"],
        max_results=15
    )
    
    print(f"Found {len(symbols)} technology stocks:")
    print(symbols)


def example_4_multiple_filters():
    """Combine multiple filters."""
    print("\n=== Example 4: Multiple Filters ===")
    
    screener = Screener()
    
    # Find affordable tech stocks with good volume
    symbols = screener.screen(
        min_price=20,
        max_price=150,
        sectors=["Technology"],
        min_volume=1_000_000,  # At least 1M daily volume
        max_results=10
    )
    
    print(f"Found {len(symbols)} tech stocks with price $20-$150 and volume > 1M:")
    print(symbols)


def example_5_valuation_filters():
    """Screen stocks by valuation metrics."""
    print("\n=== Example 5: Valuation Filters ===")
    
    screener = Screener()
    
    # Find value stocks with low P/E ratios
    symbols = screener.screen(
        min_pe_ratio=5,
        max_pe_ratio=15,
        min_market_cap=1_000_000_000,  # At least $1B market cap
        max_results=10
    )
    
    print(f"Found {len(symbols)} value stocks with P/E between 5 and 15:")
    print(symbols)


def example_6_dividend_stocks():
    """Screen for dividend-paying stocks."""
    print("\n=== Example 6: Dividend Stocks ===")
    
    screener = Screener()
    
    # Find stocks with dividend yield > 3%
    symbols = screener.screen(
        min_dividend_yield=3.0,  # 3% yield
        min_market_cap=5_000_000_000,  # Large caps only
        max_results=10
    )
    
    print(f"Found {len(symbols)} dividend stocks with yield > 3%:")
    print(symbols)


def example_7_dataframe_output():
    """Get detailed data as pandas DataFrame."""
    print("\n=== Example 7: DataFrame Output ===")
    
    screener = Screener()
    
    # Get detailed data instead of just symbols
    df = screener.screen(
        min_price=50,
        max_price=200,
        sectors=["Healthcare"],
        max_results=5,
        as_dataframe=True  # Return DataFrame instead of symbol list
    )
    
    print(f"Found {len(df)} healthcare stocks:")
    print(df[['symbol', 'name', 'price', 'marketCap', 'pe']])


def example_8_growth_stocks():
    """Screen for growth stocks."""
    print("\n=== Example 8: Growth Stocks ===")
    
    screener = Screener()
    
    # Find stocks with strong revenue and earnings growth
    symbols = screener.screen(
        min_revenue_growth=15,  # 15% revenue growth
        min_earnings_growth=20,  # 20% earnings growth
        min_market_cap=1_000_000_000,
        max_results=10
    )
    
    print(f"Found {len(symbols)} growth stocks:")
    print(symbols)


def example_9_profitable_stocks():
    """Screen for profitable stocks."""
    print("\n=== Example 9: Profitable Stocks ===")
    
    screener = Screener()
    
    # Find stocks with strong profitability metrics
    symbols = screener.screen(
        min_profit_margin=15,  # 15% profit margin
        min_roe=15,  # 15% return on equity
        min_market_cap=2_000_000_000,
        max_results=10
    )
    
    print(f"Found {len(symbols)} highly profitable stocks:")
    print(symbols)


def example_10_regional_screening():
    """Screen stocks by region."""
    print("\n=== Example 10: Regional Screening ===")
    
    screener = Screener()
    
    # Find European stocks
    symbols = screener.screen(
        regions=["eu"],
        min_market_cap=5_000_000_000,
        max_results=10
    )
    
    print(f"Found {len(symbols)} European stocks:")
    print(symbols)


def example_11_caching():
    """Demonstrate caching for faster repeated queries."""
    print("\n=== Example 11: Caching ===")
    
    import time
    
    # First query - will fetch from API
    screener = Screener(cache_enabled=True, cache_ttl=3600)
    
    print("First query (fetching from API)...")
    start = time.time()
    symbols1 = screener.screen(
        min_price=50,
        max_price=100,
        sectors=["Technology"],
        max_results=10
    )
    elapsed1 = time.time() - start
    print(f"Found {len(symbols1)} stocks in {elapsed1:.2f} seconds")
    
    # Second identical query - will use cache
    print("\nSecond query (using cache)...")
    start = time.time()
    symbols2 = screener.screen(
        min_price=50,
        max_price=100,
        sectors=["Technology"],
        max_results=10
    )
    elapsed2 = time.time() - start
    print(f"Found {len(symbols2)} stocks in {elapsed2:.2f} seconds")
    print(f"Cache speedup: {elapsed1/elapsed2:.1f}x faster")


def example_12_sorting():
    """Screen with custom sorting."""
    print("\n=== Example 12: Custom Sorting ===")
    
    screener = Screener()
    
    # Find stocks sorted by market cap (largest first)
    df = screener.screen(
        sectors=["Technology"],
        min_market_cap=10_000_000_000,
        sort_by="marketcap",
        sort_order="desc",
        max_results=10,
        as_dataframe=True
    )
    
    print("Top 10 tech stocks by market cap:")
    print(df[['symbol', 'name', 'marketCap']])


def example_13_available_filters():
    """Show available filter values."""
    print("\n=== Example 13: Available Filter Values ===")
    
    screener = Screener()
    
    # Get available sectors
    sectors = screener.get_available_sectors()
    print(f"\nAvailable sectors ({len(sectors)}):")
    print(sectors)
    
    # Get available regions
    regions = screener.get_available_regions()
    print(f"\nAvailable regions ({len(regions)}):")
    print(regions)
    
    # Get sample industries
    industries = screener.get_available_industries()
    print(f"\nSample industries ({len(industries)}):")
    print(industries[:10])


if __name__ == "__main__":
    print("=" * 60)
    print("YFinance Screener - Basic Examples")
    print("=" * 60)
    
    # Run all examples
    # Note: Comment out examples you don't want to run
    
    example_1_simple_price_filter()
    example_2_market_cap_filter()
    example_3_sector_filter()
    example_4_multiple_filters()
    example_5_valuation_filters()
    example_6_dividend_stocks()
    example_7_dataframe_output()
    example_8_growth_stocks()
    example_9_profitable_stocks()
    example_10_regional_screening()
    example_11_caching()
    example_12_sorting()
    example_13_available_filters()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
