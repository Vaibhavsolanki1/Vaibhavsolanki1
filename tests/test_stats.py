"""
Unit tests for Legacy Analytics SVG Generator (Phase 6 / Deprecated)
"""

from pathlib import Path

from deprecated.stats import generate_analytics as legacy_generate_analytics
from scripts.config_loader import load_config
from scripts.github_api import GitHubAPIClient


def test_deprecated_analytics_generator(tmp_path: Path) -> None:
    """Verify legacy analytics generator in deprecated module."""
    config = load_config("config.yml")
    client = GitHubAPIClient(token=None)

    assets = legacy_generate_analytics(config, github_client=client, output_dir=tmp_path)
    assert isinstance(assets, dict)
