"""
GitHub Profile 2.0 - Cache Manager

Disk storage and retrieval of temporary API responses with TTL expiration support.
"""

import json
import time
from pathlib import Path
from typing import Any

from scripts.logger import get_logger

logger = get_logger("CacheManager")


class CacheManager:
    """Manages disk-backed JSON cache files inside target cache directory."""

    def __init__(self, cache_dir: Path | str = "generated/cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        safe_key = "".join(c if c.isalnum() else "_" for c in key)
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str, ttl: int = 86400) -> dict[str, Any] | None:
        """Retrieve cached JSON payload if file exists and has not expired."""
        cache_file = self._get_cache_path(key)

        if not cache_file.exists():
            logger.debug(f"Cache miss for key: {key} (file absent)")
            return None

        file_age = time.time() - cache_file.stat().st_mtime
        if file_age > ttl:
            logger.debug(f"Cache expired for key: {key} (age {file_age:.0f}s > ttl {ttl}s)")
            return None

        try:
            with open(cache_file, encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)
                logger.debug(f"Cache hit for key: {key}")
                return data
        except Exception as e:
            logger.warning(f"Failed to read cache file {cache_file}: {e}")
            return None

    def set(self, key: str, data: dict[str, Any]) -> None:
        """Write JSON payload to disk cache file."""
        cache_file = self._get_cache_path(key)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Cache saved for key: {key}")
        except Exception as e:
            logger.error(f"Failed to write cache file {cache_file}: {e}")

    def clear(self, key: str | None = None) -> None:
        """Clear specific cache entry or purge entire cache directory."""
        if key:
            cache_file = self._get_cache_path(key)
            if cache_file.exists():
                cache_file.unlink()
        else:
            for item in self.cache_dir.glob("*.json"):
                item.unlink()
