"""
GitHub Profile 2.0 - Project Showcase Generator

Generates project cards section SVG (generated/projects.svg) from config.yml project items.
"""

from pathlib import Path

from scripts.config_loader import ProfileConfig
from scripts.logger import get_logger
from scripts.svg_engine import SVGEngine

logger = get_logger("ProjectsGenerator")


def generate_projects(
    config: ProfileConfig,
    output_dir: Path | str = "generated",
) -> str:
    """Generate Projects section SVG string and write asset file to disk."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = SVGEngine(templates_dir="templates/svg")

    projects_list = [p.model_dump() for p in config.projects]
    count = len(projects_list) or 1
    calculated_height = 80 + (count * 100)

    context = {
        "width": 800,
        "height": calculated_height,
        "projects": projects_list,
    }

    rendered_projects_svg = engine.render("project_card.svg.j2", context)

    projects_file = out_dir / "projects.svg"
    projects_file.write_text(rendered_projects_svg, encoding="utf-8")
    logger.info(f"Projects section SVG successfully rendered and saved to {projects_file}")

    return rendered_projects_svg
