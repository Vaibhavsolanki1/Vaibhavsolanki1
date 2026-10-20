"""
Unit tests for Manga Protagonist Generator.
"""

from pathlib import Path

from scripts.portrait import render_manga_protagonist
from scripts.protagonist import render_protagonist_banner, render_speed_lines


def test_render_protagonist_banner() -> None:
    """Verify protagonist SVG banner renders with valid SVG group and styling."""
    svg_art = render_protagonist_banner(x=20, y=10, scale=1.0)
    assert '<g class="manga-protagonist-container"' in svg_art
    assert "translate(20, 10)" in svg_art
    assert "</g>" in svg_art


def test_render_protagonist_fallback(tmp_path: Path) -> None:
    """Verify fallback rendering when asset file does not exist."""
    missing_file = tmp_path / "non_existent.svg"
    svg_art = render_protagonist_banner(protagonist_path=missing_file)
    assert "VAIBHAV" in svg_art


def test_render_speed_lines() -> None:
    """Verify speed lines asset loading."""
    speed_lines = render_speed_lines()
    assert "speedLineGlow" in speed_lines or "<line" in speed_lines


def test_render_manga_protagonist_facade() -> None:
    """Verify portrait module facade function."""
    svg_art = render_manga_protagonist(x=10, y=10)
    assert "manga-protagonist-container" in svg_art
