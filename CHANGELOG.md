# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial package structure and configuration
- Core package modules (to be implemented)
- Comprehensive documentation
- Unit and integration test framework

## [1.0.0] - TBD

### Added
- Complete Yahoo Finance screener filter support
- Simple parameter-based screening interface
- Advanced QueryBuilder with fluent interface
- YFinance-compatible data structures (DataFrame and list outputs)
- Smart caching with configurable TTL
- Robust error handling with custom exceptions
- Session management with automatic crumb extraction
- Pagination support for large result sets
- Geographic market support (US, EU, Asia, etc.)
- Backward compatibility layer for legacy yfinance_screener_fetcher users
- Type hints for all public APIs
- Comprehensive documentation and examples

### Features
- Filter by price, market cap, volume, P/E ratio, dividends, and more
- Filter by sectors, industries, regions, and exchanges
- Support for valuation, growth, and profitability metrics
- Automatic browser session management with playwright-stealth
- Result caching to minimize API calls
- DataFrame output compatible with yfinance library
- Legacy API support for smooth migration

### Documentation
- Installation and quick start guide
- Complete API reference
- Filter reference with all available options
- Migration guide from yfinance_screener_fetcher
- Usage examples for common scenarios

### Testing
- Unit tests for core functionality
- Integration tests with mocked API responses
- 80%+ code coverage

[Unreleased]: https://github.com/yourusername/yfinance-screener/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/yfinance-screener/releases/tag/v1.0.0
