"""
GitHub Profile 2.0 - Manga Power Level Assessment Generator

Transforms GitHub development activity metrics into an anime-inspired
power level gauge with rank tiers (S/A/B/C) and animated progress bars.
"""

from pathlib import Path
from typing import Any

from scripts.config_loader import ProfileConfig
from scripts.logger import get_logger
from scripts.svg_engine import SVGEngine

logger = get_logger("PowerLevelGenerator")


def calculate_power_stats(raw_stats: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Convert raw GitHub statistics into manga power level bars."""
    stats = raw_stats or {}

    total_commits = int(stats.get("total_commits", 450) if isinstance(stats.get("total_commits"), int | float) else 450)
    total_prs = int(stats.get("total_prs", 35) if isinstance(stats.get("total_prs"), int | float) else 35)
    total_stars = int(stats.get("starred", 48) if isinstance(stats.get("starred"), int | float) else 48)
    followers = int(stats.get("followers", 18) if isinstance(stats.get("followers"), int | float) else 18)
    streak = int(stats.get("streak", 28) if isinstance(stats.get("streak"), int | float) else 28)

    # Normalized scale definitions
    max_track_width = 336.0

    items: list[dict[str, Any]] = [
        {
            "label": "CODING POWER // コーディング力",
            "value": f"{total_commits:,} COMMITS",
            "percentage": min(98, max(50, int((total_commits / 500) * 100))),
        },
        {
            "label": "COLLABORATION JUTSU // 協力の術",
            "value": f"{total_prs:,} PRs",
            "percentage": min(95, max(40, int((total_prs / 40) * 100))),
        },
        {
            "label": "STAR ENERGY // 星のオーラ",
            "value": f"{total_stars:,} STARS",
            "percentage": min(92, max(35, int((total_stars / 50) * 100))),
        },
        {
            "label": "ALLY COUNT // 仲間の数",
            "value": f"{followers:,} ALLIES",
            "percentage": min(90, max(30, int((followers / 20) * 100))),
        },
        {
            "label": "QUEST STREAK // 連勝記録",
            "value": f"{streak} DAYS",
            "percentage": min(96, max(45, int((streak / 30) * 100))),
        },
    ]

    for item in items:
        pct = float(item["percentage"])
        item["bar_width"] = round((pct / 100.0) * max_track_width, 1)

    return items


def determine_rank(power_stats: list[dict[str, Any]], override_rank: str | None = None) -> tuple[str, str]:
    """Calculate protagonist rank from power percentages."""
    if override_rank:
        rank_titles = {
            "S": "SPECIAL S-TIER",
            "A": "VETERAN A-TIER",
            "B": "RISING B-TIER",
            "C": "NOVICE C-TIER",
        }
        return override_rank.upper(), rank_titles.get(override_rank.upper(), "PROTAGONIST")

    avg_pct = sum(float(item["percentage"]) for item in power_stats) / max(len(power_stats), 1)
    if avg_pct >= 75:
        return "S", "SPECIAL S-TIER"
    elif avg_pct >= 60:
        return "A", "VETERAN A-TIER"
    elif avg_pct >= 45:
        return "B", "RISING B-TIER"
    return "C", "NOVICE C-TIER"


def generate_power_level(
    config: ProfileConfig,
    raw_stats: dict[str, Any] | None = None,
    output_dir: Path | str = "generated",
) -> str:
    """Render manga power level SVG and write to disk."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = SVGEngine(templates_dir="templates/svg")
    power_stats = calculate_power_stats(raw_stats)

    configured_rank = getattr(config.manga, "power_rank", None) if getattr(config, "manga", None) else None
    rank, rank_title = determine_rank(power_stats, override_rank=configured_rank)

    context = {
        "width": 800,
        "height": 240,
        "theme": "manga",
        "power_stats": power_stats,
        "rank": rank,
        "rank_title": rank_title,
    }

    rendered_svg = engine.render("power_level.svg.j2", context, theme="manga")

    output_file = out_dir / "power_level.svg"
    output_file.write_text(rendered_svg, encoding="utf-8")

    # Also write to stats.svg for backward asset reference compatibility
    stats_file = out_dir / "stats.svg"
    stats_file.write_text(rendered_svg, encoding="utf-8")

    logger.info(f"Power level SVG successfully rendered and saved to {output_file}")
    return rendered_svg
