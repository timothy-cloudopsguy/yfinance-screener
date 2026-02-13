# Migration Guide

Guide for migrating from `yfinance_screener_fetcher` to the new `yfinance-screener` package.

## Overview

The new `yfinance-screener` package provides a complete rewrite with enhanced features, better error handling, and a more flexible API. This guide will help you migrate your existing code.

## Key Differences

### Package Name

**Old:**
```python
from yfinance_screener_fetcher import YFinanceScreenerFetcher
```

**New:**
```python
from yfinance_screener import Screener
```

### Class Name

**Old:** `YFinanceScreenerFetcher`  
**New:** `Screener` (recommended) or `YFinanceScreenerFetcher` (legacy compatibility)

### Method Names

**Old:** `fetch_stocks()`, `fetch_stocks_detailed()`  
**New:** `screen()` with `as_dataframe` parameter

## Quick Migration

### Option 1: Minimal Changes (Legacy Compatibility)

The package includes a legacy compatibility layer. Simply update your import:

**Before:**
```python
from yfinance_screener_fetcher import YFinanceScreenerFetcher

fetcher = YFinanceScreenerFetcher()
symbols = fetcher.fetch_stocks(
    min_price=10,
    max_price=100,
    min_market_cap=10_000_000_000,
    max_results=100
)
```

**After:**
```python
from yfinance_screener import YFinanceScreenerFetcher

fetcher = YFinanceScreenerFetcher()  # Emits deprecation warning
symbols = fetcher.fetch_stocks(
    min_price=10,
    max_price=100,
    min_market_cap=10_000_000_000,
    max_results=100
)
```

**Note:** This approach is deprecated and will be removed in version 2.0.0.

### Option 2: Recommended Migration

Update to use the new `Screener` class:

**Before:**
```python
from yfinance_screener_fetcher import YFinanceScreenerFetcher

fetcher = YFinanceScreenerFetcher()
symbols = fetcher.fetch_stocks(
    min_price=10,
    max_price=100,
    min_market_cap=10_000_000_000,
    max_results=100
)
```

**After:**
```python
from yfinance_screener import Screener

screener = Screener()
symbols = screener.screen(
    min_price=10,
    max_price=100,
    min_market_cap=10_000_000_000,
    max_results=100
)
```

## Method Migration

### fetch_stocks() → screen()

**Before:**
```python
fetcher = YFinanceScreenerFetcher()
symbols = fetcher.fetch_stocks(
    min_price=10.0,
    max_price=100.0,
    min_market_cap=10_000_000_000,
    max_results=50
)
# Returns: ['AAPL', 'MSFT', ...]
```

**After:**
```python
screener = Screener()
symbols = screener.screen(
    min_price=10.0,
    max_price=100.0,
    min_market_cap=10_000_000_000,
    max_results=50
)
# Returns: ['AAPL', 'MSFT', ...]
```

### fetch_stocks_detailed() → screen(as_dataframe=True)

**Before:**
```python
fetcher = YFinanceScreenerFetcher()
stocks = fetcher.fetch_stocks_detailed(
    min_price=10.0,
    max_price=100.0,
    min_market_cap=10_000_000_000,
    max_results=50
)
# Returns: [{'symbol': 'AAPL', 'name': '...', ...}, ...]
```

**After:**
```python
screener = Screener()
df = screener.screen(
    min_price=10.0,
    max_price=100.0,
    min_market_cap=10_000_000_000,
    max_results=50,
    as_dataframe=True
)
# Returns: pandas DataFrame

# If you need list of dicts (like old behavior):
stocks = df.to_dict('records')
```

## New Features Available

### 1. Additional Filters

The new package supports many more filters:

```python
screener = Screener()

# Valuation filters
symbols = screener.screen(
    min_pe_ratio=10,
    max_pe_ratio=25,
    min_pb_ratio=1,
    max_pb_ratio=3,
    max_peg_ratio=2
)

# Dividend filters
symbols = screener.screen(
    min_dividend_yield=2.0,
    max_dividend_yield=8.0
)

# Growth filters
symbols = screener.screen(
    min_revenue_growth=15,
    min_earnings_growth=20
)

# Profitability filters
symbols = screener.screen(
    min_profit_margin=10,
    min_roe=15,
    min_roa=5
)

# Categorical filters
symbols = screener.screen(
    sectors=["Technology", "Healthcare"],
    industries=["Software—Application"],
    regions=["us", "eu"],
    exchanges=["NMS", "NYQ"]
)
```

### 2. Query Builder Interface

Build complex queries with a fluent interface:

```python
screener = Screener()

results = (screener.query()
    .price(min=10, max=100)
    .market_cap(min=1_000_000_000)
    .pe_ratio(max=25)
    .dividend_yield(min=2.0)
    .sector("Technology", "Healthcare")
    .sort_by("marketcap", "desc")
    .limit(50)
    .execute(as_dataframe=True))
```

### 3. Configuration Options

Control caching and browser behavior:

```python
# Custom cache settings
screener = Screener(
    cache_enabled=True,
    cache_ttl=7200,  # 2 hours
    headless=True
)

# Disable caching for real-time data
screener = Screener(cache_enabled=False)

# Visible browser (for debugging)
screener = Screener(headless=False)
```

### 4. Better Error Handling

More specific exceptions with helpful messages:

```python
from yfinance_screener import (
    Screener,
    ValidationError,
    AuthenticationError,
    NetworkError,
    RateLimitError
)

screener = Screener()

try:
    results = screener.screen(min_price=10, max_price=100)
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
```

### 5. Helper Methods

Get available filter values:

```python
screener = Screener()

# Get available sectors
sectors = screener.get_available_sectors()
print(sectors)

# Get available regions
regions = screener.get_available_regions()
print(regions)

# Get sample industries
industries = screener.get_available_industries()
print(industries)
```

## Common Migration Patterns

### Pattern 1: Simple Symbol Fetching

**Before:**
```python
from yfinance_screener_fetcher import YFinanceScreenerFetcher

def get_tech_stocks():
    fetcher = YFinanceScreenerFetcher()
    return fetcher.fetch_stocks(
        min_price=50,
        max_price=200,
        max_results=100
    )
```

**After:**
```python
from yfinance_screener import Screener

def get_tech_stocks():
    screener = Screener()
    return screener.screen(
        min_price=50,
        max_price=200,
        sectors=["Technology"],  # New: can filter by sector
        max_results=100
    )
```

### Pattern 2: Detailed Data Processing

**Before:**
```python
from yfinance_screener_fetcher import YFinanceScreenerFetcher

fetcher = YFinanceScreenerFetcher()
stocks = fetcher.fetch_stocks_detailed(max_results=50)

for stock in stocks:
    symbol = stock['symbol']
    name = stock['name']
    price = stock['price']
    print(f"{symbol}: {name} - ${price}")
```

**After:**
```python
from yfinance_screener import Screener

screener = Screener()
df = screener.screen(max_results=50, as_dataframe=True)

for _, row in df.iterrows():
    symbol = row['symbol']
    name = row['name']
    price = row['price']
    print(f"{symbol}: {name} - ${price}")

# Or more efficiently:
for symbol, name, price in zip(df['symbol'], df['name'], df['price']):
    print(f"{symbol}: {name} - ${price}")
```

### Pattern 3: Filtering and Sorting

**Before:**
```python
from yfinance_screener_fetcher import YFinanceScreenerFetcher

fetcher = YFinanceScreenerFetcher()
stocks = fetcher.fetch_stocks_detailed(
    min_price=10,
    max_price=100,
    min_market_cap=5_000_000_000,
    max_results=100
)

# Manual sorting
stocks_sorted = sorted(stocks, key=lambda x: x['marketCap'], reverse=True)
top_10 = stocks_sorted[:10]
```

**After:**
```python
from yfinance_screener import Screener

screener = Screener()
df = screener.screen(
    min_price=10,
    max_price=100,
    min_market_cap=5_000_000_000,
    sort_by="marketcap",
    sort_order="desc",
    max_results=10,  # Get top 10 directly
    as_dataframe=True
)
```

### Pattern 4: Integration with yfinance

**Before:**
```python
import yfinance as yf
from yfinance_screener_fetcher import YFinanceScreenerFetcher

fetcher = YFinanceScreenerFetcher()
symbols = fetcher.fetch_stocks(max_results=10)

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")
    print(f"{symbol}: {len(hist)} days of data")
```

**After:**
```python
import yfinance as yf
from yfinance_screener import Screener

screener = Screener()
symbols = screener.screen(
    min_volume=1_000_000,  # New: ensure liquid stocks
    max_results=10
)

for symbol in symbols:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1mo")
    print(f"{symbol}: {len(hist)} days of data")
```

## Breaking Changes

### 1. Return Type for Detailed Data

**Old:** Returns `List[Dict[str, Any]]`  
**New:** Returns `pd.DataFrame` (use `.to_dict('records')` for old format)

### 2. Default Parameters

**Old:**
- `min_price=10.0`
- `max_price=100.0`
- `min_market_cap=10_000_000_000`

**New:**
- All parameters default to `None` (no filtering)
- You must explicitly set filters

### 3. Browser Automation

**Old:** Used basic Playwright setup  
**New:** Uses playwright-stealth for better reliability

**Action Required:** Install Chromium browser:
```bash
playwright install chromium
```

### 4. Error Types

**Old:** Generic exceptions  
**New:** Specific exception types (ValidationError, AuthenticationError, etc.)

**Action Required:** Update exception handling if you catch specific errors.

## Deprecation Timeline

| Version | Status | Notes |
|---------|--------|-------|
| 1.0.0 | Current | YFinanceScreenerFetcher available with deprecation warnings |
| 1.x.x | Maintenance | Both APIs supported |
| 2.0.0 | Future | YFinanceScreenerFetcher will be removed |

## Testing Your Migration

### 1. Side-by-Side Comparison

Test both implementations to ensure equivalent results:

```python
# Old implementation
from yfinance_screener import YFinanceScreenerFetcher
old_fetcher = YFinanceScreenerFetcher()
old_results = old_fetcher.fetch_stocks(
    min_price=10,
    max_price=100,
    max_results=50
)

# New implementation
from yfinance_screener import Screener
new_screener = Screener()
new_results = new_screener.screen(
    min_price=10,
    max_price=100,
    max_results=50
)

# Compare
print(f"Old: {len(old_results)} results")
print(f"New: {len(new_results)} results")
print(f"Match: {set(old_results) == set(new_results)}")
```

### 2. Gradual Migration

Migrate one function at a time:

```python
# Step 1: Update imports
from yfinance_screener import Screener

# Step 2: Create wrapper function
def fetch_stocks_legacy(min_price, max_price, min_market_cap, max_results):
    """Legacy wrapper for old code"""
    screener = Screener()
    return screener.screen(
        min_price=min_price,
        max_price=max_price,
        min_market_cap=min_market_cap,
        max_results=max_results
    )

# Step 3: Replace old calls gradually
symbols = fetch_stocks_legacy(10, 100, 10_000_000_000, 50)
```

## Getting Help

If you encounter issues during migration:

1. Check the [API Reference](api_reference.md) for detailed documentation
2. Review the [Quick Start Guide](quickstart.md) for examples
3. Open an issue on GitHub with your migration question
4. Include code samples showing old and new implementations

## Benefits of Migrating

1. **More Filters**: Access to 15+ filter types vs. 3 in old version
2. **Better Performance**: Built-in caching and session reuse
3. **Improved Reliability**: playwright-stealth for better bot detection bypass
4. **Better Errors**: Specific exception types with helpful messages
5. **Type Hints**: Full type hint support for better IDE integration
6. **Active Development**: New features and bug fixes
7. **Better Documentation**: Comprehensive docs and examples

## Conclusion

While the legacy `YFinanceScreenerFetcher` class is available for backward compatibility, we strongly recommend migrating to the new `Screener` class to take advantage of new features and improvements.

The migration is straightforward - most code changes involve updating the class name and method calls. The new API is more flexible and powerful while maintaining simplicity for basic use cases.
