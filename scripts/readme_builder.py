"""
GitHub Profile 2.0 - README Assembler

Assembles final README.md file from templates/readme.md.j2 using generated asset references.
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from scripts.logger import get_logger

logger = get_logger("READMEBuilder")


class READMEBuilder:
    """Markdown Profile Builder."""

    def __init__(self, templates_dir: Path | str = "templates") -> None:
        self.templates_dir = Path(templates_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def build(self, context: dict[str, Any], template_name: str = "readme.md.j2") -> str:
        """Render README Markdown string from Jinja template and context dict."""
        template = self.env.get_template(template_name)
        rendered_md = template.render(context)
        return rendered_md

    def save(self, markdown_content: str, output_path: Path | str = "README.md") -> Path:
        """Save rendered markdown content to target output file path."""
        target = Path(output_path)
        target.write_text(markdown_content, encoding="utf-8")
        logger.info(f"Successfully assembled and saved {target}")
        return target
