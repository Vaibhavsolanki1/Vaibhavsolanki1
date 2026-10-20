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


def create_speed_line_animation(dur: str = "4s") -> str:
    """Generate SMIL <animateTransform> for rotating background speed lines."""
    return (
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="0 400 200" to="360 400 200" dur="{dur}" repeatCount="indefinite"/>'
    )


def create_energy_glow_animation(dur: str = "2.5s") -> str:
    """Generate SMIL <animate> node for pulsating protagonist energy aura."""
    return (
        f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" '
        f'values="0.5;0.95;0.5" keyTimes="0;0.5;1"/>'
    )


def create_power_bar_fill(
    target_width: float,
    dur: str = "1.2s",
    delay: str = "0.2s",
) -> str:
    """Generate SMIL <animate> node that animates power level bar width from 0 to target_width."""
    return (
        f'<animate attributeName="width" from="0" to="{target_width}" dur="{dur}" '
        f'begin="{delay}" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>'
    )


def create_manga_entrance(
    from_x: float = -40.0,
    to_x: float = 0.0,
    dur: str = "0.6s",
    delay: str = "0s",
) -> str:
    """Generate SMIL <animateTransform> node for dramatic character slide-in entrance."""
    return (
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="{from_x} 0" to="{to_x} 0" dur="{dur}" begin="{delay}" '
        f'fill="freeze" calcMode="spline" keySplines="0.1 0.9 0.2 1"/>'
    )


def create_sparkle_animation(dur: str = "1.5s", delay: str = "0s") -> str:
    """Generate SMIL <animate> node for glittering rank sparkle."""
    return (
        f'<animate attributeName="opacity" dur="{dur}" begin="{delay}" repeatCount="indefinite" '
        f'values="0.2;1;0.2" keyTimes="0;0.5;1"/>'
    )
