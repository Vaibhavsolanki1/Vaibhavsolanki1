"""
Unit tests for Shared SVG & Geometry Utilities (Phase 2)
"""

from scripts.utils import calculate_text_width, escape_xml, truncate_text


def test_escape_xml() -> None:
    """Verify XML special character escaping."""
    raw = 'Hello <world> & "friends"'
    escaped = escape_xml(raw)
    assert "&lt;" in escaped
    assert "&gt;" in escaped
    assert "&amp;" in escaped
    assert "&quot;" in escaped


def test_calculate_text_width() -> None:
    """Verify monospaced text width calculation."""
    width = calculate_text_width("Hello", font_size=10.0, font_family="JetBrains Mono")
    assert width == 30.0  # 5 chars * (10.0 * 0.60)


def test_truncate_text() -> None:
    """Verify string truncation logic."""
    short_str = "Short"
    long_str = "This is a very long string that should be truncated"

    assert truncate_text(short_str, max_length=20) == "Short"
    truncated = truncate_text(long_str, max_length=20)
    assert len(truncated) == 20
    assert truncated.endswith("...")
