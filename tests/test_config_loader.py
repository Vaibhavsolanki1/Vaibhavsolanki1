"""
Unit tests for Configuration Loader (Phase 2)
"""

from pathlib import Path

import pytest

from scripts.config_loader import ProfileConfig, load_config


def test_load_config_valid() -> None:
    """Verify loading real config.yml file."""
    config = load_config("config.yml")
    assert isinstance(config, ProfileConfig)
    assert config.profile.name == "Vaibhav Solanki"
    assert config.github.username == "vaibhavsolanki1"
    assert len(config.projects) >= 1


def test_load_config_missing_file(tmp_path: Path) -> None:
    """Verify FileNotFoundError raised for non-existent path."""
    missing = tmp_path / "non_existent.yml"
    with pytest.raises(FileNotFoundError):
        load_config(missing)


def test_load_config_empty_file(tmp_path: Path) -> None:
    """Verify ValueError raised for empty YAML file."""
    empty_file = tmp_path / "empty.yml"
    empty_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(empty_file)
