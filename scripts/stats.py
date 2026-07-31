"""
GitHub Profile 2.0 - DEPRECATED / LEGACY STUB

[DEPRECATED in v1.1.0]
Replaced by live GitHub widgets in templates/readme.md.j2 under Hybrid Architecture.
See deprecated/stats.py for original code.
"""

from pathlib import Path

from scripts.config_loader import ProfileConfig
from scripts.github_api import GitHubAPIClient


def generate_analytics(
    config: ProfileConfig,
    github_client: GitHubAPIClient | None = None,
    output_dir: Path | str = "generated",
) -> dict[str, str]:
    """Deprecated stub returning empty dict."""
    return {}
