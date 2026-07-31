from pathlib import Path

from scripts.font_subset import encode_font_to_base64, generate_font_face_css


def test_encode_font_non_existent(tmp_path: Path) -> None:
    """Verify non-existent font file returns None."""
    missing_file = tmp_path / "missing.ttf"
    assert encode_font_to_base64(missing_file) is None


def test_encode_font_existing(tmp_path: Path) -> None:
    """Verify existing file encodes to valid Base64 string."""
    dummy_font = tmp_path / "test_font.ttf"
    dummy_font.write_bytes(b"dummy font data 12345")

    encoded = encode_font_to_base64(dummy_font)
    assert encoded is not None
    assert isinstance(encoded, str)
    assert len(encoded) > 0


def test_generate_font_face_css_fallback(tmp_path: Path) -> None:
    """Verify CSS generator uses system fallback when font file is absent."""
    missing_file = tmp_path / "missing.ttf"
    css = generate_font_face_css(missing_file)
    assert "@font-face" in css
    assert "local('JetBrains Mono')" in css
