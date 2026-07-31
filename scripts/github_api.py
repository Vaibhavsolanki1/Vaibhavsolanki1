"""
GitHub Profile 2.0 - GitHub GraphQL API Client

Resilient API client for fetching GitHub profile metrics, contribution heatmaps,
language distributions, and repository data with caching and mock fallbacks.
"""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from scripts.cache_manager import CacheManager
from scripts.graphql_queries import GET_USER_STATS_QUERY
from scripts.logger import get_logger

logger = get_logger("GitHubAPI")

GITHUB_GRAPHQL_ENDPOINT = "https://api.github.com/graphql"


class GitHubAPIClient:
    """GitHub GraphQL API Client with caching and retry logic."""

    def __init__(
        self,
        token: str | None = None,
        cache_manager: CacheManager | None = None,
        mock_fixture_path: Path | str = "tests/mock_github_data.json",
    ) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.cache = cache_manager or CacheManager()
        self.mock_fixture_path = Path(mock_fixture_path)

    def _execute_graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Execute HTTP POST request to GitHub GraphQL endpoint with retry logic."""
        if not self.token:
            raise ValueError("GITHUB_TOKEN missing. Live API query unavailable.")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "GitHub-Profile-2.0-Engine",
        }
        payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

        req = urllib.request.Request(
            GITHUB_GRAPHQL_ENDPOINT, data=payload, headers=headers, method="POST"
        )

        max_attempts = 3
        base_delay = 1.0

        for attempt in range(1, max_attempts + 1):
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_body = response.read().decode("utf-8")
                    data: dict[str, Any] = json.loads(res_body)
                    if "errors" in data:
                        logger.error(f"GraphQL error returned: {data['errors']}")
                        raise RuntimeError(
                            f"GitHub GraphQL query returned errors: {data['errors']}"
                        )
                    return data
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
                logger.warning(f"GraphQL request attempt {attempt}/{max_attempts} failed: {e}")
                if attempt == max_attempts:
                    raise
                time.sleep(base_delay * (2 ** (attempt - 1)))

        raise RuntimeError("GraphQL execution exhausted retry limits.")

    def fetch_user_stats(
        self, username: str, mode: str = "live", ttl: int = 86400
    ) -> dict[str, Any]:
        """Fetch user statistics with caching, mode checking, and mock fallback."""
        cache_key = f"github_user_stats_{username}"

        # 1. Check cache first
        if mode != "force_live":
            cached_data = self.cache.get(cache_key, ttl=ttl)
            if cached_data:
                logger.info(f"Loaded GitHub statistics for '{username}' from cache.")
                return cached_data

        # 2. Check if mock mode requested or token absent
        if mode == "mock" or not self.token:
            logger.info("Using mock/cached fixture for GitHub stats data.")
            return self._load_mock_fixture()

        # 3. Live GraphQL query
        try:
            logger.info(f"Fetching live GitHub GraphQL statistics for '{username}'...")
            raw_response = self._execute_graphql(
                GET_USER_STATS_QUERY, variables={"username": username}
            )
            normalized = self._normalize_user_stats(raw_response)
            self.cache.set(cache_key, normalized)
            return normalized
        except Exception as e:
            logger.error(f"Live API request failed: {e}. Falling back to mock fixture.")
            return self._load_mock_fixture()

    def _load_mock_fixture(self) -> dict[str, Any]:
        """Load static mock fixture from disk."""
        if not self.mock_fixture_path.exists():
            raise FileNotFoundError(f"Mock fixture missing at {self.mock_fixture_path}")
        with open(self.mock_fixture_path, encoding="utf-8") as f:
            raw: dict[str, Any] = json.load(f)
        return self._normalize_user_stats(raw)

    def _normalize_user_stats(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Normalize raw GraphQL response dictionary into clean metrics structure."""
        user = raw_data.get("data", {}).get("user", {})
        contribs = user.get("contributionsCollection", {})
        calendar = contribs.get("contributionCalendar", {})

        # Normalize Language Totals
        languages_map: dict[str, dict[str, Any]] = {}
        repos = user.get("repositories", {}).get("nodes", [])

        for repo in repos:
            edges = repo.get("languages", {}).get("edges", [])
            for edge in edges:
                name = edge["node"]["name"]
                color = edge["node"].get("color", "#858585")
                size = edge.get("size", 0)

                if name not in languages_map:
                    languages_map[name] = {"name": name, "color": color, "size": 0}
                languages_map[name]["size"] += size

        sorted_languages = sorted(languages_map.values(), key=lambda x: x["size"], reverse=True)
        total_bytes = sum(lang["size"] for lang in sorted_languages) or 1

        for lang in sorted_languages:
            lang["percentage"] = round((lang["size"] / total_bytes) * 100, 1)

        return {
            "name": user.get("name", ""),
            "username": user.get("login", ""),
            "followers": user.get("followers", {}).get("totalCount", 0),
            "starred": user.get("starredRepositories", {}).get("totalCount", 0),
            "total_commits": contribs.get("totalCommitContributions", 0),
            "total_prs": contribs.get("totalPullRequestContributions", 0),
            "total_issues": contribs.get("totalIssueContributions", 0),
            "total_contributions": calendar.get("totalContributions", 0),
            "contribution_weeks": calendar.get("weeks", []),
            "languages": sorted_languages[:8],  # Top 8 languages
            "repositories_count": user.get("repositories", {}).get("totalCount", 0),
        }
