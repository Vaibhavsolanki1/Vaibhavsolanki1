"""
GitHub Profile 2.0 - Hero Generator

Generates animated manga hero section SVG (generated/hero.svg) or classic terminal banner.
"""

from pathlib import Path

from scripts.animation import create_pulse_animation
from scripts.config_loader import ProfileConfig
from scripts.logger import get_logger
from scripts.portrait import render_ascii_portrait, render_vector_name
from scripts.protagonist import render_protagonist_banner, render_speed_lines
from scripts.svg_engine import SVGEngine

logger = get_logger("HeroGenerator")


def generate_hero(
    config: ProfileConfig,
    portrait_path: Path | str = "assets/data/portrait.txt",
    name_svg_path: Path | str = "assets/data/name.svg",
    protagonist_path: Path | str = "assets/data/protagonist.svg",
    output_dir: Path | str = "generated",
) -> str:
    """Generate animated Hero section SVG string and write asset file to disk."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = SVGEngine(templates_dir="templates/svg")
    pulse_anim = create_pulse_animation(dur="2s")

    is_manga = getattr(config, "manga", None) and config.manga.enabled

    if is_manga:
        canvas_width = 800
        canvas_height = 340
        protagonist_art = render_protagonist_banner(
            protagonist_path=protagonist_path, x=20.0, y=10.0, scale=0.88
        )
        speed_lines_art = render_speed_lines()

        context = {
            "width": canvas_width,
            "height": canvas_height,
            "is_manga": True,
            "theme": "manga",
            "name": config.profile.name,
            "title": config.profile.title,
            "status": config.profile.status,
            "location": config.profile.location,
            "focus": config.profile.focus,
            "availability": config.profile.availability,
            "protagonist_art": protagonist_art,
            "speed_lines": speed_lines_art,
            "chapter_title": config.manga.chapter_title,
            "protagonist_name": config.manga.protagonist_name,
            "pulse_anim": pulse_anim,
        }
    else:
        canvas_width = 800
        canvas_height = 280
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
        context = {
            "width": canvas_width,
            "height": canvas_height,
            "is_manga": False,
            "theme": "dark",
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

    rendered_hero_svg = engine.render("hero.svg.j2", context, theme="manga" if is_manga else "dark")

    hero_file = out_dir / "hero.svg"
    hero_file.write_text(rendered_hero_svg, encoding="utf-8")
    logger.info(f"Hero section SVG successfully rendered and saved to {hero_file}")

    return rendered_hero_svg
