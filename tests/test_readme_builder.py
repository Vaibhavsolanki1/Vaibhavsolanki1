"""
Unit tests for README Assembler (Phase 3)
"""

from pathlib import Path

from scripts.readme_builder import READMEBuilder


def test_readme_builder_render() -> None:
    """Verify README markdown rendering from template and context."""
    builder = READMEBuilder(templates_dir="templates")
    context = {
        "config": {
            "profile": {
                "status": "Testing status",
                "focus": "Testing focus",
                "location": "India",
            }
        },
        "assets": {
            "hero": "generated/hero.svg",
        },
    }

    markdown = builder.build(context)

    assert "![Hero Banner](generated/hero.svg)" in markdown
    assert "Testing status" in markdown


def test_readme_builder_save(tmp_path: Path) -> None:
    """Verify saving markdown content to file."""
    builder = READMEBuilder(templates_dir="templates")
    target_file = tmp_path / "TEST_README.md"

    builder.save("# Test Title", output_path=target_file)

    assert target_file.exists()
    assert target_file.read_text(encoding="utf-8") == "# Test Title"
