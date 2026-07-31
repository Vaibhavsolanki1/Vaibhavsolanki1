"""
Unit tests for SVG Math & Chart Primitives Engine (Phase 6)
"""

from scripts.charts import (
    calculate_contribution_color,
    render_donut_chart_paths,
    render_heatmap_grid,
)


def test_calculate_contribution_color() -> None:
    """Verify color token mapping for contribution counts."""
    assert calculate_contribution_color(0) == "var(--contribution-0)"
    assert calculate_contribution_color(2) == "var(--contribution-1)"
    assert calculate_contribution_color(5) == "var(--contribution-2)"
    assert calculate_contribution_color(10) == "var(--contribution-3)"
    assert calculate_contribution_color(15) == "var(--contribution-4)"


def test_render_heatmap_grid() -> None:
    """Verify heatmap grid rect rendering."""
    weeks = [
        {
            "contributionDays": [
                {"contributionCount": 3, "date": "2026-07-30", "weekday": 0},
                {"contributionCount": 8, "date": "2026-07-31", "weekday": 1},
            ]
        }
    ]

    rects_svg = render_heatmap_grid(weeks)
    assert "<rect" in rects_svg
    assert "2026-07-30" in rects_svg
    assert "2026-07-31" in rects_svg


def test_render_donut_chart_paths() -> None:
    """Verify donut chart arc rendering."""
    languages = [
        {"name": "Python", "percentage": 60.0, "color": "#3572A5"},
        {"name": "TypeScript", "percentage": 40.0, "color": "#3178C6"},
    ]

    paths_svg = render_donut_chart_paths(languages)
    assert "<path" in paths_svg
    assert "Python: 60.0%" in paths_svg
    assert "TypeScript: 40.0%" in paths_svg
