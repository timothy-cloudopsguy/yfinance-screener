# yfinance-screener

A Python package providing programmatic access to Yahoo Finance's stock screener with complete feature parity to the web interface.

## Overview

yfinance-screener enables you to screen stocks using all the filters available on Yahoo Finance's web screener, with a clean, yfinance-compatible API. Whether you need simple price-based screening or complex multi-criteria queries, this package provides both simple and advanced interfaces to meet your needs.

## Key Features

- **Complete Filter Support**: Access all Yahoo Finance screener filters including price, market cap, valuation ratios, growth metrics, profitability metrics, and more
- **Geographic Markets**: Screen stocks from US, European, Asian, and other international markets
- **Flexible Query Building**: Use simple parameter-based screening or build complex queries with a fluent interface
- **YFinance Compatible**: Results are returned in formats compatible with the yfinance library (DataFrames and symbol lists)
- **Performance Optimized**: Built-in caching, session reuse, and intelligent pagination for fast results
- **Robust Error Handling**: Clear, actionable error messages for all failure scenarios
- **Type Hints**: Full type hint support for better IDE integration and code quality

## Quick Start

### Installation

```bash
pip install yfinance-screener

# Install playwright browsers (required for authentication)
playwright install chromium
```

### Basic Usage

```python
from yfinance_screener import Screener

# Create screener instance
screener = Screener()

# Simple screening - get symbols
symbols = screener.screen(
    min_price=10,
    max_price=100,
    min_market_cap=1_000_000_000,
    max_results=50
)
print(symbols)  # ['AAPL', 'MSFT', ...]

# Get detailed data as DataFrame
df = screener.screen(
    min_price=10,
    max_price=100,
    sectors=["Technology", "Healthcare"],
    as_dataframe=True
)
print(df.head())
```

### Advanced Query Building

```python
from yfinance_screener import Screener

screener = Screener()

# Build complex query with fluent interface
results = (screener.query()
    .price(min=10, max=100)
    .market_cap(min=1_000_000_000)
    .pe_ratio(max=25)
    .dividend_yield(min=2.0)
    .sector("Technology", "Healthcare")
    .region("us")
    .sort_by("marketcap", "desc")
    .limit(50)
    .execute(as_dataframe=True))

print(results)
```

## Integration with yfinance

yfinance-screener is designed to work seamlessly with the yfinance library:

```python
import yfinance as yf
from yfinance_screener import Screener

# Screen for stocks
screener = Screener()
symbols = screener.screen(
    min_price=50,
    max_price=200,
    min_market_cap=10_000_000_000,
    sectors=["Technology"],
    max_results=10
)

# Use yfinance to get detailed data
for symbol in symbols:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    print(f"{symbol}: {info.get('longName')} - ${info.get('currentPrice')}")
```

## Documentation

- [Quick Start Guide](quickstart.md) - Installation and basic examples
- [API Reference](api_reference.md) - Complete API documentation
- [Filter Reference](filters.md) - All available filters and their usage
- [Migration Guide](migration_guide.md) - Migrating from yfinance_screener_fetcher

## Requirements

- Python 3.8+
- playwright >= 1.40.0
- playwright-stealth >= 1.0.0
- pandas >= 1.5.0 (optional, required for DataFrame output)
- aiohttp >= 3.8.0

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
