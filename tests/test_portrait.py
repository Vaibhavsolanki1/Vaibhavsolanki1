"""
Unit tests for ASCII Portrait Parser (Phase 5)
"""

from pathlib import Path

from scripts.portrait import render_ascii_portrait


def test_render_ascii_portrait_file_exists(tmp_path: Path) -> None:
    """Verify rendering ASCII text lines into SVG text elements."""
    portrait_file = tmp_path / "portrait.txt"
    portrait_file.write_text("LINE 1\nLINE 2", encoding="utf-8")

    svg_group = render_ascii_portrait(portrait_path=portrait_file)

    assert '<g class="ascii-portrait"' in svg_group
    assert "LINE 1" in svg_group
    assert "LINE 2" in svg_group
    assert "</g>" in svg_group


def test_render_ascii_portrait_missing_file(tmp_path: Path) -> None:
    """Verify fallback text rendering when file is missing."""
    missing = tmp_path / "missing.txt"
    svg_output = render_ascii_portrait(portrait_path=missing)

    assert "<text" in svg_output
    assert "VAIBHAV SOLANKI" in svg_output
