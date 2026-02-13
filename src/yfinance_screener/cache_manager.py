"""
Cache manager for screener results with TTL support.

This module provides file-based caching for screener results with
time-to-live (TTL) expiration support.

The CacheManager class handles:
- File-based cache storage as JSON
- TTL-based expiration
- Query hashing for cache keys
- Cache cleanup operations

Example:
    Using CacheManager directly (advanced usage)::

        from yfinance_screener.cache_manager import CacheManager

        cache = CacheManager(ttl=3600)  # 1 hour TTL

        # Cache results
        query_hash = CacheManager.hash_query(query_dict)
        cache.set(query_hash, results)

        # Retrieve cached results
        cached = cache.get(query_hash)
"""

import contextlib
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class CacheManager:
    """
    Manages caching of screener results.

    Uses file-based caching with TTL (time-to-live) support.
    Cache files are stored as JSON with metadata including timestamp.
    """

    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = 3600):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache files (default: ~/.yfinance_screener/cache)
            ttl: Time-to-live in seconds (default: 3600 = 1 hour)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".yfinance_screener" / "cache"

        self.cache_dir = Path(cache_dir)
        self.ttl = ttl

        # Create cache directory if it doesn't exist
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, query_hash: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached results for a query.

        Args:
            query_hash: Hash of the query (from hash_query method)

        Returns:
            Cached results or None if not found/expired
        """
        cache_file = self.cache_dir / f"{query_hash}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, encoding="utf-8") as f:
                cache_data = json.load(f)

            # Check if cache is expired
            timestamp = cache_data.get("timestamp", 0)
            if time.time() - timestamp > self.ttl:
                # Cache expired, remove it
                cache_file.unlink(missing_ok=True)
                return None

            results: Optional[List[Dict[str, Any]]] = cache_data.get("results")
            return results

        except (json.JSONDecodeError, KeyError, OSError):
            # If cache file is corrupted or unreadable, remove it
            cache_file.unlink(missing_ok=True)
            return None

    def set(self, query_hash: str, results: List[Dict[str, Any]]) -> None:
        """
        Cache results for a query.

        Args:
            query_hash: Hash of the query (from hash_query method)
            results: List of stock dictionaries to cache
        """
        cache_file = self.cache_dir / f"{query_hash}.json"

        cache_data = {"timestamp": time.time(), "results": results}

        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except OSError:
            # If we can't write to cache, silently fail
            # (caching is optional, shouldn't break the application)
            pass

    def clear(self) -> None:
        """Clear all cached results."""
        if not self.cache_dir.exists():
            return

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except OSError:
                # Continue even if some files can't be deleted
                pass

    def clear_expired(self) -> None:
        """Remove expired cache entries."""
        if not self.cache_dir.exists():
            return

        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, encoding="utf-8") as f:
                    cache_data = json.load(f)

                timestamp = cache_data.get("timestamp", 0)
                if current_time - timestamp > self.ttl:
                    cache_file.unlink()

            except (json.JSONDecodeError, KeyError, OSError):
                # If file is corrupted or unreadable, remove it
                with contextlib.suppress(OSError):
                    cache_file.unlink()

    @staticmethod
    def hash_query(query: Dict[str, Any]) -> str:
        """
        Generate hash for a query dictionary.

        Creates a deterministic hash based on the query structure.
        The hash is used as the cache key.

        Args:
            query: Query dictionary to hash

        Returns:
            Hexadecimal hash string
        """
        # Convert query to a canonical JSON string for consistent hashing
        query_str = json.dumps(query, sort_keys=True, separators=(",", ":"))

        # Generate SHA256 hash
        hash_obj = hashlib.sha256(query_str.encode("utf-8"))

        return hash_obj.hexdigest()
