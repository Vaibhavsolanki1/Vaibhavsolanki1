"""
GitHub Profile 2.0 - Core SVG Rendering Engine

Jinja2 template renderer for SVG components, embedding design tokens and font CSS blocks.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from scripts.design_tokens import to_css_variables
from scripts.font_subset import generate_font_face_css
from scripts.logger import get_logger

logger = get_logger("SVGEngine")


class SVGEngine:
    """Core SVG Template Rendering Engine."""

    def __init__(self, templates_dir: Path | str = "templates/svg") -> None:
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(
        self,
        template_name: str,
        context: dict[str, Any],
        palette_override: dict[str, str] | None = None,
    ) -> str:
        """Render a Jinja2 SVG template with dynamic design system variables."""
        template = self.env.get_template(template_name)

        # Build design system CSS block
        css_vars = to_css_variables(palette_override)
        font_css = generate_font_face_css()
        system_styles = f"<style>\n{font_css}\n{css_vars}\n</style>"

        # Inject styles into context
        merged_context = {
            **context,
            "system_styles": system_styles,
        }

        rendered_xml = template.render(merged_context)

        # XML Conformance Check
        self.validate_xml(rendered_xml, template_name)

        return rendered_xml

    def validate_xml(self, xml_string: str, source_name: str) -> None:
        """Validate rendered XML string format."""
        try:
            ET.fromstring(xml_string)
        except ET.ParseError as e:
            logger.error(f"XML parse error in rendered SVG ({source_name}): {e}")
            raise ValueError(
                f"Rendered SVG ({source_name}) contains malformed XML syntax: {e}"
            ) from e
