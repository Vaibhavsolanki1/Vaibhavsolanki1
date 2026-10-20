"""
GitHub Profile 2.0 - Story Arc Timeline Generator

Generates a manga narrative timeline (generated/story_arc.svg) showcasing
the protagonist's journey across connected story arcs.
"""

from pathlib import Path

from scripts.config_loader import ProfileConfig
from scripts.logger import get_logger
from scripts.svg_engine import SVGEngine

logger = get_logger("StoryArcGenerator")

DEFAULT_STORY_ARCS = [
    {
        "title": "Origin Arc",
        "subtitle": "The Beginning",
        "icon": "🎓",
        "description": "CS Engineering Student — Deepening expertise in Systems & AI.",
    },
    {
        "title": "Rising Power",
        "subtitle": "Building Legends",
        "icon": "🤖",
        "description": "Builder & AI Engineer — Crafting Oasis & Maitri platforms.",
    },
    {
        "title": "Creator Arc",
        "subtitle": "Platform Architect",
        "icon": "🔮",
        "description": "Autonomous Workflows & Generative AI Studio at scale.",
    },
]


def generate_story_arc(
    config: ProfileConfig,
    output_dir: Path | str = "generated",
) -> str:
    """Generate Story Arc section SVG string and write asset file to disk."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = SVGEngine(templates_dir="templates/svg")

    story_arcs = []
    if getattr(config, "manga", None) and config.manga.story_arcs:
        story_arcs = [arc.model_dump() for arc in config.manga.story_arcs]
    else:
        story_arcs = DEFAULT_STORY_ARCS

    context = {
        "width": 800,
        "height": 240,
        "theme": "manga",
        "story_arcs": story_arcs,
    }

    rendered_svg = engine.render("story_arc.svg.j2", context, theme="manga")

    output_file = out_dir / "story_arc.svg"
    output_file.write_text(rendered_svg, encoding="utf-8")
    logger.info(f"Story Arc section SVG successfully rendered and saved to {output_file}")

    return rendered_svg
