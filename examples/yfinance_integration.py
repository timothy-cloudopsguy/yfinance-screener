"""
YFinance Integration Examples

This module demonstrates how to integrate yfinance-screener with the yfinance
library for comprehensive stock analysis workflows.
"""

from yfinance_screener import Screener

# Note: yfinance is not a dependency of yfinance-screener
# Install separately: pip install yfinance
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("Warning: yfinance not installed. Install with: pip install yfinance")


def example_1_screen_then_analyze():
    """Screen for stocks, then analyze with yfinance."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 1: Screen Then Analyze ===")
    
    # Step 1: Screen for interesting stocks
    screener = Screener()
    symbols = screener.screen(
        min_price=50,
        max_price=200,
        sectors=["Technology"],
        min_market_cap=10_000_000_000,
        max_results=5
    )
    
    print(f"Found {len(symbols)} tech stocks: {symbols}")
    
    # Step 2: Get detailed data with yfinance
    print("\nFetching detailed data with yfinance...")
    for symbol in symbols[:3]:  # Analyze first 3
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        print(f"\n{symbol}:")
        print(f"  Name: {info.get('longName', 'N/A')}")
        print(f"  Price: ${info.get('currentPrice', 'N/A')}")
        print(f"  Market Cap: ${info.get('marketCap', 0):,.0f}")
        print(f"  P/E Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"  52W High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")


def example_2_screen_and_download_history():
    """Screen stocks and download historical data."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 2: Screen and Download History ===")
    
    # Screen for dividend stocks
    screener = Screener()
    symbols = screener.screen(
        min_dividend_yield=3.0,
        min_market_cap=5_000_000_000,
        max_results=3
    )
    
    print(f"Found {len(symbols)} dividend stocks: {symbols}")
    
    # Download historical data
    print("\nDownloading 1-year price history...")
    data = yf.download(symbols, period="1y", progress=False)
    
    print("\nPrice summary:")
    print(data['Close'].describe())


def example_3_portfolio_builder():
    """Build a diversified portfolio using screening."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 3: Portfolio Builder ===")
    
    screener = Screener()
    portfolio = {}
    
    # Get tech stocks
    tech_stocks = screener.screen(
        sectors=["Technology"],
        min_market_cap=10_000_000_000,
        min_roe=15,
        max_results=2
    )
    portfolio['Technology'] = tech_stocks
    
    # Get healthcare stocks
    health_stocks = screener.screen(
        sectors=["Healthcare"],
        min_market_cap=10_000_000_000,
        min_roe=15,
        max_results=2
    )
    portfolio['Healthcare'] = health_stocks
    
    # Get financial stocks
    finance_stocks = screener.screen(
        sectors=["Financial Services"],
        min_market_cap=10_000_000_000,
        min_dividend_yield=2,
        max_results=2
    )
    portfolio['Financial Services'] = finance_stocks
    
    print("Diversified Portfolio:")
    for sector, stocks in portfolio.items():
        print(f"\n{sector}: {stocks}")
    
    # Get current prices
    all_symbols = [s for stocks in portfolio.values() for s in stocks]
    print(f"\nFetching current prices for {len(all_symbols)} stocks...")
    
    for symbol in all_symbols:
        ticker = yf.Ticker(symbol)
        price = ticker.info.get('currentPrice', 'N/A')
        print(f"  {symbol}: ${price}")


def example_4_fundamental_analysis():
    """Screen and perform fundamental analysis."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 4: Fundamental Analysis ===")
    
    # Screen for undervalued stocks
    screener = Screener()
    df = screener.screen(
        min_pe_ratio=5,
        max_pe_ratio=15,
        min_market_cap=1_000_000_000,
        max_results=3,
        as_dataframe=True
    )
    
    print("Screening results:")
    print(df[['symbol', 'name', 'pe', 'marketCap']])
    
    # Deep dive with yfinance
    print("\nDetailed fundamental analysis:")
    for symbol in df['symbol']:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        print(f"\n{symbol} - {info.get('longName', 'N/A')}")
        print(f"  P/E Ratio: {info.get('trailingPE', 'N/A'):.2f}")
        print(f"  P/B Ratio: {info.get('priceToBook', 'N/A')}")
        print(f"  Profit Margin: {info.get('profitMargins', 0) * 100:.2f}%")
        print(f"  ROE: {info.get('returnOnEquity', 0) * 100:.2f}%")
        print(f"  Debt/Equity: {info.get('debtToEquity', 'N/A')}")


def example_5_dividend_analysis():
    """Screen dividend stocks and analyze dividend history."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 5: Dividend Analysis ===")
    
    # Screen for dividend aristocrats
    screener = Screener()
    symbols = screener.screen(
        min_dividend_yield=2.5,
        min_market_cap=10_000_000_000,
        min_roe=12,
        max_results=3
    )
    
    print(f"Found {len(symbols)} dividend stocks: {symbols}")
    
    # Analyze dividend history
    print("\nDividend analysis:")
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        print(f"\n{symbol}:")
        print(f"  Dividend Yield: {info.get('dividendYield', 0) * 100:.2f}%")
        print(f"  Payout Ratio: {info.get('payoutRatio', 0) * 100:.2f}%")
        print(f"  5Y Avg Dividend Yield: {info.get('fiveYearAvgDividendYield', 'N/A')}")
        
        # Get dividend history
        dividends = ticker.dividends
        if not dividends.empty:
            print(f"  Last Dividend: ${dividends.iloc[-1]:.2f}")
            print(f"  Dividend Payments (last year): {len(dividends.last('1Y'))}")


def example_6_technical_screening():
    """Combine fundamental screening with technical analysis."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 6: Technical Screening ===")
    
    # Screen for fundamentally strong stocks
    screener = Screener()
    symbols = screener.screen(
        min_market_cap=5_000_000_000,
        min_roe=15,
        min_volume=1_000_000,
        max_results=5
    )
    
    print(f"Found {len(symbols)} fundamentally strong stocks")
    
    # Apply technical filters
    print("\nApplying technical analysis...")
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo")
        
        if hist.empty:
            continue
        
        current_price = hist['Close'].iloc[-1]
        high_52w = ticker.info.get('fiftyTwoWeekHigh', current_price)
        low_52w = ticker.info.get('fiftyTwoWeekLow', current_price)
        
        # Calculate position in 52-week range
        range_position = (current_price - low_52w) / (high_52w - low_52w) * 100
        
        print(f"\n{symbol}:")
        print(f"  Current: ${current_price:.2f}")
        print(f"  52W Range: ${low_52w:.2f} - ${high_52w:.2f}")
        print(f"  Position in range: {range_position:.1f}%")
        
        # Simple moving averages
        sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        
        print(f"  20-day SMA: ${sma_20:.2f}")
        print(f"  50-day SMA: ${sma_50:.2f}")
        print(f"  Trend: {'Bullish' if sma_20 > sma_50 else 'Bearish'}")


def example_7_sector_rotation():
    """Analyze sector performance for rotation strategy."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 7: Sector Rotation ===")
    
    screener = Screener()
    sectors = ["Technology", "Healthcare", "Financial Services", "Energy"]
    
    sector_leaders = {}
    
    # Find top stock in each sector
    for sector in sectors:
        stocks = screener.screen(
            sectors=[sector],
            min_market_cap=10_000_000_000,
            sort_by="marketcap",
            sort_order="desc",
            max_results=1
        )
        
        if stocks:
            sector_leaders[sector] = stocks[0]
    
    print("Sector leaders:")
    for sector, symbol in sector_leaders.items():
        print(f"  {sector}: {symbol}")
    
    # Compare performance
    print("\nComparing 3-month performance...")
    for sector, symbol in sector_leaders.items():
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo")
        
        if not hist.empty:
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            return_pct = (end_price - start_price) / start_price * 100
            
            print(f"  {sector} ({symbol}): {return_pct:+.2f}%")


def example_8_value_vs_growth():
    """Compare value and growth stocks."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 8: Value vs Growth ===")
    
    screener = Screener()
    
    # Screen for value stocks
    value_stocks = screener.screen(
        max_pe_ratio=15,
        min_dividend_yield=2,
        min_market_cap=5_000_000_000,
        max_results=3
    )
    
    # Screen for growth stocks
    growth_stocks = screener.screen(
        min_revenue_growth=20,
        min_earnings_growth=25,
        min_market_cap=5_000_000_000,
        max_results=3
    )
    
    print(f"Value stocks: {value_stocks}")
    print(f"Growth stocks: {growth_stocks}")
    
    # Compare metrics
    print("\nValue stock metrics:")
    for symbol in value_stocks:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        print(f"  {symbol}: P/E={info.get('trailingPE', 'N/A'):.1f}, "
              f"Div Yield={info.get('dividendYield', 0) * 100:.2f}%")
    
    print("\nGrowth stock metrics:")
    for symbol in growth_stocks:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        print(f"  {symbol}: Rev Growth={info.get('revenueGrowth', 0) * 100:.1f}%, "
              f"P/E={info.get('trailingPE', 'N/A')}")


def example_9_options_screening():
    """Screen stocks suitable for options trading."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 9: Options Screening ===")
    
    # Screen for liquid stocks suitable for options
    screener = Screener()
    symbols = screener.screen(
        min_price=20,
        max_price=500,
        min_volume=2_000_000,  # High liquidity
        min_market_cap=5_000_000_000,
        max_results=5
    )
    
    print(f"Found {len(symbols)} liquid stocks for options trading")
    
    # Check options availability
    print("\nChecking options availability:")
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        
        try:
            options_dates = ticker.options
            if options_dates:
                print(f"\n{symbol}:")
                print(f"  Current Price: ${ticker.info.get('currentPrice', 'N/A')}")
                print(f"  Volume: {ticker.info.get('volume', 0):,}")
                print(f"  Options Expiration Dates: {len(options_dates)}")
                print(f"  Next Expiration: {options_dates[0]}")
        except Exception as e:
            print(f"  {symbol}: No options data available")


def example_10_watchlist_builder():
    """Build and monitor a watchlist."""
    if not HAS_YFINANCE:
        print("Skipping example - yfinance not installed")
        return
    
    print("\n=== Example 10: Watchlist Builder ===")
    
    screener = Screener()
    
    # Build watchlist with different criteria
    watchlist = []
    
    # Add value stocks
    value = screener.screen(
        max_pe_ratio=15,
        min_market_cap=5_000_000_000,
        max_results=2
    )
    watchlist.extend(value)
    
    # Add growth stocks
    growth = screener.screen(
        min_revenue_growth=20,
        min_market_cap=5_000_000_000,
        max_results=2
    )
    watchlist.extend(growth)
    
    # Add dividend stocks
    dividend = screener.screen(
        min_dividend_yield=3,
        min_market_cap=5_000_000_000,
        max_results=2
    )
    watchlist.extend(dividend)
    
    # Remove duplicates
    watchlist = list(set(watchlist))
    
    print(f"Watchlist ({len(watchlist)} stocks): {watchlist}")
    
    # Get current snapshot
    print("\nCurrent snapshot:")
    for symbol in watchlist:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        print(f"\n{symbol} - {info.get('longName', 'N/A')}")
        print(f"  Price: ${info.get('currentPrice', 'N/A')}")
        print(f"  Change: {info.get('regularMarketChangePercent', 0):.2f}%")
        print(f"  Volume: {info.get('volume', 0):,}")


if __name__ == "__main__":
    print("=" * 60)
    print("YFinance Screener - Integration Examples")
    print("=" * 60)
    
    if not HAS_YFINANCE:
        print("\nNote: These examples require yfinance to be installed.")
        print("Install with: pip install yfinance")
        print("\nShowing example structure only...\n")
    
    # Run all examples
    # Note: Comment out examples you don't want to run
    
    example_1_screen_then_analyze()
    example_2_screen_and_download_history()
    example_3_portfolio_builder()
    example_4_fundamental_analysis()
    example_5_dividend_analysis()
    example_6_technical_screening()
    example_7_sector_rotation()
    example_8_value_vs_growth()
    example_9_options_screening()
    example_10_watchlist_builder()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
