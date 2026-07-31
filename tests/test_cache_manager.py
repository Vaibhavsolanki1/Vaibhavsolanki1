"""
Unit tests for Cache Manager (Phase 2)
"""

import time
from pathlib import Path

from scripts.cache_manager import CacheManager


def test_cache_miss(tmp_path: Path) -> None:
    """Verify cache miss for non-existent key."""
    cache = CacheManager(cache_dir=tmp_path)
    assert cache.get("missing_key") is None


def test_cache_set_and_get(tmp_path: Path) -> None:
    """Verify writing and reading cache data."""
    cache = CacheManager(cache_dir=tmp_path)
    payload = {"data": [1, 2, 3], "status": "ok"}

    cache.set("test_key", payload)
    retrieved = cache.get("test_key", ttl=100)

    assert retrieved == payload


def test_cache_ttl_expiration(tmp_path: Path) -> None:
    """Verify cache item expires when TTL is exceeded."""
    cache = CacheManager(cache_dir=tmp_path)
    cache.set("expire_key", {"foo": "bar"})

    # Wait briefly and check with TTL 0
    time.sleep(0.1)
    assert cache.get("expire_key", ttl=0) is None


def test_cache_clear(tmp_path: Path) -> None:
    """Verify clear method deletes cache files."""
    cache = CacheManager(cache_dir=tmp_path)
    cache.set("key1", {"a": 1})
    cache.set("key2", {"b": 2})

    cache.clear("key1")
    assert cache.get("key1") is None
    assert cache.get("key2") is not None

    cache.clear()
    assert cache.get("key2") is None
