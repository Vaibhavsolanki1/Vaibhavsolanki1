"""
GitHub Profile 2.0 - DEPRECATED / LEGACY MODULE

[DEPRECATED in v1.1.0]
This module has been deprecated as part of the transition to the Hybrid Architecture.
Live GitHub Statistics, Streak, and Top Languages are now rendered dynamically using
trusted live widgets in README.md to ensure real-time accuracy and zero build overhead.
"""

from pathlib import Path

from scripts.config_loader import ProfileConfig
from scripts.github_api import GitHubAPIClient
from scripts.logger import get_logger

logger = get_logger("LegacyStatsGenerator")


def generate_analytics(
    config: ProfileConfig,
    github_client: GitHubAPIClient | None = None,
    output_dir: Path | str = "generated",
) -> dict[str, str]:
    """[LEGACY] Deprecated stats generator function."""
    logger.warning(
        "generate_analytics() is deprecated. Live widgets in README.md are used in Hybrid Architecture."
    )
    return {}
