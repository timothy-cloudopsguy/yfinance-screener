# API Reference

Complete API documentation for yfinance-screener.

## Screener Class

The main interface for stock screening.

### Constructor

```python
Screener(
    cache_enabled: bool = True,
    cache_ttl: int = 3600,
    headless: bool = True
)
```

Initialize a new Screener instance.

**Parameters:**

- `cache_enabled` (bool, optional): Enable result caching. Default: `True`
- `cache_ttl` (int, optional): Cache time-to-live in seconds. Default: `3600` (1 hour)
- `headless` (bool, optional): Run browser in headless mode. Default: `True`

**Example:**

```python
from yfinance_screener import Screener

# Default configuration
screener = Screener()

# Custom configuration
screener = Screener(
    cache_enabled=True,
    cache_ttl=7200,  # 2 hours
    headless=True
)
```

### screen()

```python
screen(
    *,
    # Price filters
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    
    # Market cap filters
    min_market_cap: Optional[float] = None,
    max_market_cap: Optional[float] = None,
    
    # Volume filters
    min_volume: Optional[int] = None,
    max_volume: Optional[int] = None,
    
    # Valuation filters
    min_pe_ratio: Optional[float] = None,
    max_pe_ratio: Optional[float] = None,
    min_pb_ratio: Optional[float] = None,
    max_pb_ratio: Optional[float] = None,
    min_peg_ratio: Optional[float] = None,
    max_peg_ratio: Optional[float] = None,
    
    # Dividend filters
    min_dividend_yield: Optional[float] = None,
    max_dividend_yield: Optional[float] = None,
    
    # Growth filters
    min_revenue_growth: Optional[float] = None,
    max_revenue_growth: Optional[float] = None,
    min_earnings_growth: Optional[float] = None,
    max_earnings_growth: Optional[float] = None,
    
    # Profitability filters
    min_profit_margin: Optional[float] = None,
    max_profit_margin: Optional[float] = None,
    min_roe: Optional[float] = None,
    max_roe: Optional[float] = None,
    min_roa: Optional[float] = None,
    max_roa: Optional[float] = None,
    
    # Categorical filters
    sectors: Optional[List[str]] = None,
    industries: Optional[List[str]] = None,
    regions: Optional[List[str]] = None,
    exchanges: Optional[List[str]] = None,
    
    # Result options
    max_results: Optional[int] = None,
    sort_by: str = "ticker",
    sort_order: str = "asc",
    
    # Output format
    as_dataframe: bool = False
) -> Union[List[str], pd.DataFrame]
```

Screen stocks with specified filters.

**Parameters:**

**Price Filters:**
- `min_price` (float, optional): Minimum stock price in dollars
- `max_price` (float, optional): Maximum stock price in dollars

**Market Cap Filters:**
- `min_market_cap` (float, optional): Minimum market capitalization in dollars
- `max_market_cap` (float, optional): Maximum market capitalization in dollars

**Volume Filters:**
- `min_volume` (int, optional): Minimum trading volume
- `max_volume` (int, optional): Maximum trading volume

**Valuation Filters:**
- `min_pe_ratio` (float, optional): Minimum price-to-earnings ratio
- `max_pe_ratio` (float, optional): Maximum price-to-earnings ratio
- `min_pb_ratio` (float, optional): Minimum price-to-book ratio
- `max_pb_ratio` (float, optional): Maximum price-to-book ratio
- `min_peg_ratio` (float, optional): Minimum PEG ratio
- `max_peg_ratio` (float, optional): Maximum PEG ratio

**Dividend Filters:**
- `min_dividend_yield` (float, optional): Minimum dividend yield percentage
- `max_dividend_yield` (float, optional): Maximum dividend yield percentage

**Growth Filters:**
- `min_revenue_growth` (float, optional): Minimum revenue growth percentage
- `max_revenue_growth` (float, optional): Maximum revenue growth percentage
- `min_earnings_growth` (float, optional): Minimum earnings growth percentage
- `max_earnings_growth` (float, optional): Maximum earnings growth percentage

**Profitability Filters:**
- `min_profit_margin` (float, optional): Minimum profit margin percentage
- `max_profit_margin` (float, optional): Maximum profit margin percentage
- `min_roe` (float, optional): Minimum return on equity percentage
- `max_roe` (float, optional): Maximum return on equity percentage
- `min_roa` (float, optional): Minimum return on assets percentage
- `max_roa` (float, optional): Maximum return on assets percentage

**Categorical Filters:**
- `sectors` (List[str], optional): List of sectors to include (OR logic)
- `industries` (List[str], optional): List of industries to include (OR logic)
- `regions` (List[str], optional): List of regions to include (OR logic)
- `exchanges` (List[str], optional): List of exchanges to include (OR logic)

**Result Options:**
- `max_results` (int, optional): Maximum number of results to return
- `sort_by` (str, optional): Field to sort by. Default: `"ticker"`
- `sort_order` (str, optional): Sort order (`"asc"` or `"desc"`). Default: `"asc"`

**Output Format:**
- `as_dataframe` (bool, optional): Return pandas DataFrame instead of symbol list. Default: `False`

**Returns:**

- `List[str]`: List of ticker symbols (if `as_dataframe=False`)
- `pd.DataFrame`: DataFrame with detailed stock data (if `as_dataframe=True`)

**Raises:**

- `ValidationError`: If filter parameters are invalid
- `AuthenticationError`: If Yahoo Finance authentication fails
- `NetworkError`: If network communication fails
- `ResponseError`: If API response is unexpected

**Example:**

```python
# Simple screening
symbols = screener.screen(
    min_price=10,
    max_price=100,
    min_market_cap=1_000_000_000
)

# Complex screening with DataFrame output
df = screener.screen(
    min_price=50,
    max_pe_ratio=20,
    min_dividend_yield=2.0,
    sectors=["Technology", "Healthcare"],
    max_results=50,
    as_dataframe=True
)
```

### query()

```python
query() -> QueryBuilder
```

Get a QueryBuilder for advanced query construction.

**Returns:**

- `QueryBuilder`: QueryBuilder instance for fluent query building

**Example:**

```python
query = screener.query()
results = (query
    .price(min=10, max=100)
    .sector("Technology")
    .execute())
```

### get_available_sectors()

```python
get_available_sectors() -> List[str]
```

Get list of available sector values.

**Returns:**

- `List[str]`: List of sector names

**Example:**

```python
sectors = screener.get_available_sectors()
print(sectors)
# ['Technology', 'Healthcare', 'Financial Services', ...]
```

### get_available_industries()

```python
get_available_industries() -> List[str]
```

Get list of available industry values.

**Returns:**

- `List[str]`: List of common industry names

**Note:** Yahoo Finance has hundreds of industries. This method returns a representative sample.

**Example:**

```python
industries = screener.get_available_industries()
print(industries)
```

### get_available_regions()

```python
get_available_regions() -> List[str]
```

Get list of available region values.

**Returns:**

- `List[str]`: List of region codes

**Example:**

```python
regions = screener.get_available_regions()
print(regions)
# ['us', 'eu', 'asia', 'au', 'ca', 'gb']
```

## QueryBuilder Class

Fluent interface for building complex screening queries.

### Constructor

```python
QueryBuilder()
```

Create a new QueryBuilder instance. Typically created via `Screener.query()`.

**Example:**

```python
screener = Screener()
builder = screener.query()
```

### Filter Methods

All filter methods return `self` for method chaining.

#### price()

```python
price(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add price range filter.

**Parameters:**
- `min` (float, optional): Minimum price in dollars
- `max` (float, optional): Maximum price in dollars

**Example:**

```python
builder.price(min=10, max=100)
```

#### market_cap()

```python
market_cap(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add market capitalization filter.

**Parameters:**
- `min` (float, optional): Minimum market cap in dollars
- `max` (float, optional): Maximum market cap in dollars

**Example:**

```python
builder.market_cap(min=1_000_000_000, max=100_000_000_000)
```

#### volume()

```python
volume(min: Optional[int] = None, max: Optional[int] = None) -> QueryBuilder
```

Add trading volume filter.

**Parameters:**
- `min` (int, optional): Minimum volume
- `max` (int, optional): Maximum volume

**Example:**

```python
builder.volume(min=1_000_000)
```

#### pe_ratio()

```python
pe_ratio(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add price-to-earnings ratio filter.

**Parameters:**
- `min` (float, optional): Minimum P/E ratio
- `max` (float, optional): Maximum P/E ratio

**Example:**

```python
builder.pe_ratio(min=10, max=25)
```

#### pb_ratio()

```python
pb_ratio(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add price-to-book ratio filter.

**Parameters:**
- `min` (float, optional): Minimum P/B ratio
- `max` (float, optional): Maximum P/B ratio

**Example:**

```python
builder.pb_ratio(max=3)
```

#### peg_ratio()

```python
peg_ratio(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add PEG ratio filter.

**Parameters:**
- `min` (float, optional): Minimum PEG ratio
- `max` (float, optional): Maximum PEG ratio

**Example:**

```python
builder.peg_ratio(max=2)
```

#### dividend_yield()

```python
dividend_yield(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add dividend yield filter.

**Parameters:**
- `min` (float, optional): Minimum dividend yield percentage
- `max` (float, optional): Maximum dividend yield percentage

**Example:**

```python
builder.dividend_yield(min=2.0, max=8.0)
```

#### revenue_growth()

```python
revenue_growth(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add revenue growth filter.

**Parameters:**
- `min` (float, optional): Minimum revenue growth percentage
- `max` (float, optional): Maximum revenue growth percentage

**Example:**

```python
builder.revenue_growth(min=15)
```

#### earnings_growth()

```python
earnings_growth(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add earnings growth filter.

**Parameters:**
- `min` (float, optional): Minimum earnings growth percentage
- `max` (float, optional): Maximum earnings growth percentage

**Example:**

```python
builder.earnings_growth(min=20)
```

#### profit_margin()

```python
profit_margin(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add profit margin filter.

**Parameters:**
- `min` (float, optional): Minimum profit margin percentage
- `max` (float, optional): Maximum profit margin percentage

**Example:**

```python
builder.profit_margin(min=10)
```

#### roe()

```python
roe(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add return on equity filter.

**Parameters:**
- `min` (float, optional): Minimum ROE percentage
- `max` (float, optional): Maximum ROE percentage

**Example:**

```python
builder.roe(min=15)
```

#### roa()

```python
roa(min: Optional[float] = None, max: Optional[float] = None) -> QueryBuilder
```

Add return on assets filter.

**Parameters:**
- `min` (float, optional): Minimum ROA percentage
- `max` (float, optional): Maximum ROA percentage

**Example:**

```python
builder.roa(min=5)
```

#### sector()

```python
sector(*sectors: str) -> QueryBuilder
```

Add sector filter (OR logic for multiple sectors).

**Parameters:**
- `*sectors` (str): One or more sector names

**Example:**

```python
builder.sector("Technology", "Healthcare")
```

#### industry()

```python
industry(*industries: str) -> QueryBuilder
```

Add industry filter (OR logic for multiple industries).

**Parameters:**
- `*industries` (str): One or more industry names

**Example:**

```python
builder.industry("Software—Application", "Biotechnology")
```

#### region()

```python
region(*regions: str) -> QueryBuilder
```

Add region filter (OR logic for multiple regions).

**Parameters:**
- `*regions` (str): One or more region codes

**Example:**

```python
builder.region("us", "eu")
```

#### exchange()

```python
exchange(*exchanges: str) -> QueryBuilder
```

Add exchange filter (OR logic for multiple exchanges).

**Parameters:**
- `*exchanges` (str): One or more exchange codes

**Example:**

```python
builder.exchange("NMS", "NYQ")
```

### Control Methods

#### sort_by()

```python
sort_by(field: str, order: str = "asc") -> QueryBuilder
```

Set sort field and order.

**Parameters:**
- `field` (str): Field to sort by (e.g., `"ticker"`, `"price"`, `"marketcap"`)
- `order` (str, optional): Sort order (`"asc"` or `"desc"`). Default: `"asc"`

**Example:**

```python
builder.sort_by("marketcap", "desc")
```

#### limit()

```python
limit(max_results: int) -> QueryBuilder
```

Limit number of results.

**Parameters:**
- `max_results` (int): Maximum number of results to return

**Example:**

```python
builder.limit(50)
```

### Execution Methods

#### build()

```python
build() -> Dict[str, Any]
```

Build and return the query dictionary.

**Returns:**

- `Dict[str, Any]`: Query dictionary ready for API submission

**Raises:**

- `ValidationError`: If query is invalid

**Example:**

```python
query_dict = builder.price(min=10).build()
```

#### execute()

```python
execute(as_dataframe: bool = False) -> Union[List[str], pd.DataFrame]
```

Execute the query and return results.

**Parameters:**
- `as_dataframe` (bool, optional): Return DataFrame instead of symbol list. Default: `False`

**Returns:**

- `List[str]`: List of ticker symbols (if `as_dataframe=False`)
- `pd.DataFrame`: DataFrame with detailed data (if `as_dataframe=True`)

**Example:**

```python
# Get symbols
symbols = builder.price(min=10).execute()

# Get DataFrame
df = builder.price(min=10).execute(as_dataframe=True)
```

## YFinanceScreenerFetcher Class (Legacy)

Legacy interface for backward compatibility.

**Deprecated:** Use `Screener` class instead.

### Constructor

```python
YFinanceScreenerFetcher()
```

Initialize fetcher (deprecated).

### fetch_stocks()

```python
fetch_stocks(
    min_price: float = 10.0,
    max_price: float = 100.0,
    min_market_cap: float = 10_000_000_000,
    max_results: Optional[int] = None
) -> List[str]
```

Fetch stock symbols (deprecated).

**Use `Screener.screen()` instead.**

### fetch_stocks_detailed()

```python
fetch_stocks_detailed(
    min_price: float = 10.0,
    max_price: float = 100.0,
    min_market_cap: float = 10_000_000_000,
    max_results: Optional[int] = None
) -> List[Dict[str, Any]]
```

Fetch detailed stock data (deprecated).

**Use `Screener.screen(as_dataframe=True)` instead.**

## Exceptions

### YFinanceScreenerError

Base exception for all package errors.

```python
class YFinanceScreenerError(Exception)
```

### ValidationError

Raised when filter validation fails.

```python
class ValidationError(YFinanceScreenerError)
```

**Example:**

```python
try:
    screener.screen(min_price=-10)  # Invalid
except ValidationError as e:
    print(f"Invalid parameter: {e}")
```

### AuthenticationError

Raised when authentication with Yahoo Finance fails.

```python
class AuthenticationError(YFinanceScreenerError)
```

### NetworkError

Raised when network communication fails.

```python
class NetworkError(YFinanceScreenerError)
```

### RateLimitError

Raised when rate limit is exceeded.

```python
class RateLimitError(YFinanceScreenerError)
```

**Attributes:**
- `retry_after` (int | None): Seconds to wait before retrying

**Example:**

```python
try:
    results = screener.screen(min_price=10)
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
```

### BrowserError

Raised when browser automation fails.

```python
class BrowserError(YFinanceScreenerError)
```

### ResponseError

Raised when API response format is unexpected.

```python
class ResponseError(YFinanceScreenerError)
```

## DataFrame Schema

When using `as_dataframe=True`, the returned DataFrame has the following columns:

| Column | Type | Description |
|--------|------|-------------|
| symbol | str | Stock ticker symbol |
| name | str | Company name |
| price | float | Current stock price |
| marketCap | float | Market capitalization |
| volume | int | Trading volume |
| avgVolume | int | Average volume |
| pe | float | Trailing P/E ratio |
| forwardPE | float | Forward P/E ratio |
| dividendYield | float | Dividend yield (as decimal) |
| sector | str | Business sector |
| industry | str | Business industry |
| exchange | str | Stock exchange |
| 52WeekHigh | float | 52-week high price |
| 52WeekLow | float | 52-week low price |

**Example:**

```python
df = screener.screen(min_price=10, as_dataframe=True)
print(df.columns)
# ['symbol', 'name', 'price', 'marketCap', 'volume', ...]
```
