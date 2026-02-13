# Filter Reference

Complete reference for all available filters in yfinance-screener.

## Overview

yfinance-screener supports all filters available on the Yahoo Finance web screener. Filters can be combined using AND logic (all conditions must be met), and categorical filters support OR logic (match any of the specified values).

## Price Filters

### Price

Filter stocks by current market price.

**Parameters:**
- `min_price` (float): Minimum price in dollars
- `max_price` (float): Maximum price in dollars

**Constraints:**
- Minimum value: $0.01
- No maximum limit

**Example:**

```python
# Stocks between $10 and $100
screener.screen(min_price=10, max_price=100)

# Stocks over $500
screener.screen(min_price=500)

# Using QueryBuilder
screener.query().price(min=10, max=100).execute()
```

## Market Capitalization Filters

### Market Cap

Filter stocks by market capitalization (total value of all shares).

**Parameters:**
- `min_market_cap` (float): Minimum market cap in dollars
- `max_market_cap` (float): Maximum market cap in dollars

**Constraints:**
- Minimum value: $0
- No maximum limit

**Common Values:**
- Mega Cap: > $200 billion
- Large Cap: $10 billion - $200 billion
- Mid Cap: $2 billion - $10 billion
- Small Cap: $300 million - $2 billion
- Micro Cap: $50 million - $300 million
- Nano Cap: < $50 million

**Example:**

```python
# Large cap stocks (> $10B)
screener.screen(min_market_cap=10_000_000_000)

# Mid cap stocks ($2B - $10B)
screener.screen(
    min_market_cap=2_000_000_000,
    max_market_cap=10_000_000_000
)

# Using QueryBuilder
screener.query().market_cap(min=10_000_000_000).execute()
```

## Volume Filters

### Volume

Filter stocks by trading volume (number of shares traded).

**Parameters:**
- `min_volume` (int): Minimum trading volume
- `max_volume` (int): Maximum trading volume

**Constraints:**
- Minimum value: 0
- No maximum limit

**Example:**

```python
# High volume stocks (> 1M shares/day)
screener.screen(min_volume=1_000_000)

# Moderate volume ($100K - $5M)
screener.screen(
    min_volume=100_000,
    max_volume=5_000_000
)

# Using QueryBuilder
screener.query().volume(min=1_000_000).execute()
```

## Valuation Filters

### P/E Ratio (Price-to-Earnings)

Filter stocks by trailing P/E ratio.

**Parameters:**
- `min_pe_ratio` (float): Minimum P/E ratio
- `max_pe_ratio` (float): Maximum P/E ratio

**Constraints:**
- No minimum or maximum limits
- Can be negative for companies with losses

**Interpretation:**
- Low P/E (< 15): Potentially undervalued or slow growth
- Medium P/E (15-25): Fair valuation
- High P/E (> 25): Growth expectations or overvalued

**Example:**

```python
# Value stocks (P/E < 15)
screener.screen(max_pe_ratio=15)

# Moderate P/E (10-20)
screener.screen(min_pe_ratio=10, max_pe_ratio=20)

# Using QueryBuilder
screener.query().pe_ratio(max=15).execute()
```

### P/B Ratio (Price-to-Book)

Filter stocks by price-to-book ratio.

**Parameters:**
- `min_pb_ratio` (float): Minimum P/B ratio
- `max_pb_ratio` (float): Maximum P/B ratio

**Constraints:**
- Minimum value: 0
- No maximum limit

**Interpretation:**
- P/B < 1: Trading below book value
- P/B 1-3: Reasonable valuation
- P/B > 3: Premium valuation

**Example:**

```python
# Stocks trading below book value
screener.screen(max_pb_ratio=1)

# Using QueryBuilder
screener.query().pb_ratio(max=3).execute()
```

### PEG Ratio (Price/Earnings-to-Growth)

Filter stocks by PEG ratio (P/E divided by growth rate).

**Parameters:**
- `min_peg_ratio` (float): Minimum PEG ratio
- `max_peg_ratio` (float): Maximum PEG ratio

**Constraints:**
- No minimum or maximum limits

**Interpretation:**
- PEG < 1: Potentially undervalued relative to growth
- PEG = 1: Fair valuation
- PEG > 1: Potentially overvalued relative to growth

**Example:**

```python
# Growth at reasonable price (PEG < 1)
screener.screen(max_peg_ratio=1)

# Using QueryBuilder
screener.query().peg_ratio(max=1.5).execute()
```

## Dividend Filters

### Dividend Yield

Filter stocks by dividend yield percentage.

**Parameters:**
- `min_dividend_yield` (float): Minimum dividend yield percentage
- `max_dividend_yield` (float): Maximum dividend yield percentage

**Constraints:**
- Minimum value: 0%
- Maximum value: 100%

**Interpretation:**
- 0%: No dividend
- 1-3%: Moderate dividend
- 3-6%: High dividend
- > 6%: Very high dividend (verify sustainability)

**Example:**

```python
# Dividend stocks (yield > 2%)
screener.screen(min_dividend_yield=2.0)

# High dividend (3-6%)
screener.screen(
    min_dividend_yield=3.0,
    max_dividend_yield=6.0
)

# Using QueryBuilder
screener.query().dividend_yield(min=2.0).execute()
```

## Growth Filters

### Revenue Growth

Filter stocks by revenue growth rate percentage.

**Parameters:**
- `min_revenue_growth` (float): Minimum revenue growth percentage
- `max_revenue_growth` (float): Maximum revenue growth percentage

**Constraints:**
- No minimum or maximum limits
- Can be negative for declining revenue

**Example:**

```python
# High growth (revenue > 20%)
screener.screen(min_revenue_growth=20)

# Using QueryBuilder
screener.query().revenue_growth(min=15).execute()
```

### Earnings Growth

Filter stocks by earnings growth rate percentage.

**Parameters:**
- `min_earnings_growth` (float): Minimum earnings growth percentage
- `max_earnings_growth` (float): Maximum earnings growth percentage

**Constraints:**
- No minimum or maximum limits
- Can be negative for declining earnings

**Example:**

```python
# Strong earnings growth (> 25%)
screener.screen(min_earnings_growth=25)

# Using QueryBuilder
screener.query().earnings_growth(min=20).execute()
```

## Profitability Filters

### Profit Margin

Filter stocks by profit margin percentage.

**Parameters:**
- `min_profit_margin` (float): Minimum profit margin percentage
- `max_profit_margin` (float): Maximum profit margin percentage

**Constraints:**
- Minimum value: 0%
- Maximum value: 100%

**Interpretation:**
- < 5%: Low margin business
- 5-10%: Moderate margin
- 10-20%: Good margin
- > 20%: Excellent margin

**Example:**

```python
# High margin businesses (> 15%)
screener.screen(min_profit_margin=15)

# Using QueryBuilder
screener.query().profit_margin(min=10).execute()
```

### ROE (Return on Equity)

Filter stocks by return on equity percentage.

**Parameters:**
- `min_roe` (float): Minimum ROE percentage
- `max_roe` (float): Maximum ROE percentage

**Constraints:**
- No minimum or maximum limits
- Can be negative for unprofitable companies

**Interpretation:**
- < 10%: Poor returns
- 10-15%: Average returns
- 15-20%: Good returns
- > 20%: Excellent returns

**Example:**

```python
# High ROE companies (> 15%)
screener.screen(min_roe=15)

# Using QueryBuilder
screener.query().roe(min=15).execute()
```

### ROA (Return on Assets)

Filter stocks by return on assets percentage.

**Parameters:**
- `min_roa` (float): Minimum ROA percentage
- `max_roa` (float): Maximum ROA percentage

**Constraints:**
- No minimum or maximum limits
- Can be negative for unprofitable companies

**Interpretation:**
- < 5%: Poor asset utilization
- 5-10%: Average utilization
- > 10%: Good asset utilization

**Example:**

```python
# Efficient asset use (ROA > 8%)
screener.screen(min_roa=8)

# Using QueryBuilder
screener.query().roa(min=5).execute()
```

## Categorical Filters

### Sector

Filter stocks by business sector. Multiple sectors use OR logic.

**Parameters:**
- `sectors` (List[str]): List of sector names

**Available Sectors:**
- Technology
- Healthcare
- Financial Services
- Consumer Cyclical
- Industrials
- Communication Services
- Consumer Defensive
- Energy
- Real Estate
- Basic Materials
- Utilities

**Example:**

```python
# Technology stocks only
screener.screen(sectors=["Technology"])

# Tech or Healthcare
screener.screen(sectors=["Technology", "Healthcare"])

# Using QueryBuilder
screener.query().sector("Technology", "Healthcare").execute()

# Get available sectors
sectors = screener.get_available_sectors()
```

### Industry

Filter stocks by business industry. Multiple industries use OR logic.

**Parameters:**
- `industries` (List[str]): List of industry names

**Note:** Yahoo Finance has hundreds of industries. Any industry string can be used.

**Common Industries:**
- Software—Application
- Software—Infrastructure
- Semiconductors
- Internet Content & Information
- Biotechnology
- Drug Manufacturers—General
- Medical Devices
- Banks—Regional
- Asset Management
- Auto Manufacturers
- Aerospace & Defense
- Oil & Gas E&P
- Utilities—Regulated Electric
- Real Estate—Diversified

**Example:**

```python
# Software companies
screener.screen(industries=["Software—Application"])

# Multiple industries
screener.screen(industries=[
    "Software—Application",
    "Software—Infrastructure"
])

# Using QueryBuilder
screener.query().industry("Biotechnology").execute()

# Get sample industries
industries = screener.get_available_industries()
```

### Region

Filter stocks by geographic region. Multiple regions use OR logic.

**Parameters:**
- `regions` (List[str]): List of region codes

**Available Regions:**
- `us` - United States
- `eu` - Europe
- `asia` - Asia
- `au` - Australia
- `ca` - Canada
- `gb` - United Kingdom

**Example:**

```python
# US stocks only
screener.screen(regions=["us"])

# US or European stocks
screener.screen(regions=["us", "eu"])

# Using QueryBuilder
screener.query().region("us").execute()

# Get available regions
regions = screener.get_available_regions()
```

### Exchange

Filter stocks by stock exchange. Multiple exchanges use OR logic.

**Parameters:**
- `exchanges` (List[str]): List of exchange codes

**Common Exchanges:**
- NMS - NASDAQ
- NYQ - NYSE
- ASE - NYSE American
- PCX - NYSE Arca

**Example:**

```python
# NASDAQ stocks only
screener.screen(exchanges=["NMS"])

# NYSE or NASDAQ
screener.screen(exchanges=["NYQ", "NMS"])

# Using QueryBuilder
screener.query().exchange("NMS").execute()
```

## Combining Filters

### AND Logic (Default)

All filters are combined with AND logic by default - stocks must match all criteria.

**Example:**

```python
# Must match ALL conditions
screener.screen(
    min_price=50,              # AND
    max_price=200,             # AND
    min_market_cap=10_000_000_000,  # AND
    max_pe_ratio=25,           # AND
    min_dividend_yield=2.0,    # AND
    sectors=["Technology"]     # AND
)
```

### OR Logic (Categorical Filters)

Categorical filters (sector, industry, region, exchange) use OR logic when multiple values are specified.

**Example:**

```python
# Match Technology OR Healthcare
screener.screen(
    sectors=["Technology", "Healthcare"]
)

# Match (Tech OR Healthcare) AND (price 10-100)
screener.screen(
    min_price=10,
    max_price=100,
    sectors=["Technology", "Healthcare"]
)
```

## Complex Query Examples

### Value Investing Screen

```python
# Find undervalued dividend stocks
screener.screen(
    max_pe_ratio=15,           # Low P/E
    max_pb_ratio=2,            # Low P/B
    min_dividend_yield=3.0,    # Good dividend
    min_market_cap=1_000_000_000,  # Established companies
    min_roe=10,                # Profitable
    as_dataframe=True
)
```

### Growth Investing Screen

```python
# Find high-growth tech stocks
screener.screen(
    min_revenue_growth=20,     # Strong revenue growth
    min_earnings_growth=15,    # Strong earnings growth
    sectors=["Technology"],
    min_market_cap=5_000_000_000,
    max_pe_ratio=40,           # Accept higher P/E for growth
    as_dataframe=True
)
```

### Dividend Aristocrats Screen

```python
# Find stable dividend payers
screener.screen(
    min_dividend_yield=2.5,
    min_market_cap=10_000_000_000,  # Large cap
    min_roe=15,                # Strong returns
    min_profit_margin=10,      # Healthy margins
    sectors=["Consumer Defensive", "Utilities"],
    as_dataframe=True
)
```

### Quality at Reasonable Price (QARP)

```python
# Find quality companies at fair prices
screener.screen(
    min_roe=15,                # Quality
    min_profit_margin=12,      # Quality
    max_pe_ratio=20,           # Reasonable price
    max_peg_ratio=1.5,         # Growth at reasonable price
    min_market_cap=5_000_000_000,
    as_dataframe=True
)
```

### Small Cap Growth

```python
# Find small cap growth opportunities
screener.screen(
    min_market_cap=300_000_000,    # Small cap
    max_market_cap=2_000_000_000,
    min_revenue_growth=25,     # High growth
    min_volume=500_000,        # Liquid enough
    regions=["us"],
    as_dataframe=True
)
```

## Result Sorting and Limiting

### Sorting

Control the order of results with `sort_by` and `sort_order`.

**Sort Fields:**
- `ticker` - Stock symbol (default)
- `price` - Current price
- `marketcap` - Market capitalization
- `volume` - Trading volume
- `peratio` - P/E ratio

**Sort Orders:**
- `asc` - Ascending (default)
- `desc` - Descending

**Example:**

```python
# Sort by market cap (largest first)
screener.screen(
    min_price=10,
    sort_by="marketcap",
    sort_order="desc"
)

# Using QueryBuilder
screener.query().price(min=10).sort_by("marketcap", "desc").execute()
```

### Limiting Results

Use `max_results` to limit the number of returned stocks.

**Example:**

```python
# Get top 50 results
screener.screen(
    min_price=10,
    max_results=50
)

# Using QueryBuilder
screener.query().price(min=10).limit(50).execute()
```

## Tips and Best Practices

1. **Start Broad, Then Narrow**: Begin with fewer filters and add more to refine results
2. **Use max_results**: Always set a limit for faster queries
3. **Combine Complementary Filters**: Use valuation + quality + growth filters together
4. **Check Available Values**: Use `get_available_sectors()` and similar methods to see valid options
5. **Validate Ranges**: Ensure min values are less than max values
6. **Consider Market Conditions**: Adjust P/E and growth expectations based on market environment
7. **Use DataFrame Output**: Set `as_dataframe=True` for easier analysis and sorting
8. **Cache Results**: Enable caching for repeated queries with same parameters
