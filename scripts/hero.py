"""
GitHub Profile 2.0 - Hero Generator

Generates animated terminal hero section SVG (generated/hero.svg).
"""

from pathlib import Path

from scripts.animation import create_pulse_animation
from scripts.config_loader import ProfileConfig
from scripts.logger import get_logger
from scripts.portrait import render_ascii_portrait, render_vector_name
from scripts.svg_engine import SVGEngine

logger = get_logger("HeroGenerator")


def generate_hero(
    config: ProfileConfig,
    portrait_path: Path | str = "assets/data/portrait.txt",
    name_svg_path: Path | str = "assets/data/name.svg",
    output_dir: Path | str = "generated",
) -> str:
    """Generate animated Hero section SVG string using assets/data/name.svg and write asset file to disk."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = SVGEngine(templates_dir="templates/svg")

    vector_name = render_vector_name(
        name_svg_path=name_svg_path, x=24.0, y=56.0, scale=1.15
    )
    ascii_art = render_ascii_portrait(
        portrait_path=portrait_path,
        x=24.0,
        y=54.0,
        font_size=11.0,
        line_height=14.0,
    )
    pulse_anim = create_pulse_animation(dur="2s")

    context = {
        "width": 800,
        "height": 280,
        "name": config.profile.name,
        "title": config.profile.title,
        "status": config.profile.status,
        "location": config.profile.location,
        "focus": config.profile.focus,
        "availability": config.profile.availability,
        "vector_name": vector_name,
        "ascii_portrait": ascii_art,
        "pulse_anim": pulse_anim,
    }

    rendered_hero_svg = engine.render("hero.svg.j2", context)

    hero_file = out_dir / "hero.svg"
    hero_file.write_text(rendered_hero_svg, encoding="utf-8")
    logger.info(f"Hero section SVG successfully rendered and saved to {hero_file}")

    return rendered_hero_svg
