"""
GitHub Profile 2.0 - Shared SVG & Geometry Utilities

Text width estimation, XML escaping, SVG element builders, and numeric helpers.
"""

import html


def escape_xml(text: str) -> str:
    """Safely escape text for XML / SVG nodes."""
    return html.escape(text, quote=True)


def calculate_text_width(
    text: str, font_size: float = 14.0, font_family: str = "monospace"
) -> float:
    """
    Estimate rendered text width in pixels for monospaced typography.
    Standard monospaced advance is ~0.60 * font_size per character.
    """
    if "monospace" in font_family.lower() or "jetbrains mono" in font_family.lower():
        char_advance = font_size * 0.60
    else:
        char_advance = font_size * 0.55

    return round(len(text) * char_advance, 2)


def truncate_text(text: str, max_length: int = 40) -> str:
    """Truncate long text string with ellipsis if exceeding max_length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
