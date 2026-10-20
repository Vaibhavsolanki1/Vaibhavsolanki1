"""
GitHub Profile 2.0 - Design System Tokens

Immutable programmatic design tokens defining color hierarchy, typography scale,
spacing grid, SMIL animation parameters, and CSS custom property compilation.
"""

from dataclasses import dataclass
from enum import Enum


class ThemeMode(Enum):
    DARK = "dark"
    MANGA = "manga"


@dataclass(frozen=True)
class ColorPalette:
    # Canvas / Background
    bg_canvas: str = "#0D1117"
    bg_surface: str = "#161B22"
    bg_subtle: str = "#21262D"
    border_muted: str = "#30363D"

    # Text Hierarchy
    text_primary: str = "#E6EDF3"
    text_secondary: str = "#8B949E"
    text_muted: str = "#484F58"

    # Brand Accent System
    accent_primary: str = "#58A6FF"
    accent_hover: str = "#79C0FF"
    accent_active: str = "#1F6FEB"
    accent_subtle: str = "#388BFD26"

    # Heatmap Contribution Intensity
    contribution_0: str = "#161B22"
    contribution_1: str = "#0E4429"
    contribution_2: str = "#006D32"
    contribution_3: str = "#26A641"
    contribution_4: str = "#39D353"

    # Semantic Status
    success: str = "#3FB950"
    warning: str = "#D29922"
    error: str = "#F85149"
    info: str = "#58A6FF"

    # Manga Specific Tokens
    manga_speed_line: str = "#E94560"
    manga_panel_border: str = "#2A2A3E"
    manga_glow: str = "#FFD700"
    manga_shadow: str = "#0D0D1A"
    manga_energy: str = "#00D4FF"


MANGA_COLORS = ColorPalette(
    bg_canvas="#0A0A0F",
    bg_surface="#12121A",
    bg_subtle="#1A1A2E",
    border_muted="#E94560",
    text_primary="#EAEAEA",
    text_secondary="#9D9DA6",
    text_muted="#5E5E6E",
    accent_primary="#E94560",
    accent_hover="#FF6B81",
    accent_active="#C23152",
    accent_subtle="#E9456026",
    manga_speed_line="#E94560",
    manga_panel_border="#2A2A3E",
    manga_glow="#FFD700",
    manga_shadow="#0D0D1A",
    manga_energy="#00D4FF",
)


@dataclass(frozen=True)
class Typography:
    font_family: str = "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, monospace"
    font_manga_title: str = "'Bangers', Impact, 'Arial Black', sans-serif"
    font_manga_body: str = "'Chakra Petch', 'Rajdhani', sans-serif"
    size_xs: int = 11
    size_sm: int = 12
    size_md: int = 14
    size_lg: int = 16
    size_xl: int = 20
    size_2xl: int = 24
    size_3xl: int = 32
    size_4xl: int = 40

    weight_regular: int = 400
    weight_medium: int = 500
    weight_bold: int = 700

    line_height_tight: float = 1.2
    line_height_normal: float = 1.5
    line_height_relaxed: float = 1.75


@dataclass(frozen=True)
class SpacingScale:
    base: int = 4
    space_1: int = 4
    space_2: int = 8
    space_3: int = 12
    space_4: int = 16
    space_6: int = 24
    space_8: int = 32
    space_12: int = 48
    space_16: int = 64
    space_24: int = 96


@dataclass(frozen=True)
class AnimationTokens:
    duration_fast: str = "200ms"
    duration_normal: str = "400ms"
    duration_slow: str = "800ms"
    ease_in_out: str = "cubic-bezier(0.4, 0, 0.2, 1)"
    ease_typewriter: str = "steps(30, end)"


COLORS = ColorPalette()
TYPOGRAPHY = Typography()
SPACING = SpacingScale()
ANIMATIONS = AnimationTokens()


def get_color(name: str, theme: str = "dark") -> str:
    """Retrieve a color hex string by attribute name."""
    palette = MANGA_COLORS if theme == "manga" else COLORS
    if not hasattr(palette, name):
        raise AttributeError(f"Color token '{name}' does not exist in ColorPalette.")
    return getattr(palette, name)  # type: ignore[no-any-return]


def get_spacing(level: int) -> int:
    """Retrieve spacing value in pixels for scale level (1, 2, 3, 4, 6, 8, 12, 16, 24)."""
    attr_name = f"space_{level}"
    if not hasattr(SPACING, attr_name):
        raise ValueError(f"Invalid spacing scale level: {level}")
    return getattr(SPACING, attr_name)  # type: ignore[no-any-return]


def to_css_variables(
    palette_override: dict[str, str] | None = None,
    theme: str | None = None,
) -> str:
    """Compile tokens into an SVG-compatible CSS variable block."""
    palette = MANGA_COLORS if theme == "manga" else COLORS
    if palette_override:
        # Construct dynamic palette override
        palette_dict = {**palette.__dict__, **palette_override}
        palette = ColorPalette(**palette_dict)

    css_lines = [
        ":root {",
        f"  --font-family: {TYPOGRAPHY.font_family};",
        f"  --font-manga-title: {TYPOGRAPHY.font_manga_title};",
        f"  --font-manga-body: {TYPOGRAPHY.font_manga_body};",
        f"  --bg-canvas: {palette.bg_canvas};",
        f"  --bg-surface: {palette.bg_surface};",
        f"  --bg-subtle: {palette.bg_subtle};",
        f"  --border-muted: {palette.border_muted};",
        f"  --text-primary: {palette.text_primary};",
        f"  --text-secondary: {palette.text_secondary};",
        f"  --text-muted: {palette.text_muted};",
        f"  --accent-primary: {palette.accent_primary};",
        f"  --accent-hover: {palette.accent_hover};",
        f"  --accent-active: {palette.accent_active};",
        f"  --accent-subtle: {palette.accent_subtle};",
        f"  --contribution-0: {palette.contribution_0};",
        f"  --contribution-1: {palette.contribution_1};",
        f"  --contribution-2: {palette.contribution_2};",
        f"  --contribution-3: {palette.contribution_3};",
        f"  --contribution-4: {palette.contribution_4};",
        f"  --status-success: {palette.success};",
        f"  --status-warning: {palette.warning};",
        f"  --status-error: {palette.error};",
        f"  --status-info: {palette.info};",
        f"  --manga-speed-line: {palette.manga_speed_line};",
        f"  --manga-panel-border: {palette.manga_panel_border};",
        f"  --manga-glow: {palette.manga_glow};",
        f"  --manga-shadow: {palette.manga_shadow};",
        f"  --manga-energy: {palette.manga_energy};",
        "}",
    ]
    return "\n".join(css_lines)
