# YFinance Screener Examples

This directory contains comprehensive examples demonstrating how to use the yfinance-screener package for stock screening and analysis.

## Example Files

### 1. basic_screening.py

Simple, straightforward examples using the `Screener.screen()` method with parameter-based filtering.

**Topics covered:**
- Simple price filtering
- Market cap filtering
- Sector and industry filtering
- Multiple filter combinations
- Valuation metrics (P/E, P/B, PEG ratios)
- Dividend screening
- Growth stock screening
- Profitability metrics
- Regional screening
- Caching for performance
- Custom sorting
- DataFrame output
- Available filter values

**Run it:**
```bash
python examples/basic_screening.py
```

### 2. advanced_queries.py

Advanced examples using the `QueryBuilder` fluent interface for complex, chainable queries.

**Topics covered:**
- QueryBuilder basics
- Complex valuation queries
- Multiple sector filtering
- Growth and profitability combinations
- Dividend aristocrat screening
- Momentum stock identification
- Value investing criteria
- Quality stock screening
- Regional comparisons
- Custom sorting strategies
- Building queries without execution
- Incremental query building
- All filter types demonstration
- Error handling
- Reusable query templates

**Run it:**
```bash
python examples/advanced_queries.py
```

### 3. yfinance_integration.py

Integration examples showing how to combine yfinance-screener with the yfinance library for comprehensive analysis workflows.

**Topics covered:**
- Screen then analyze workflow
- Historical data download
- Portfolio building
- Fundamental analysis
- Dividend analysis
- Technical screening
- Sector rotation strategies
- Value vs growth comparison
- Options screening
- Watchlist building

**Requirements:**
```bash
pip install yfinance
```

**Run it:**
```bash
python examples/yfinance_integration.py
```

## Quick Start

### Installation

First, install the package:

```bash
pip install yfinance-screener
playwright install chromium
```

### Basic Usage

```python
from yfinance_screener import Screener

# Create screener instance
screener = Screener()

# Simple screening
symbols = screener.screen(
    min_price=10,
    max_price=100,
    sectors=["Technology"],
    max_results=10
)

print(f"Found {len(symbols)} stocks: {symbols}")
```

### Advanced Usage

```python
from yfinance_screener import Screener

screener = Screener()

# Build complex query
results = (screener.query()
    .price(min=10, max=100)
    .market_cap(min=1_000_000_000)
    .pe_ratio(max=25)
    .sector("Technology", "Healthcare")
    .sort_by("marketcap", "desc")
    .limit(20)
    .execute(as_dataframe=True))

print(results[['symbol', 'name', 'price', 'marketCap']])
```

## Common Use Cases

### Value Investing

```python
# Find undervalued stocks
symbols = screener.screen(
    max_pe_ratio=15,
    max_pb_ratio=2,
    min_dividend_yield=2,
    min_market_cap=1_000_000_000
)
```

### Growth Investing

```python
# Find high-growth stocks
symbols = screener.screen(
    min_revenue_growth=20,
    min_earnings_growth=25,
    min_market_cap=1_000_000_000
)
```

### Dividend Investing

```python
# Find dividend aristocrats
symbols = screener.screen(
    min_dividend_yield=3,
    min_market_cap=10_000_000_000,
    min_roe=15
)
```

### Quality Stocks

```python
# Find high-quality companies
symbols = screener.screen(
    min_roe=20,
    min_profit_margin=15,
    min_market_cap=5_000_000_000
)
```

## Tips and Best Practices

### 1. Use Caching for Repeated Queries

```python
# Enable caching (default)
screener = Screener(cache_enabled=True, cache_ttl=3600)

# First query fetches from API
results1 = screener.screen(min_price=10, max_price=100)

# Second identical query uses cache (much faster)
results2 = screener.screen(min_price=10, max_price=100)
```

### 2. Limit Results for Faster Queries

```python
# Only fetch what you need
symbols = screener.screen(
    sectors=["Technology"],
    max_results=10  # Stop after 10 results
)
```

### 3. Use DataFrame Output for Analysis

```python
# Get detailed data as DataFrame
df = screener.screen(
    min_market_cap=1_000_000_000,
    as_dataframe=True
)

# Now you can use pandas operations
print(df.describe())
print(df[df['pe'] < 15])
```

### 4. Handle Errors Gracefully

```python
from yfinance_screener import ValidationError, NetworkError

try:
    results = screener.screen(min_price=10, max_price=100)
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

### 5. Build Reusable Query Templates

```python
def create_value_query(screener):
    """Reusable template for value stocks."""
    return (screener.query()
        .pe_ratio(max=15)
        .pb_ratio(max=2)
        .dividend_yield(min=2))

# Use with different sectors
tech_value = create_value_query(screener).sector("Technology").execute()
health_value = create_value_query(screener).sector("Healthcare").execute()
```

## Available Filters

### Numeric Range Filters
- `price` - Stock price
- `market_cap` - Market capitalization
- `volume` - Trading volume
- `pe_ratio` - Price-to-earnings ratio
- `pb_ratio` - Price-to-book ratio
- `peg_ratio` - PEG ratio
- `dividend_yield` - Dividend yield percentage
- `revenue_growth` - Revenue growth percentage
- `earnings_growth` - Earnings growth percentage
- `profit_margin` - Profit margin percentage
- `roe` - Return on equity percentage
- `roa` - Return on assets percentage

### Categorical Filters
- `sectors` - Business sectors
- `industries` - Industries
- `regions` - Geographic regions
- `exchanges` - Stock exchanges

### Result Options
- `max_results` - Limit number of results
- `sort_by` - Field to sort by
- `sort_order` - Sort direction ("asc" or "desc")
- `as_dataframe` - Return DataFrame instead of symbol list

## Getting Help

- **Documentation**: See the `docs/` directory
- **API Reference**: `docs/api_reference.md`
- **Filter Reference**: `docs/filters.md`
- **Migration Guide**: `docs/migration_guide.md`

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub.

Want to contribute an example? Pull requests are welcome!
