"""
Unit tests for SVG Minification & Optimization Engine (Phase 9)
"""

from scripts.svg_optimizer import optimize_svg


def test_optimize_svg_strips_comments_and_whitespace() -> None:
    """Verify stripping XML comments and collapsing whitespace."""
    raw = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <!-- Comment to strip -->
        <rect width="10" height="10"/>
    </svg>
    """
    optimized = optimize_svg(raw)

    assert "<!--" not in optimized
    assert "><" in optimized
    assert "<rect" in optimized


def test_optimize_svg_truncates_floats() -> None:
    """Verify float coordinate truncation to 2 decimal places."""
    raw = '<svg><path d="M 12.345678 98.765432 L 10.000 20.123"/></svg>'
    optimized = optimize_svg(raw)

    assert "12.35" in optimized
    assert "98.77" in optimized
