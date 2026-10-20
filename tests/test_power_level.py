"""
Unit tests for Power Level Assessment Generator.
"""

from pathlib import Path

from scripts.config_loader import load_config
from scripts.power_level import (
    calculate_power_stats,
    determine_rank,
    generate_power_level,
)


def test_calculate_power_stats() -> None:
    """Verify raw stats conversion to normalized percentage and bar widths."""
    raw = {
        "total_commits": 500,
        "total_prs": 40,
        "starred": 50,
        "followers": 20,
        "streak": 30,
    }
    stats = calculate_power_stats(raw)
    assert len(stats) == 5
    for item in stats:
        assert "label" in item
        assert "value" in item
        assert "percentage" in item
        assert "bar_width" in item
        assert 0 <= item["percentage"] <= 100
        assert item["bar_width"] > 0


def test_determine_rank() -> None:
    """Verify tier ranking calculation."""
    s_stats = [{"percentage": 90}, {"percentage": 85}, {"percentage": 95}]
    rank, title = determine_rank(s_stats)
    assert rank == "S"
    assert "S-TIER" in title

    low_stats = [{"percentage": 30}, {"percentage": 40}]
    rank_c, title_c = determine_rank(low_stats)
    assert rank_c == "C"

    # Test override
    rank_o, title_o = determine_rank(low_stats, override_rank="S")
    assert rank_o == "S"


def test_generate_power_level(tmp_path: Path) -> None:
    """Verify power level SVG generation and file creation."""
    config = load_config("config.yml")
    svg_output = generate_power_level(config, output_dir=tmp_path)

    assert "<svg" in svg_output
    assert "POWER LEVEL ASSESSMENT" in svg_output
    assert "</svg>" in svg_output
    assert (tmp_path / "power_level.svg").exists()
    assert (tmp_path / "stats.svg").exists()
