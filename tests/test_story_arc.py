"""
Unit tests for Story Arc Timeline Generator.
"""

from pathlib import Path

from scripts.config_loader import load_config
from scripts.story_arc import generate_story_arc


def test_generate_story_arc(tmp_path: Path) -> None:
    """Verify story arc SVG timeline rendering and asset writing."""
    config = load_config("config.yml")
    svg_output = generate_story_arc(config, output_dir=tmp_path)

    assert "<svg" in svg_output
    assert "THE STORY SO FAR" in svg_output
    assert "ARC #01" in svg_output
    assert "TO BE CONTINUED" in svg_output
    assert "</svg>" in svg_output
    assert (tmp_path / "story_arc.svg").exists()
