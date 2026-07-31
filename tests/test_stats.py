"""
Unit tests for Analytics SVG Generator (Phase 6)
"""

from pathlib import Path

from scripts.config_loader import load_config
from scripts.github_api import GitHubAPIClient
from scripts.stats import generate_analytics


def test_generate_analytics(tmp_path: Path) -> None:
    """Verify analytics SVG assets generation."""
    config = load_config("config.yml")
    client = GitHubAPIClient(token=None, mock_fixture_path="tests/mock_github_data.json")

    assets = generate_analytics(config, github_client=client, output_dir=tmp_path)

    assert "stats" in assets
    assert "heatmap" in assets
    assert "languages" in assets

    assert (tmp_path / "stats.svg").exists()
    assert (tmp_path / "heatmap.svg").exists()
    assert (tmp_path / "languages.svg").exists()
