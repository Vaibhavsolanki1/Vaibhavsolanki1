"""
GitHub Profile 2.0 - SMIL SVG Animation Utilities

Generates native SVG SMIL animation nodes (<animate>, <animateTransform>)
for typewriter effects, pulse indicators, and fade-in transitions.
"""


def create_typewriter_animation(
    text_phrases: list[str],
    dur: str = "12s",
    repeat_count: str = "indefinite",
) -> str:
    """
    Generate SMIL <animate> node that cycles through text phrases discrete values
    to simulate a typewriter effect.
    """
    if not text_phrases:
        return ""

    values_str = ";".join(text_phrases)
    return (
        f'<animate attributeName="d" dur="{dur}" repeatCount="{repeat_count}" '
        f'values="{values_str}"/>'
    )


def create_pulse_animation(
    dur: str = "2s",
    min_opacity: float = 0.3,
    max_opacity: float = 1.0,
) -> str:
    """Generate SMIL <animate> node for pulsing status indicator opacity."""
    return (
        f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" '
        f'values="{min_opacity};{max_opacity};{min_opacity}" keyTimes="0;0.5;1"/>'
    )


def create_fade_in_animation(
    dur: str = "0.8s",
    delay: str = "0s",
) -> str:
    """Generate SMIL <animate> node for smooth component entry fade-in."""
    return (
        f'<animate attributeName="opacity" from="0" to="1" dur="{dur}" begin="{delay}" '
        f'fill="freeze"/>'
    )
