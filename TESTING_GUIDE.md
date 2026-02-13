# Testing Guide for yfinance-screener

## Quick Test Commands

### 1. Verify Package Installation

```bash
python -c "from yfinance_screener import Screener; print('✓ Package imported successfully')"
```

### 2. Test US Region Default (No Browser Required)

```bash
cd yfinance-screener
python test_us_default.py
```

Expected output should show:
```
✓ Region filter appears to be present
```

### 3. Test with Actual API Call (Requires Browser)

Create a test file `test_live.py`:

```python
from yfinance_screener import Screener

screener = Screener()

print("Testing US region default...")
df = screener.screen(
    min_price=10,
    max_price=100,
    max_results=10,
    as_dataframe=True
)

print("\nResults:")
print(df[['symbol', 'longName', 'regularMarketPrice']])

print("\nSymbols:", df['symbol'].tolist())

# Check for international symbols
symbols = df['symbol'].tolist()
international = [s for s in symbols if any(suffix in s for suffix in ['.SZ', '.DU', '.F', '.MU', '.SG'])]

if international:
    print(f"\n❌ FAIL: Found international symbols: {international}")
else:
    print("\n✅ PASS: All symbols are US stocks")
```

Run it:
```bash
python test_live.py
```

### 4. Test All Regions (Should Include International)

```python
from yfinance_screener import Screener

screener = Screener()

print("Testing all regions (empty list)...")
df = screener.screen(
    min_price=10,
    max_price=100,
    regions=[],  # Empty list = all regions
    max_results=10,
    as_dataframe=True
)

print("\nSymbols:", df['symbol'].tolist())

# Check for international symbols
symbols = df['symbol'].tolist()
international = [s for s in symbols if any(suffix in s for suffix in ['.SZ', '.DU', '.F', '.MU', '.SG'])]

if international:
    print(f"\n✅ PASS: Found international symbols as expected: {international}")
else:
    print("\n⚠️  WARNING: No international symbols found (might be due to filters)")
```

### 5. Test European Stocks

```python
from yfinance_screener import Screener

screener = Screener()

print("Testing European region...")
df = screener.screen(
    min_price=10,
    max_price=100,
    regions=["eu"],
    max_results=10,
    as_dataframe=True
)

print("\nSymbols:", df['symbol'].tolist())
print("\nExchanges:", df['exchange'].unique().tolist())
```

## Expected Results

### Default Behavior (US Only)
- ✅ Symbols like: `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `NVDA`
- ❌ NO symbols like: `000020.SZ`, `ZVR.DU`, `SAP.F`

### All Regions (Empty List)
- ✅ Mix of US and international symbols
- ✅ Symbols like: `AAPL`, `000020.SZ`, `ZVR.DU`, `SAP.F`

### European Region
- ✅ European exchange symbols
- ✅ Exchanges like: `FRA`, `PAR`, `LON`, `AMS`

## Troubleshooting

### Issue: "Playwright browser not found"
```bash
playwright install chromium
```

### Issue: "Authentication failed"
This is normal for Yahoo Finance. The package handles retries automatically.

### Issue: "No results returned"
Try adjusting your filters:
```python
# More lenient filters
df = screener.screen(
    min_price=1,
    max_price=1000,
    max_results=50,
    as_dataframe=True
)
```

### Issue: Still seeing international stocks with default settings
1. Verify you're using the latest version:
   ```bash
   pip show yfinance-screener
   ```
   Should show version 1.0.0

2. Reinstall:
   ```bash
   pip uninstall yfinance-screener
   pip install dist/yfinance_screener-1.0.0-py3-none-any.whl
   ```

3. Check the query being built:
   ```python
   from yfinance_screener import Screener
   screener = Screener()
   
   # This should show region filter
   from yfinance_screener.query_builder import QueryBuilder
   builder = QueryBuilder()
   builder.price(min=10, max=100)
   builder.region("us")
   print(builder.build())
   ```

## Performance Notes

- First run may be slower (browser initialization)
- Subsequent runs use cached results (default 1 hour TTL)
- Disable cache for testing: `Screener(cache_enabled=False)`

## Quick Verification Script

Save as `quick_test.py`:

```python
#!/usr/bin/env python3
from yfinance_screener import Screener

print("Quick verification test...")
screener = Screener(cache_enabled=False)

try:
    # Test with small result set
    symbols = screener.screen(
        min_price=50,
        max_price=200,
        min_market_cap=10_000_000_000,
        max_results=5
    )
    
    print(f"\n✅ SUCCESS: Found {len(symbols)} symbols")
    print(f"Symbols: {symbols}")
    
    # Check for international
    international = [s for s in symbols if '.' in s and s.split('.')[-1] in ['SZ', 'DU', 'F', 'MU', 'SG']]
    if international:
        print(f"\n❌ FAIL: Found international symbols: {international}")
        print("Expected: US stocks only")
    else:
        print("\n✅ PASS: All symbols are US stocks (no international suffixes)")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
```

Run it:
```bash
python quick_test.py
```
