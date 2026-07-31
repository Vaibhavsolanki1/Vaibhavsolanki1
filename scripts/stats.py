"""
GitHub Profile 2.0 - Analytics SVG Generator

Consumes normalized GitHub data dictionary and generates stats.svg, heatmap.svg, and languages.svg.
"""

from pathlib import Path
from typing import Any

from scripts.charts import render_donut_chart_paths, render_heatmap_grid
from scripts.config_loader import ProfileConfig
from scripts.github_api import GitHubAPIClient
from scripts.logger import get_logger
from scripts.svg_engine import SVGEngine

logger = get_logger("StatsGenerator")


def generate_analytics(
    config: ProfileConfig,
    github_client: GitHubAPIClient | None = None,
    output_dir: Path | str = "generated",
) -> dict[str, str]:
    """Generate all analytics SVGs and return dict of asset paths."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    client = github_client or GitHubAPIClient()
    stats_data: dict[str, Any] = client.fetch_user_stats(
        username=config.github.username, mode=config.github.data_mode
    )

    engine = SVGEngine(templates_dir="templates/svg")
    generated_assets: dict[str, str] = {}

    # 1. Render Stats Card (stats.svg)
    stats_svg = engine.render("stats_card.svg.j2", {"stats": stats_data})
    stats_file = out_dir / "stats.svg"
    stats_file.write_text(stats_svg, encoding="utf-8")
    generated_assets["stats"] = f"{config.system.output_dir}/stats.svg"

    # 2. Render Contribution Heatmap (heatmap.svg)
    weeks = stats_data.get("contribution_weeks", [])
    heatmap_rects = render_heatmap_grid(
        weeks, start_x=24.0, start_y=40.0, cell_size=10.0, cell_gap=3.0
    )
    heatmap_svg = engine.render(
        "heatmap.svg.j2", {"stats": stats_data, "heatmap_rects": heatmap_rects}
    )
    heatmap_file = out_dir / "heatmap.svg"
    heatmap_file.write_text(heatmap_svg, encoding="utf-8")
    generated_assets["heatmap"] = f"{config.system.output_dir}/heatmap.svg"

    # 3. Render Languages Chart (languages.svg)
    languages = stats_data.get("languages", [])
    donut_paths = render_donut_chart_paths(
        languages, cx=150.0, cy=115.0, radius=65.0, inner_radius=42.0
    )
    languages_svg = engine.render(
        "language_chart.svg.j2", {"stats": stats_data, "donut_paths": donut_paths}
    )
    languages_file = out_dir / "languages.svg"
    languages_file.write_text(languages_svg, encoding="utf-8")
    generated_assets["languages"] = f"{config.system.output_dir}/languages.svg"

    logger.info("Successfully generated all analytics SVG assets.")
    return generated_assets
