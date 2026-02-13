#!/usr/bin/env python3
"""
Test script to verify US region default behavior.
"""

from yfinance_screener import Screener

print("Testing US region default behavior...")
print()

# Create screener
screener = Screener(cache_enabled=False, headless=True)

# Test 1: Build query using screen() method (should default to US)
print("Test 1: Using screen() method (should default to US)")
print("Building query with: screener.screen(min_price=10, max_price=100)")
print()

# We can't actually execute without browser, but we can check the query builder
# Let's manually test the logic
from yfinance_screener.query_builder import QueryBuilder

builder = QueryBuilder()
builder.price(min=10, max=100)

# Simulate what screen() does
regions = None  # User didn't specify
if regions is None:
    builder.region("us")
elif regions:
    builder.region(*regions)

query = builder.build()
print("Query with default US region:")
print(query)
print()

# Check if region filter is present
query_str = str(query)
if 'region' in query_str.lower() or 'us' in query_str:
    print("✓ Region filter appears to be present")
else:
    print("✗ Region filter NOT found in query")

print()
print("Test 2: Explicitly passing empty list (should search all regions)")
builder2 = QueryBuilder()
builder2.price(min=10, max=100)

regions = []  # User explicitly wants all regions
if regions is None:
    builder2.region("us")
elif regions:
    builder2.region(*regions)

query2 = builder2.build()
print("Query with empty regions list:")
print(query2)
print()

print("Test 3: Explicitly passing ['eu'] (should search Europe)")
builder3 = QueryBuilder()
builder3.price(min=10, max=100)

regions = ["eu"]
if regions is None:
    builder3.region("us")
elif regions:
    builder3.region(*regions)

query3 = builder3.build()
print("Query with EU region:")
print(query3)
print()

print("=" * 60)
print("To test with actual API call (requires browser):")
print("  screener = Screener()")
print("  df = screener.screen(min_price=10, max_price=100, max_results=10, as_dataframe=True)")
print("  print(df['symbol'].tolist())")
print()
print("Expected: Only US stock symbols (no .SZ, .DU, .F, .MU suffixes)")
