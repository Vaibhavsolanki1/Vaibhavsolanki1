"""
GitHub Profile 2.0 - ASCII Portrait Parser

Transforms ASCII art text files into formatted SVG <text> element arrays.
"""

from pathlib import Path

from scripts.utils import escape_xml

DEFAULT_PORTRAIT_PATH = Path("assets/data/portrait.txt")


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
        # Fallback text banner if file is missing
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
