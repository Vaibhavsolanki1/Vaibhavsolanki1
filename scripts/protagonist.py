"""
GitHub Profile 2.0 - Manga Protagonist Vector Art Generator

Loads and positions protagonist character vector art (assets/data/protagonist.svg)
with dynamic SMIL entrance animations, energy auras, and manga action effects.
"""

from pathlib import Path

from scripts.animation import create_energy_glow_animation, create_manga_entrance
from scripts.logger import get_logger

logger = get_logger("ProtagonistGenerator")

DEFAULT_PROTAGONIST_PATH = Path("assets/data/protagonist.svg")
DEFAULT_SPEED_LINES_PATH = Path("assets/data/speed_lines.svg")


def load_vector_asset(file_path: Path | str) -> str:
    """Read an SVG asset file and return its inner contents."""
    path = Path(file_path)
    if not path.exists():
        logger.warning(f"Vector asset not found: {path}")
        return ""
    content = path.read_text(encoding="utf-8")
    return content


def render_protagonist_banner(
    protagonist_path: Path | str = DEFAULT_PROTAGONIST_PATH,
    x: float = 20.0,
    y: float = 20.0,
    scale: float = 1.0,
    with_entrance: bool = True,
) -> str:
    """
    Renders the manga protagonist character inside an SVG group with aura and entrance animation.
    """
    path = Path(protagonist_path)
    if not path.exists():
        logger.warning(f"Protagonist art not found at {path}. Rendering fallback.")
        return f'<text x="{x}" y="{y + 60}" fill="var(--accent-primary)" font-size="24">⚔️ VAIBHAV</text>'

    content = path.read_text(encoding="utf-8")

    # Extract inner content between <svg> tags
    start = content.find(">")
    end = content.rfind("</svg>")
    inner_svg = content[start + 1 : end].strip() if start != -1 and end != -1 else content

    aura_anim = create_energy_glow_animation(dur="3s")
    entrance_anim = create_manga_entrance(from_x=-30, to_x=0, dur="0.8s") if with_entrance else ""

    return (
        f'<g class="manga-protagonist-container" transform="translate({x}, {y}) scale({scale})">\n'
        f"  {entrance_anim}\n"
        f'  <g class="manga-protagonist-body">\n'
        f"    {aura_anim}\n"
        f"    {inner_svg}\n"
        f"  </g>\n"
        f"</g>"
    )


def render_speed_lines(speed_lines_path: Path | str = DEFAULT_SPEED_LINES_PATH) -> str:
    """Load and render background speed line vectors."""
    path = Path(speed_lines_path)
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    start = content.find(">")
    end = content.rfind("</svg>")
    return content[start + 1 : end].strip() if start != -1 and end != -1 else content
