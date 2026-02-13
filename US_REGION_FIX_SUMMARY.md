# US Region Default Fix - Summary

## Problem
After installing the package locally, users were getting international stocks (Chinese .SZ, German .DU/.F/.MU, etc.) instead of US stocks when screening without specifying a region.

Example of problematic output:
```
symbol
0     000020.SZ  # Chinese stock
1     000021.SZ  # Chinese stock
2     000028.SZ  # Chinese stock
3     ZVR.DU     # German stock
4     ZVR.F      # German stock
5     ZYME       # US stock
```

## Root Cause
The screener was not applying any default region filter, causing it to return stocks from all regions globally when users didn't explicitly specify `regions` parameter.

## Solution Implemented

### 1. Code Changes

**File**: `yfinance-screener/src/yfinance_screener/screener.py`

Added default US region logic in the `screen()` method:

```python
# Default to US region if no regions specified
if regions is None:
    builder.region("us")
elif regions:
    builder.region(*regions)
```

**Behavior**:
- `regions=None` (default): Filters to US stocks only
- `regions=[]` (empty list): Searches all regions globally
- `regions=["eu"]`: Searches specific region(s)

### 2. Documentation Updates

**README.md**:
- Added "US Stocks by Default" to features list
- Added "Region Filtering" section with examples
- Updated docstrings to document default behavior

**New Example**: `examples/region_filtering.py`
- Demonstrates default US behavior
- Shows how to search other regions
- Shows how to search all regions globally

### 3. Verification

Created `test_us_default.py` to verify the fix:

```bash
$ python test_us_default.py
Test 1: Using screen() method (should default to US)
Query with default US region:
{'query': {'operator': 'AND', 'operands': [
    {'operator': 'BTWN', 'operands': ['intradayprice', 10, 100]}, 
    {'operator': 'EQ', 'operands': ['region', 'us']}  # ✓ US filter added
]}}
✓ Region filter appears to be present
```

## Usage Examples

### Default Behavior (US stocks only)
```python
from yfinance_screener import Screener

screener = Screener()

# Returns only US stocks
symbols = screener.screen(min_price=10, max_price=100)
# Result: ['AAPL', 'MSFT', 'GOOGL', ...] (no .SZ, .DU, .F suffixes)
```

### Search Other Regions
```python
# European stocks
symbols = screener.screen(min_price=10, regions=["eu"])

# Multiple regions
symbols = screener.screen(min_price=10, regions=["us", "ca", "gb"])
```

### Search All Regions (Global)
```python
# Pass empty list to search all regions
symbols = screener.screen(min_price=10, regions=[])
# Result: ['AAPL', '000020.SZ', 'ZVR.DU', ...] (includes international)
```

## Available Regions

- `us` - United States (default)
- `eu` - Europe
- `asia` - Asia
- `au` - Australia
- `ca` - Canada
- `gb` - United Kingdom

## Testing Instructions

To test the fix with actual API calls:

```python
from yfinance_screener import Screener

screener = Screener()

# Test 1: Default should return only US stocks
df = screener.screen(
    min_price=10, 
    max_price=100, 
    max_results=10, 
    as_dataframe=True
)
print("US stocks:", df['symbol'].tolist())
# Expected: No .SZ, .DU, .F, .MU suffixes

# Test 2: Empty list should return international stocks
df = screener.screen(
    min_price=10, 
    max_price=100, 
    regions=[],  # All regions
    max_results=10, 
    as_dataframe=True
)
print("Global stocks:", df['symbol'].tolist())
# Expected: Mix of US and international symbols
```

## Package Status

- ✅ Fix implemented and tested
- ✅ Documentation updated
- ✅ Examples added
- ✅ Package rebuilt (v1.0.0)
- ✅ Distributions created:
  - `yfinance_screener-1.0.0-py3-none-any.whl`
  - `yfinance_screener-1.0.0.tar.gz`
- ✅ Ready for user testing

## Installation

To install the fixed version:

```bash
# Uninstall old version
pip uninstall yfinance-screener

# Install from local wheel
pip install yfinance-screener/dist/yfinance_screener-1.0.0-py3-none-any.whl

# Or install in editable mode for development
pip install -e yfinance-screener/
```

## Impact

This fix ensures the package behaves as most users expect:
- **Default**: US stocks only (most common use case)
- **Flexible**: Can still search international stocks when needed
- **Explicit**: Clear documentation on how to control region filtering

Users no longer need to remember to add `regions=["us"]` to every query to avoid getting international stocks mixed in with their results.
