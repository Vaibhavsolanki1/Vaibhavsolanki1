"""
Unit tests for Project Showcase Generator (Phase 7)
"""

from pathlib import Path

from scripts.config_loader import load_config
from scripts.projects import generate_projects


def test_generate_projects(tmp_path: Path) -> None:
    """Verify projects SVG generation and output file creation."""
    config = load_config("config.yml")
    projects_svg = generate_projects(config, output_dir=tmp_path)

    assert "<svg" in projects_svg
    assert "FEATURED PROJECTS" in projects_svg
    assert "Metry" in projects_svg
    assert "Kalam" in projects_svg
    assert (tmp_path / "projects.svg").exists()
