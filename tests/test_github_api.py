"""
Unit tests for GitHub GraphQL API Client (Phase 4)
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.cache_manager import CacheManager
from scripts.github_api import GitHubAPIClient


def test_github_api_mock_fallback(tmp_path: Path) -> None:
    """Verify API client loads mock fixture when mode='mock' explicitly."""
    cache = CacheManager(cache_dir=tmp_path)
    client = GitHubAPIClient(
        token=None, cache_manager=cache, mock_fixture_path="tests/mock_github_data.json"
    )

    stats = client.fetch_user_stats("vaibhavsolanki1", mode="mock")

    assert stats["username"] == "vaibhavsolanki1"
    assert stats["total_commits"] == 412
    assert len(stats["languages"]) >= 1
    assert stats["languages"][0]["name"] == "Python"


def test_github_api_unauthenticated_fallback(tmp_path: Path) -> None:
    """Verify unauthenticated client returns unavailable state without hardcoded fake stats."""
    cache = CacheManager(cache_dir=tmp_path)
    client = GitHubAPIClient(token=None, cache_manager=cache)

    stats = client.fetch_user_stats("vaibhavsolanki1", mode="live")

    assert stats["username"] == "vaibhavsolanki1"
    assert stats["total_commits"] == "Data unavailable"
    assert stats["followers"] == "Data unavailable"
    assert stats["is_available"] is False


def test_github_api_normalization() -> None:
    """Verify raw GraphQL response normalization logic."""
    client = GitHubAPIClient(token=None)
    mock_data = client._load_mock_fixture()

    assert "total_contributions" in mock_data
    assert "contribution_weeks" in mock_data
    assert isinstance(mock_data["languages"], list)
    assert mock_data["languages"][0]["percentage"] > 0


@patch("urllib.request.urlopen")
def test_github_api_live_execution(mock_urlopen: MagicMock, tmp_path: Path) -> None:
    """Verify GraphQL HTTP POST request execution and parsing."""
    mock_response = MagicMock()
    mock_response.__enter__.return_value.read.return_value = (
        Path("tests/mock_github_data.json").read_text(encoding="utf-8").encode("utf-8")
    )
    mock_urlopen.return_value = mock_response

    cache = CacheManager(cache_dir=tmp_path)
    client = GitHubAPIClient(token="dummy_token", cache_manager=cache)

    stats = client.fetch_user_stats("vaibhavsolanki1", mode="force_live")

    assert stats["username"] == "vaibhavsolanki1"
    assert mock_urlopen.called
