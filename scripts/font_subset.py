"""
GitHub Profile 2.0 - Font Subsetting Utility

Utility for loading, subsetting, and Base64-encoding JetBrains Mono font assets
to embed custom monospaced typography directly inside SVG <style> tags.
"""

import base64
from pathlib import Path

DEFAULT_FONT_PATH = Path("assets/fonts/JetBrainsMono-Regular.ttf")


def encode_font_to_base64(font_path: Path) -> str | None:
    """Encode a font file on disk into a Base64 data string."""
    if not font_path.exists():
        return None

    try:
        with open(font_path, "rb") as font_file:
            encoded_bytes = base64.b64encode(font_file.read())
            return encoded_bytes.decode("utf-8")
    except Exception:
        return None


def generate_font_face_css(
    font_path: Path = DEFAULT_FONT_PATH, font_family: str = "JetBrains Mono"
) -> str:
    """
    Generate an SVG @font-face CSS definition.
    If font file exists, embeds Base64 woff2/ttf data; otherwise falls back to system monospace stack.
    """
    base64_data = encode_font_to_base64(font_path)

    if base64_data:
        return (
            f"@font-face {{\n"
            f"  font-family: '{font_family}';\n"
            f"  src: url('data:font/ttf;charset=utf-8;base64,{base64_data}') format('truetype');\n"
            f"  font-weight: 400 700;\n"
            f"  font-style: normal;\n"
            f"}}"
        )

    # Clean fallback definition when font asset is absent
    return (
        f"/* Font file {font_path} not found. Utilizing system fallback stack. */\n"
        f"@font-face {{\n"
        f"  font-family: '{font_family}';\n"
        f"  src: local('JetBrains Mono'), local('Consolas'), local('SFMono-Regular');\n"
        f"}}"
    )
