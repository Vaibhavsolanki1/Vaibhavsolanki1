"""
GitHub Profile 2.0 - Vector Name & ASCII Portrait Renderer

Loads vector name SVG (assets/data/name.svg) or ASCII art text files
and formats them into SVG element groups for hero section rendering.
"""

import re
from pathlib import Path

from scripts.utils import escape_xml

DEFAULT_PORTRAIT_PATH = Path("assets/data/portrait.txt")
DEFAULT_NAME_SVG_PATH = Path("assets/data/name.svg")


def render_vector_name(
    name_svg_path: Path | str = DEFAULT_NAME_SVG_PATH,
    x: float = 24.0,
    y: float = 52.0,
    scale: float = 1.1,
    fill_color: str = "var(--accent-primary)",
) -> str:
    """Read assets/data/name.svg vector file and return SVG <g> group for VAIBHAV."""
    path = Path(name_svg_path)
    if not path.exists():
        return (
            f'<text x="{x}" y="{y}" fill="{fill_color}" '
            f'font-family="var(--font-family)" font-size="24" font-weight="700">VAIBHAV</text>'
        )

    content = path.read_text(encoding="utf-8")
    match = re.search(r'd="([^"]+)"', content)
    if not match:
        return f'<text x="{x}" y="{y}" fill="{fill_color}">VAIBHAV</text>'

    path_d = match.group(1)

    return (
        f'<g class="vector-name" transform="translate({x}, {y}) scale({scale})" fill="{fill_color}">\n'
        f'  <g transform="translate(0, -9.47)">\n'
        f'    <path d="{path_d}"/>\n'
        f'  </g>\n'
        f'</g>'
    )


def render_ascii_portrait(
    portrait_path: Path | str = DEFAULT_PORTRAIT_PATH,
    x: float = 24.0,
    y: float = 40.0,
    font_size: float = 12.0,
    line_height: float = 14.0,
    fill_color: str = "var(--accent-primary)",
) -> str:
    """Read ASCII art text and format as group of SVG <text> elements."""
    path = Path(portrait_path)

    if not path.exists():
        return (
            f'<text x="{x}" y="{y}" fill="{fill_color}" '
            f'font-family="var(--font-family)" font-size="{font_size}">VAIBHAV SOLANKI</text>'
        )

    lines = path.read_text(encoding="utf-8").splitlines()
    svg_lines: list[str] = [
        f'<g class="ascii-portrait" font-family="\'JetBrains Mono\', \'Fira Code\', \'Consolas\', \'Courier New\', monospace" font-size="{font_size}" font-weight="700" letter-spacing="0.5px">'
    ]

    current_y = y
    for line in lines:
        escaped_line = escape_xml(line)
        svg_lines.append(
            f'  <text x="{x}" y="{current_y:.1f}" fill="{fill_color}" xml:space="preserve">{escaped_line}</text>'
        )
        current_y += line_height

    svg_lines.append("</g>")
    return "\n".join(svg_lines)
