from pathlib import Path

import pytest

from scripts.svg_engine import SVGEngine


def test_svg_engine_render_base_component() -> None:
    """Verify rendering base SVG component template produces valid XML."""
    engine = SVGEngine(templates_dir="templates/svg")
    context = {
        "width": 800,
        "height": 200,
        "title": "Unit Test Title",
        "content": "Rendered content test.",
    }

    rendered_svg = engine.render("base_component.svg.j2", context)

    assert "<svg" in rendered_svg
    assert "</svg>" in rendered_svg
    assert "Unit Test Title" in rendered_svg
    assert "--bg-surface:" in rendered_svg


def test_svg_engine_malformed_xml(tmp_path: Path) -> None:
    """Verify malformed template raises ValueError during XML validation."""
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    broken_template = template_dir / "broken.svg.j2"
    broken_template.write_text("<svg><rect></svg>", encoding="utf-8")  # Unclosed rect tag

    engine = SVGEngine(templates_dir=template_dir)
    with pytest.raises(ValueError):
        engine.render("broken.svg.j2", {})
