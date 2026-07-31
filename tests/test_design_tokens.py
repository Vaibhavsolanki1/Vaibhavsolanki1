from dataclasses import FrozenInstanceError

import pytest

from scripts.design_tokens import (
    COLORS,
    get_color,
    get_spacing,
    to_css_variables,
)


def test_color_palette_immutability() -> None:
    """Verify ColorPalette tokens are frozen and immutable."""
    with pytest.raises(FrozenInstanceError):
        COLORS.accent_primary = "#000000"  # type: ignore[misc]


def test_get_color_valid() -> None:
    """Verify get_color retrieves valid hex tokens."""
    assert get_color("accent_primary") == "#58A6FF"
    assert get_color("bg_canvas") == "#0D1117"


def test_get_color_invalid() -> None:
    """Verify get_color raises AttributeError for non-existent tokens."""
    with pytest.raises(AttributeError):
        get_color("non_existent_color")


def test_spacing_scale() -> None:
    """Verify get_spacing returns accurate pixel values."""
    assert get_spacing(1) == 4
    assert get_spacing(4) == 16
    assert get_spacing(8) == 32
    assert get_spacing(24) == 96


def test_spacing_scale_invalid() -> None:
    """Verify invalid spacing scale raises ValueError."""
    with pytest.raises(ValueError):
        get_spacing(5)


def test_to_css_variables_generation() -> None:
    """Verify to_css_variables compiles valid CSS block containing expected tokens."""
    css = to_css_variables()
    assert ":root {" in css
    assert "--bg-canvas: #0D1117;" in css
    assert "--accent-primary: #58A6FF;" in css
    assert "}" in css


def test_to_css_variables_override() -> None:
    """Verify custom palette override modifies compiled CSS block."""
    override = {"accent_primary": "#7C3AED"}
    css = to_css_variables(override)
    assert "--accent-primary: #7C3AED;" in css
