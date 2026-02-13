"""
Advanced Query Building Examples

This module demonstrates advanced stock screening using the QueryBuilder
fluent interface for complex, chainable queries.
"""

from yfinance_screener import Screener


def example_1_query_builder_basics():
    """Basic QueryBuilder usage."""
    print("\n=== Example 1: QueryBuilder Basics ===")
    
    screener = Screener()
    
    # Build a query using fluent interface
    results = (screener.query()
        .price(min=10, max=100)
        .market_cap(min=1_000_000_000)
        .limit(10)
        .execute())
    
    print(f"Found {len(results)} stocks:")
    print(results)


def example_2_complex_valuation_query():
    """Complex query with multiple valuation filters."""
    print("\n=== Example 2: Complex Valuation Query ===")
    
    screener = Screener()
    
    # Find undervalued stocks with multiple criteria
    results = (screener.query()
        .pe_ratio(min=5, max=20)
        .pb_ratio(max=3)
        .peg_ratio(max=1.5)
        .market_cap(min=1_000_000_000)
        .sort_by("peratio", "asc")
        .limit(15)
        .execute())
    
    print(f"Found {len(results)} undervalued stocks:")
    print(results)


def example_3_sector_and_industry():
    """Filter by multiple sectors and industries."""
    print("\n=== Example 3: Multiple Sectors ===")
    
    screener = Screener()
    
    # Find stocks in tech or healthcare sectors
    results = (screener.query()
        .sector("Technology", "Healthcare")
        .price(min=20, max=500)
        .volume(min=500_000)
        .limit(20)
        .execute())
    
    print(f"Found {len(results)} tech or healthcare stocks:")
    print(results[:10])


def example_4_growth_and_profitability():
    """Combine growth and profitability filters."""
    print("\n=== Example 4: Growth + Profitability ===")
    
    screener = Screener()
    
    # Find profitable growth stocks
    df = (screener.query()
        .revenue_growth(min=15)
        .earnings_growth(min=20)
        .profit_margin(min=10)
        .roe(min=15)
        .market_cap(min=2_000_000_000)
        .sort_by("marketcap", "desc")
        .limit(10)
        .execute(as_dataframe=True))
    
    print(f"Found {len(df)} profitable growth stocks:")
    print(df[['symbol', 'name', 'price', 'marketCap']])


def example_5_dividend_aristocrats():
    """Find high-quality dividend stocks."""
    print("\n=== Example 5: Dividend Aristocrats ===")
    
    screener = Screener()
    
    # Find large-cap dividend payers with strong fundamentals
    df = (screener.query()
        .dividend_yield(min=2.5, max=8)
        .market_cap(min=10_000_000_000)
        .roe(min=10)
        .profit_margin(min=10)
        .sort_by("dividendyield", "desc")
        .limit(15)
        .execute(as_dataframe=True))
    
    print(f"Found {len(df)} dividend aristocrat candidates:")
    print(df[['symbol', 'name', 'dividendYield', 'marketCap']])


def example_6_momentum_stocks():
    """Find stocks with strong momentum."""
    print("\n=== Example 6: Momentum Stocks ===")
    
    screener = Screener()
    
    # Find stocks with high volume and growth
    results = (screener.query()
        .volume(min=2_000_000)
        .revenue_growth(min=20)
        .price(min=10)
        .market_cap(min=500_000_000)
        .sort_by("volume", "desc")
        .limit(20)
        .execute())
    
    print(f"Found {len(results)} momentum stocks:")
    print(results[:10])


def example_7_value_investing():
    """Classic value investing criteria."""
    print("\n=== Example 7: Value Investing ===")
    
    screener = Screener()
    
    # Benjamin Graham style value stocks
    df = (screener.query()
        .pe_ratio(max=15)
        .pb_ratio(max=1.5)
        .dividend_yield(min=2)
        .market_cap(min=1_000_000_000)
        .sort_by("peratio", "asc")
        .limit(20)
        .execute(as_dataframe=True))
    
    print(f"Found {len(df)} value stocks:")
    print(df[['symbol', 'name', 'pe', 'dividendYield']])


def example_8_quality_stocks():
    """Find high-quality companies."""
    print("\n=== Example 8: Quality Stocks ===")
    
    screener = Screener()
    
    # High ROE, high profit margin, large cap
    df = (screener.query()
        .roe(min=20)
        .roa(min=10)
        .profit_margin(min=15)
        .market_cap(min=5_000_000_000)
        .sort_by("roe", "desc")
        .limit(15)
        .execute(as_dataframe=True))
    
    print(f"Found {len(df)} quality stocks:")
    print(df[['symbol', 'name', 'marketCap']])


def example_9_regional_comparison():
    """Compare stocks across regions."""
    print("\n=== Example 9: Regional Comparison ===")
    
    screener = Screener()
    
    # US tech stocks
    us_stocks = (screener.query()
        .region("us")
        .sector("Technology")
        .market_cap(min=10_000_000_000)
        .limit(5)
        .execute())
    
    print(f"US tech stocks: {us_stocks}")
    
    # European tech stocks
    eu_stocks = (screener.query()
        .region("eu")
        .sector("Technology")
        .market_cap(min=10_000_000_000)
        .limit(5)
        .execute())
    
    print(f"EU tech stocks: {eu_stocks}")


def example_10_custom_sorting():
    """Advanced sorting examples."""
    print("\n=== Example 10: Custom Sorting ===")
    
    screener = Screener()
    
    # Sort by different fields
    print("\nTop 5 by market cap:")
    top_by_cap = (screener.query()
        .sector("Technology")
        .sort_by("marketcap", "desc")
        .limit(5)
        .execute())
    print(top_by_cap)
    
    print("\nTop 5 by volume:")
    top_by_volume = (screener.query()
        .sector("Technology")
        .sort_by("volume", "desc")
        .limit(5)
        .execute())
    print(top_by_volume)
    
    print("\nLowest P/E ratios:")
    low_pe = (screener.query()
        .sector("Technology")
        .pe_ratio(min=1)  # Exclude negative P/E
        .sort_by("peratio", "asc")
        .limit(5)
        .execute())
    print(low_pe)


def example_11_build_without_execute():
    """Build query dictionary without executing."""
    print("\n=== Example 11: Build Without Execute ===")
    
    screener = Screener()
    
    # Build query and inspect it
    query = (screener.query()
        .price(min=10, max=100)
        .sector("Technology")
        .market_cap(min=1_000_000_000)
        .build())
    
    print("Query structure:")
    import json
    print(json.dumps(query, indent=2))


def example_12_incremental_query_building():
    """Build queries incrementally based on conditions."""
    print("\n=== Example 12: Incremental Query Building ===")
    
    screener = Screener()
    
    # Start with base query
    query = screener.query().market_cap(min=1_000_000_000)
    
    # Add filters based on conditions
    include_tech = True
    include_healthcare = False
    require_dividends = True
    
    if include_tech and include_healthcare:
        query = query.sector("Technology", "Healthcare")
    elif include_tech:
        query = query.sector("Technology")
    elif include_healthcare:
        query = query.sector("Healthcare")
    
    if require_dividends:
        query = query.dividend_yield(min=1.5)
    
    # Execute the built query
    results = query.limit(10).execute()
    
    print(f"Found {len(results)} stocks matching dynamic criteria:")
    print(results)


def example_13_all_filter_types():
    """Demonstrate all available filter types."""
    print("\n=== Example 13: All Filter Types ===")
    
    screener = Screener()
    
    # Use every type of filter
    df = (screener.query()
        # Price filters
        .price(min=20, max=500)
        # Size filters
        .market_cap(min=1_000_000_000)
        .volume(min=500_000)
        # Valuation filters
        .pe_ratio(min=5, max=30)
        .pb_ratio(max=5)
        # Profitability filters
        .profit_margin(min=5)
        .roe(min=10)
        # Growth filters
        .revenue_growth(min=5)
        # Income filters
        .dividend_yield(min=0.5)
        # Categorical filters
        .sector("Technology")
        .region("us")
        # Sorting and limiting
        .sort_by("marketcap", "desc")
        .limit(5)
        .execute(as_dataframe=True))
    
    print(f"Found {len(df)} stocks matching all criteria:")
    print(df[['symbol', 'name', 'price', 'marketCap']])


def example_14_error_handling():
    """Demonstrate error handling."""
    print("\n=== Example 14: Error Handling ===")
    
    from yfinance_screener import ValidationError
    
    screener = Screener()
    
    # Example 1: Invalid price range
    try:
        results = (screener.query()
            .price(min=100, max=10)  # Invalid: min > max
            .execute())
    except ValidationError as e:
        print(f"Caught validation error: {e}")
    
    # Example 2: Empty query
    try:
        results = screener.query().build()  # No filters added
    except ValidationError as e:
        print(f"Caught validation error: {e}")
    
    # Example 3: Invalid sort order
    try:
        results = (screener.query()
            .price(min=10)
            .sort_by("price", "invalid")  # Invalid sort order
            .execute())
    except ValidationError as e:
        print(f"Caught validation error: {e}")


def example_15_reusable_queries():
    """Create reusable query templates."""
    print("\n=== Example 15: Reusable Query Templates ===")
    
    screener = Screener()
    
    def create_value_query():
        """Template for value stocks."""
        return (screener.query()
            .pe_ratio(max=15)
            .pb_ratio(max=2)
            .dividend_yield(min=2)
            .market_cap(min=1_000_000_000))
    
    def create_growth_query():
        """Template for growth stocks."""
        return (screener.query()
            .revenue_growth(min=15)
            .earnings_growth(min=20)
            .market_cap(min=1_000_000_000))
    
    # Use templates with different sectors
    print("\nValue stocks in Technology:")
    tech_value = create_value_query().sector("Technology").limit(5).execute()
    print(tech_value)
    
    print("\nGrowth stocks in Healthcare:")
    health_growth = create_growth_query().sector("Healthcare").limit(5).execute()
    print(health_growth)


if __name__ == "__main__":
    print("=" * 60)
    print("YFinance Screener - Advanced Query Examples")
    print("=" * 60)
    
    # Run all examples
    # Note: Comment out examples you don't want to run
    
    example_1_query_builder_basics()
    example_2_complex_valuation_query()
    example_3_sector_and_industry()
    example_4_growth_and_profitability()
    example_5_dividend_aristocrats()
    example_6_momentum_stocks()
    example_7_value_investing()
    example_8_quality_stocks()
    example_9_regional_comparison()
    example_10_custom_sorting()
    example_11_build_without_execute()
    example_12_incremental_query_building()
    example_13_all_filter_types()
    example_14_error_handling()
    example_15_reusable_queries()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
