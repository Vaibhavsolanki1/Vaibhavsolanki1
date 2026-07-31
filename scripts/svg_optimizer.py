"""
GitHub Profile 2.0 - SVG Minification & Optimization Engine

Strips unnecessary XML whitespace, comments, and truncates floating-point numbers in path data.
"""

import re
import xml.etree.ElementTree as ET

from scripts.logger import get_logger

logger = get_logger("SVGOptimizer")


def optimize_svg(raw_svg: str) -> str:
    """Minify SVG string content while maintaining valid XML syntax."""
    if not raw_svg:
        return ""

    # Verify input XML validity
    try:
        ET.fromstring(raw_svg)
    except ET.ParseError as e:
        logger.warning(f"SVG optimizer received malformed XML: {e}")
        return raw_svg

    # 1. Strip XML comments
    cleaned = re.sub(r"<!--.*?-->", "", raw_svg, flags=re.DOTALL)

    # 2. Collapse multi-line whitespace and line breaks
    cleaned = re.sub(r">\s+<", "><", cleaned)
    cleaned = cleaned.strip()

    # 3. Truncate long float coordinates (e.g. 12.345678 -> 12.35)
    def truncate_float(match: re.Match[str]) -> str:
        val = float(match.group(0))
        return f"{val:.2f}".rstrip("0").rstrip(".")

    cleaned = re.sub(r"\b\d+\.\d{3,}\b", truncate_float, cleaned)

    return cleaned
