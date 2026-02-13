# yfinance-screener

A Python package providing programmatic access to Yahoo Finance's stock screener with complete feature parity to the web interface.

## Features

- **Complete Filter Support**: Access all Yahoo Finance screener filters including price, market cap, P/E ratio, volume, dividends, sectors, regions, and more
- **US Stocks by Default**: Automatically filters to US stocks unless you specify different regions
- **YFinance Compatible**: Returns data in formats compatible with the yfinance library
- **Flexible Query Building**: Simple parameter-based screening or advanced fluent query builder interface
- **Smart Caching**: Configurable result caching to minimize API calls
- **Robust Error Handling**: Clear error messages and automatic retry logic
- **Type Hints**: Full type hint support for better IDE integration

## Installation

```bash
pip install yfinance-screener
```

After installation, you need to install the Playwright browser:

```bash
playwright install chromium
```

## Quick Start

### Simple Screening

```python
from yfinance_screener import Screener

# Create a screener instance
screener = Screener()

# Screen for US stocks with basic filters (US is the default region)
symbols = screener.screen(
    min_price=10,
    max_price=100,
    min_market_cap=10_000_000_000,
    max_results=50
)

print(f"Found {len(symbols)} stocks: {symbols[:5]}")
```

### Get Detailed Data as DataFrame

```python
import pandas as pd
from yfinance_screener import Screener

screener = Screener()

# Get detailed data as pandas DataFrame
df = screener.screen(
    min_price=10,
    max_price=100,
    sectors=["Technology", "Healthcare"],
    min_pe_ratio=10,
    max_pe_ratio=30,
    as_dataframe=True
)

print(df.head())
```

### Advanced Query Building

```python
from yfinance_screener import Screener

screener = Screener()

# Build complex queries with fluent interface
results = screener.query() \
    .price(min=50, max=200) \
    .market_cap(min=1_000_000_000) \
    .pe_ratio(min=10, max=25) \
    .dividend_yield(min=2.0) \
    .sector("Technology", "Healthcare") \
    .region("us") \
    .sort_by("marketCap", order="desc") \
    .limit(100) \
    .execute(as_dataframe=True)

print(results)
```

## Available Filters

The package supports all Yahoo Finance screener filters:

- **Price**: `min_price`, `max_price`
- **Market Cap**: `min_market_cap`, `max_market_cap`
- **Volume**: `min_volume`, `max_volume`
- **Valuation Ratios**: `min_pe_ratio`, `max_pe_ratio`, `min_pb_ratio`, `max_pb_ratio`, `min_peg_ratio`, `max_peg_ratio`
- **Dividends**: `min_dividend_yield`, `max_dividend_yield`
- **Growth Metrics**: `min_revenue_growth`, `max_revenue_growth`, `min_earnings_growth`, `max_earnings_growth`
- **Profitability**: `min_profit_margin`, `max_profit_margin`, `min_roe`, `max_roe`, `min_roa`, `max_roa`
- **Categorical**: `sectors`, `industries`, `regions`, `exchanges`

### Region Filtering

By default, the screener returns only US stocks. To search other regions:

```python
# Search European stocks
symbols = screener.screen(
    min_price=10,
    regions=["eu"]
)

# Search multiple regions
symbols = screener.screen(
    min_price=10,
    regions=["us", "ca", "gb"]  # US, Canada, UK
)

# Search ALL regions (pass empty list)
symbols = screener.screen(
    min_price=10,
    regions=[]
)
```

Available regions: `us`, `eu`, `asia`, `au`, `ca`, `gb`

## Configuration

```python
from yfinance_screener import Screener

# Configure caching and browser behavior
screener = Screener(
    cache_enabled=True,      # Enable result caching
    cache_ttl=3600,          # Cache TTL in seconds (1 hour)
    headless=True            # Run browser in headless mode
)
```

## Integration with yfinance

```python
import yfinance as yf
from yfinance_screener import Screener

# Screen for stocks
screener = Screener()
symbols = screener.screen(
    min_market_cap=50_000_000_000,
    sectors=["Technology"],
    max_results=10
)

# Use with yfinance to get detailed data
for symbol in symbols:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    print(f"{symbol}: {info.get('longName')} - ${info.get('currentPrice')}")
```

## Backward Compatibility

For users of the original `yfinance_screener_fetcher` module:

```python
from yfinance_screener import YFinanceScreenerFetcher

# Legacy interface still works
fetcher = YFinanceScreenerFetcher()
stocks = fetcher.fetch_stocks(
    min_price=10.0,
    max_price=100.0,
    min_market_cap=10_000_000_000
)
```

## Requirements

- Python 3.8+
- playwright >= 1.40.0
- playwright-stealth >= 1.0.0
- pandas >= 1.5.0
- aiohttp >= 3.8.0

## Documentation

For detailed documentation, see:
- [API Reference](https://yfinance-screener.readthedocs.io/api_reference)
- [Filter Guide](https://yfinance-screener.readthedocs.io/filters)
- [Migration Guide](https://yfinance-screener.readthedocs.io/migration_guide)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/yfinance-screener/issues
- Documentation: https://yfinance-screener.readthedocs.io
