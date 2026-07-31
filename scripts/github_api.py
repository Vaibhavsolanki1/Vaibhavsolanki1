"""
GitHub Profile 2.0 - GitHub GraphQL & REST API Client

Resilient API client for fetching GitHub profile metrics, contribution heatmaps,
language distributions, and repository data. Supports GraphQL API (with GITHUB_TOKEN)
and Public REST API fallback (unauthenticated) to guarantee real profile statistics.
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
GITHUB_REST_ENDPOINT = "https://api.github.com/users"


class GitHubAPIClient:
    """GitHub API Client supporting GraphQL and Public REST endpoints with disk caching."""

    def __init__(
        self,
        token: str | None = None,
        cache_manager: CacheManager | None = None,
        mock_fixture_path: Path | str = "tests/mock_github_data.json",
    ) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.cache = cache_manager or CacheManager()
        self.mock_fixture_path = Path(mock_fixture_path)

    def fetch_user_stats(
        self, username: str, mode: str = "live", ttl: int = 86400
    ) -> dict[str, Any]:
        """Fetch user statistics using GraphQL (if authenticated), Public REST API (fallback), or cache."""
        cache_key = f"github_user_stats_{username}"

        # 1. Explicit mock mode requested (e.g. unit tests)
        if mode == "mock":
            logger.info("Explicit mock mode requested. Using mock fixture.")
            return self._load_mock_fixture()

        # 2. Check disk cache
        if mode != "force_live":
            cached_data = self.cache.get(cache_key, ttl=ttl)
            if cached_data:
                logger.info(f"Loaded GitHub statistics for '{username}' from cache.")
                return cached_data

        # 3. Live GraphQL Query (Authenticated)
        if self.token:
            try:
                logger.info(f"Fetching live GraphQL statistics for '{username}'...")
                raw_response = self._execute_graphql(
                    GET_USER_STATS_QUERY, variables={"username": username}
                )
                normalized = self._normalize_user_stats(raw_response)
                self.cache.set(cache_key, normalized)
                return normalized
            except Exception as e:
                logger.warning(f"GraphQL request failed: {e}. Trying Public REST API fallback.")

        # 4. Public REST API Fallback (Unauthenticated real metrics)
        try:
            logger.info(f"Fetching public REST API metrics for '{username}'...")
            rest_stats = self._fetch_public_rest_stats(username)
            self.cache.set(cache_key, rest_stats)
            return rest_stats
        except Exception as e:
            logger.error(f"Public REST API request failed: {e}. Returning unavailable metrics.")
            return self._unavailable_user_stats(username)

    def _execute_graphql(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Execute HTTP POST request to GitHub GraphQL endpoint."""
        if not self.token:
            raise ValueError("GITHUB_TOKEN missing for GraphQL execution.")

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
                        raise RuntimeError(f"GraphQL query errors: {data['errors']}")
                    return data
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
                if attempt == max_attempts:
                    raise
                time.sleep(base_delay * (2 ** (attempt - 1)))

        raise RuntimeError("GraphQL execution exhausted retry limits.")

    def _fetch_public_rest_stats(self, username: str) -> dict[str, Any]:
        """Fetch real public user metrics via GitHub REST API without authentication."""
        user_url = f"{GITHUB_REST_ENDPOINT}/{username}"
        repos_url = f"{GITHUB_REST_ENDPOINT}/{username}/repos?per_page=100"

        headers = {"User-Agent": "GitHub-Profile-2.0-Engine"}

        user_req = urllib.request.Request(user_url, headers=headers)
        with urllib.request.urlopen(user_req, timeout=10) as response:
            user_data = json.loads(response.read().decode("utf-8"))

        repos_req = urllib.request.Request(repos_url, headers=headers)
        with urllib.request.urlopen(repos_req, timeout=10) as response:
            repos_data = json.loads(response.read().decode("utf-8"))

        total_stars = sum(r.get("stargazers_count", 0) for r in repos_data)

        # Aggregate language counts from public repos
        lang_counts: dict[str, int] = {}
        for r in repos_data:
            lang = r.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

        total_lang_repos = sum(lang_counts.values()) or 1
        sorted_langs = []

        # Color mapping for common languages
        lang_colors = {
            "Python": "#3572A5",
            "TypeScript": "#3178C6",
            "JavaScript": "#F1E05A",
            "HTML": "#E34C26",
            "CSS": "#563D7C",
            "C++": "#F34B7D",
            "C": "#555555",
            "Java": "#B07219",
        }

        for lang, count in sorted(lang_counts.items(), key=lambda item: item[1], reverse=True):
            pct = round((count / total_lang_repos) * 100, 1)
            color = lang_colors.get(lang, "#858585")
            sorted_langs.append({"name": lang, "color": color, "size": count, "percentage": pct})

        return {
            "name": user_data.get("name") or username,
            "username": username,
            "followers": user_data.get("followers", 0),
            "starred": total_stars,
            "total_commits": "Data unavailable",
            "total_prs": "Data unavailable",
            "total_issues": "Data unavailable",
            "total_contributions": "Data unavailable",
            "contribution_weeks": [],
            "languages": sorted_langs[:8],
            "repositories_count": user_data.get("public_repos", 0),
            "is_available": True,
        }

    def _load_mock_fixture(self) -> dict[str, Any]:
        """Load static mock fixture from disk (for unit testing)."""
        if not self.mock_fixture_path.exists():
            raise FileNotFoundError(f"Mock fixture missing at {self.mock_fixture_path}")
        with open(self.mock_fixture_path, encoding="utf-8") as f:
            raw: dict[str, Any] = json.load(f)
        return self._normalize_user_stats(raw)

    def _unavailable_user_stats(self, username: str) -> dict[str, Any]:
        """Return clean unauthenticated/unavailable metric payload without hardcoded fake numbers."""
        return {
            "name": username,
            "username": username,
            "followers": "Data unavailable",
            "starred": "Data unavailable",
            "total_commits": "Data unavailable",
            "total_prs": "Data unavailable",
            "total_issues": "Data unavailable",
            "total_contributions": "Data unavailable",
            "contribution_weeks": [],
            "languages": [],
            "repositories_count": "Data unavailable",
            "is_available": False,
        }

    def _normalize_user_stats(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Normalize raw GraphQL response dictionary into clean metrics structure."""
        user = raw_data.get("data", {}).get("user", {})
        contribs = user.get("contributionsCollection", {})
        calendar = contribs.get("contributionCalendar", {})

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
            "languages": sorted_languages[:8],
            "repositories_count": user.get("repositories", {}).get("totalCount", 0),
            "is_available": True,
        }
