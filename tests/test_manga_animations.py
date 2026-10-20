"""
Unit tests for Manga SMIL Animation Utilities.
"""

from scripts.animation import (
    create_energy_glow_animation,
    create_manga_entrance,
    create_power_bar_fill,
    create_sparkle_animation,
    create_speed_line_animation,
)


def test_manga_animations_syntax() -> None:
    """Verify all manga SMIL animations produce valid SVG animation nodes."""
    anim_speed = create_speed_line_animation()
    assert "<animateTransform" in anim_speed
    assert 'attributeName="transform"' in anim_speed
    assert 'type="rotate"' in anim_speed

    anim_glow = create_energy_glow_animation()
    assert "<animate" in anim_glow
    assert 'attributeName="opacity"' in anim_glow

    anim_bar = create_power_bar_fill(250.0)
    assert "<animate" in anim_bar
    assert 'attributeName="width"' in anim_bar
    assert 'to="250.0"' in anim_bar

    anim_entrance = create_manga_entrance()
    assert "<animateTransform" in anim_entrance
    assert 'type="translate"' in anim_entrance

    anim_sparkle = create_sparkle_animation()
    assert "<animate" in anim_sparkle
    assert 'attributeName="opacity"' in anim_sparkle
