"""
Unit tests for SMIL SVG Animation Utilities (Phase 5)
"""

from scripts.animation import (
    create_fade_in_animation,
    create_pulse_animation,
    create_typewriter_animation,
)


def test_create_typewriter_animation() -> None:
    """Verify typewriter SMIL animation string generation."""
    phrases = ["AI Engineer", "Full Stack Developer"]
    anim = create_typewriter_animation(phrases, dur="10s")

    assert '<animate attributeName="d"' in anim
    assert 'dur="10s"' in anim
    assert 'values="AI Engineer;Full Stack Developer"' in anim


def test_create_pulse_animation() -> None:
    """Verify pulsing opacity animation tag."""
    anim = create_pulse_animation(dur="2s", min_opacity=0.2, max_opacity=0.8)

    assert '<animate attributeName="opacity"' in anim
    assert 'values="0.2;0.8;0.2"' in anim


def test_create_fade_in_animation() -> None:
    """Verify fade in opacity animation tag."""
    anim = create_fade_in_animation(dur="0.5s", delay="0.2s")

    assert '<animate attributeName="opacity"' in anim
    assert 'from="0"' in anim
    assert 'to="1"' in anim
    assert 'begin="0.2s"' in anim
