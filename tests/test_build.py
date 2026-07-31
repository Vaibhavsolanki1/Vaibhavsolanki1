"""
Unit tests for Main Build Pipeline (Phase 3)
"""

from pathlib import Path

from scripts.build import compute_sha256, run_pipeline, write_asset_if_changed


def test_compute_sha256() -> None:
    """Verify SHA-256 computation integrity."""
    h1 = compute_sha256("test content")
    h2 = compute_sha256("test content")
    h3 = compute_sha256("different content")

    assert h1 == h2
    assert h1 != h3


def test_write_asset_if_changed(tmp_path: Path) -> None:
    """Verify incremental asset writing logic based on content SHA-256."""
    target_file = tmp_path / "asset.svg"

    # Initial write should return True
    written = write_asset_if_changed(target_file, "<svg>1</svg>")
    assert written is True
    assert target_file.read_text(encoding="utf-8") == "<svg>1</svg>"

    # Identical write should return False (no disk rewrite)
    written_again = write_asset_if_changed(target_file, "<svg>1</svg>")
    assert written_again is False

    # Force write should return True
    written_force = write_asset_if_changed(target_file, "<svg>1</svg>", force=True)
    assert written_force is True


def test_run_pipeline() -> None:
    """Verify full end-to-end pipeline execution."""
    success = run_pipeline(config_path="config.yml", force=True)
    assert success is True
    assert Path("generated/hero.svg").exists()
    assert Path("README.md").exists()
