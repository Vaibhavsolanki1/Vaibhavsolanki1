"""
Unit tests for Hero Generator (Phase 5)
"""

from pathlib import Path

from scripts.config_loader import load_config
from scripts.hero import generate_hero


def test_generate_hero(tmp_path: Path) -> None:
    """Verify hero SVG generation and file writing."""
    config = load_config("config.yml")
    hero_svg = generate_hero(config, portrait_path="assets/data/portrait.txt", output_dir=tmp_path)

    assert "<svg" in hero_svg
    assert "</svg>" in hero_svg
    assert config.profile.name in hero_svg
    assert (tmp_path / "hero.svg").exists()
