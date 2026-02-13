"""
Example: Region Filtering

This example demonstrates how to filter stocks by region.
By default, the screener returns only US stocks.
"""

from yfinance_screener import Screener

# Create screener instance
screener = Screener()

print("=" * 60)
print("Example 1: Default behavior (US stocks only)")
print("=" * 60)
print()
print("Code:")
print("  symbols = screener.screen(min_price=50, max_results=5)")
print()
print("This will return only US stocks (no .SZ, .DU, .F suffixes)")
print()

# Uncomment to run (requires browser):
# symbols = screener.screen(min_price=50, max_results=5)
# print(f"Found {len(symbols)} US stocks: {symbols}")
# print()

print("=" * 60)
print("Example 2: Search European stocks")
print("=" * 60)
print()
print("Code:")
print("  symbols = screener.screen(")
print("      min_price=50,")
print("      regions=['eu'],")
print("      max_results=5")
print("  )")
print()

# Uncomment to run (requires browser):
# symbols = screener.screen(min_price=50, regions=["eu"], max_results=5)
# print(f"Found {len(symbols)} European stocks: {symbols}")
# print()

print("=" * 60)
print("Example 3: Search multiple regions")
print("=" * 60)
print()
print("Code:")
print("  symbols = screener.screen(")
print("      min_price=50,")
print("      regions=['us', 'ca', 'gb'],  # US, Canada, UK")
print("      max_results=5")
print("  )")
print()

# Uncomment to run (requires browser):
# symbols = screener.screen(
#     min_price=50,
#     regions=["us", "ca", "gb"],
#     max_results=5
# )
# print(f"Found {len(symbols)} stocks from US/CA/GB: {symbols}")
# print()

print("=" * 60)
print("Example 4: Search ALL regions (global)")
print("=" * 60)
print()
print("Code:")
print("  symbols = screener.screen(")
print("      min_price=50,")
print("      regions=[],  # Empty list = all regions")
print("      max_results=5")
print("  )")
print()
print("This will return stocks from all regions worldwide")
print("(including .SZ, .DU, .F, .MU, etc.)")
print()

# Uncomment to run (requires browser):
# symbols = screener.screen(min_price=50, regions=[], max_results=5)
# print(f"Found {len(symbols)} global stocks: {symbols}")
# print()

print("=" * 60)
print("Available Regions")
print("=" * 60)
print()
print("  - 'us'   : United States (default)")
print("  - 'eu'   : Europe")
print("  - 'asia' : Asia")
print("  - 'au'   : Australia")
print("  - 'ca'   : Canada")
print("  - 'gb'   : United Kingdom")
print()

print("=" * 60)
print("Using Query Builder")
print("=" * 60)
print()
print("You can also use the query builder for more complex queries:")
print()
print("Code:")
print("  results = screener.query() \\")
print("      .price(min=50, max=200) \\")
print("      .market_cap(min=1_000_000_000) \\")
print("      .region('us') \\  # Explicitly set region")
print("      .sector('Technology') \\")
print("      .limit(10) \\")
print("      .execute(as_dataframe=True)")
print()
print("Note: When using query builder, you must explicitly call")
print("      .region() if you want to filter by region.")
print()
