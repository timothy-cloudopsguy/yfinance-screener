# Quick Start Guide

This guide will help you get started with yfinance-screener quickly.

## Installation

### Install the Package

```bash
pip install yfinance-screener
```

### Install Playwright Browsers

yfinance-screener uses Playwright for browser automation to handle Yahoo Finance authentication. After installing the package, you need to install the Chromium browser:

```bash
playwright install chromium
```

### Optional: Install pandas

For DataFrame output support, install pandas:

```bash
pip install pandas
```

## Basic Examples

### Example 1: Simple Symbol List

Get a list of stock symbols matching basic criteria:

```python
from yfinance_screener import Screener

# Create screener instance
screener = Screener()

# Screen for stocks between $10 and $100
symbols = screener.screen(
    min_price=10,
    max_price=100,
    max_results=20
)

print(f"Found {len(symbols)} stocks:")
for symbol in symbols:
    print(symbol)
```

### Example 2: DataFrame Output

Get detailed stock data as a pandas DataFrame:

```python
from yfinance_screener import Screener

screener = Screener()

# Get detailed data as DataFrame
df = screener.screen(
    min_price=50,
    max_price=200,
    min_market_cap=10_000_000_000,
    max_results=50,
    as_dataframe=True
)

# Display results
print(df[['symbol', 'name', 'price', 'marketCap', 'pe']])

# Save to CSV
df.to_csv('screener_results.csv', index=False)
```

### Example 3: Sector Filtering

Screen stocks from specific sectors:

```python
from yfinance_screener import Screener

screener = Screener()

# Get technology and healthcare stocks
symbols = screener.screen(
    min_price=20,
    sectors=["Technology", "Healthcare"],
    min_market_cap=5_000_000_000,
    max_results=30
)

print(f"Found {len(symbols)} tech and healthcare stocks")
```

### Example 4: Valuation Metrics

Filter by valuation ratios:

```python
from yfinance_screener import Screener

screener = Screener()

# Find undervalued stocks
df = screener.screen(
    min_price=10,
    max_pe_ratio=15,  # P/E ratio under 15
    min_dividend_yield=2.0,  # Dividend yield at least 2%
    min_market_cap=1_000_000_000,
    as_dataframe=True
)

print(df[['symbol', 'name', 'price', 'pe', 'dividendYield']])
```

### Example 5: Growth Stocks

Screen for high-growth companies:

```python
from yfinance_screener import Screener

screener = Screener()

# Find growth stocks
df = screener.screen(
    min_revenue_growth=20,  # Revenue growth > 20%
    min_earnings_growth=15,  # Earnings growth > 15%
    sectors=["Technology"],
    max_results=25,
    as_dataframe=True
)

print(df[['symbol', 'name', 'price', 'marketCap']])
```

## Advanced Query Building

For more complex queries, use the QueryBuilder interface:

### Example 6: Fluent Query Interface

```python
from yfinance_screener import Screener

screener = Screener()

# Build complex query with method chaining
results = (screener.query()
    .price(min=25, max=150)
    .market_cap(min=5_000_000_000)
    .pe_ratio(min=10, max=30)
    .dividend_yield(min=1.5)
    .sector("Technology", "Healthcare", "Financial Services")
    .region("us")
    .sort_by("marketcap", "desc")
    .limit(40)
    .execute(as_dataframe=True))

print(results)
```

### Example 7: Multiple Filters

Combine many filters for precise screening:

```python
from yfinance_screener import Screener

screener = Screener()

# Comprehensive screening
query = (screener.query()
    .price(min=50, max=500)
    .market_cap(min=10_000_000_000)
    .volume(min=1_000_000)
    .pe_ratio(max=25)
    .pb_ratio(max=5)
    .roe(min=15)
    .profit_margin(min=10)
    .sector("Technology")
    .sort_by("volume", "desc")
    .limit(20))

# Execute and get results
symbols = query.execute()
print(symbols)
```

## Integration with yfinance

yfinance-screener works great with the yfinance library:

### Example 8: Screen and Fetch Details

```python
import yfinance as yf
from yfinance_screener import Screener

# Screen for stocks
screener = Screener()
symbols = screener.screen(
    min_price=100,
    max_price=500,
    sectors=["Technology"],
    min_market_cap=50_000_000_000,
    max_results=5
)

# Get detailed info with yfinance
for symbol in symbols:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    
    print(f"\n{symbol} - {info.get('longName')}")
    print(f"  Price: ${info.get('currentPrice'):.2f}")
    print(f"  Market Cap: ${info.get('marketCap'):,.0f}")
    print(f"  P/E Ratio: {info.get('trailingPE', 'N/A')}")
```

### Example 9: Screen and Download Historical Data

```python
import yfinance as yf
from yfinance_screener import Screener

# Screen for dividend stocks
screener = Screener()
symbols = screener.screen(
    min_dividend_yield=3.0,
    min_market_cap=10_000_000_000,
    max_results=10
)

# Download historical data
data = yf.download(symbols, period="1y", group_by="ticker")

# Analyze returns
for symbol in symbols:
    if symbol in data:
        returns = data[symbol]['Close'].pct_change().mean() * 252
        print(f"{symbol}: {returns:.2%} annualized return")
```

## Configuration Options

### Caching

Control result caching for better performance:

```python
from yfinance_screener import Screener

# Enable caching with 2-hour TTL
screener = Screener(
    cache_enabled=True,
    cache_ttl=7200  # 2 hours in seconds
)

# Disable caching for real-time data
screener = Screener(cache_enabled=False)
```

### Headless Mode

Control browser visibility (useful for debugging):

```python
from yfinance_screener import Screener

# Run browser in visible mode (for debugging)
screener = Screener(headless=False)

# Run in headless mode (default, faster)
screener = Screener(headless=True)
```

## Available Sectors and Regions

### Get Available Values

```python
from yfinance_screener import Screener

screener = Screener()

# Get available sectors
sectors = screener.get_available_sectors()
print("Available sectors:", sectors)

# Get available regions
regions = screener.get_available_regions()
print("Available regions:", regions)

# Get sample industries
industries = screener.get_available_industries()
print("Sample industries:", industries)
```

## Error Handling

Handle errors gracefully:

```python
from yfinance_screener import Screener
from yfinance_screener import (
    ValidationError,
    AuthenticationError,
    NetworkError,
    RateLimitError
)

screener = Screener()

try:
    results = screener.screen(
        min_price=10,
        max_price=100,
        sectors=["Technology"]
    )
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
```

## Next Steps

- Read the [API Reference](api_reference.md) for complete documentation
- Check the [Filter Reference](filters.md) for all available filters
- See the [Migration Guide](migration_guide.md) if upgrading from yfinance_screener_fetcher

## Tips

1. **Use max_results**: Always set a reasonable `max_results` limit for faster queries
2. **Enable caching**: Cache results when you don't need real-time data
3. **Combine filters**: Use multiple filters to narrow down results precisely
4. **DataFrame output**: Use `as_dataframe=True` for easier data analysis
5. **Error handling**: Always wrap screening calls in try-except blocks for production code
