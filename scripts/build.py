"""
GitHub Profile 2.0 - Main Build Pipeline Orchestrator

CLI entrypoint for running SVG section generators, verifying asset digests,
and rendering the final README.md profile page.
"""

import argparse
import hashlib
import sys
from pathlib import Path

# Ensure project root is on sys.path for direct invocation (python scripts/build.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config_loader import ProfileConfig, load_config
from scripts.github_api import GitHubAPIClient
from scripts.hero import generate_hero
from scripts.logger import get_logger
from scripts.projects import generate_projects
from scripts.readme_builder import READMEBuilder
from scripts.stats import generate_analytics
from scripts.svg_optimizer import optimize_svg

logger = get_logger("BuildPipeline")


def compute_sha256(content: str) -> str:
    """Compute SHA-256 digest hex string of text content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def write_asset_if_changed(
    output_file: Path, content: str, force: bool = False, optimize: bool = True
) -> bool:
    """
    Write content to disk only if file does not exist, force flag is set,
    or SHA-256 digest has changed. Returns True if written.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    target_content = optimize_svg(content) if optimize and output_file.suffix == ".svg" else content
    new_hash = compute_sha256(target_content)

    if not force and output_file.exists():
        existing_content = output_file.read_text(encoding="utf-8")
        existing_hash = compute_sha256(existing_content)
        if new_hash == existing_hash:
            logger.debug(f"Asset unchanged: {output_file.name} (SHA-256 matched)")
            return False

    output_file.write_text(target_content, encoding="utf-8")
    logger.info(f"Updated asset: {output_file.name}")
    return True


def run_pipeline(config_path: str = "config.yml", force: bool = False) -> bool:
    """Execute complete profile build pipeline."""
    logger.info("Initializing GitHub Profile 2.0 build pipeline...")

    config: ProfileConfig = load_config(config_path)
    output_dir = Path(config.system.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    asset_paths: dict[str, str] = {}

    # 1. Render Animated Hero SVG Section
    hero_svg = generate_hero(
        config, portrait_path="assets/data/portrait.txt", output_dir=output_dir
    )
    hero_file = output_dir / "hero.svg"
    write_asset_if_changed(hero_file, hero_svg, force=force)
    asset_paths["hero"] = f"{config.system.output_dir}/hero.svg"

    # 2. Render Analytics SVG Sections
    github_client = GitHubAPIClient(mock_fixture_path="tests/mock_github_data.json")
    analytics_assets = generate_analytics(
        config, github_client=github_client, output_dir=output_dir
    )
    asset_paths.update(analytics_assets)

    # 3. Render Projects Showcase SVG Section
    projects_svg = generate_projects(config, output_dir=output_dir)
    projects_file = output_dir / "projects.svg"
    write_asset_if_changed(projects_file, projects_svg, force=force)
    asset_paths["projects"] = f"{config.system.output_dir}/projects.svg"

    # Assemble README.md
    readme_builder = READMEBuilder(templates_dir="templates")
    context = {
        "config": config,
        "assets": asset_paths,
    }
    markdown_content = readme_builder.build(context)
    readme_builder.save(markdown_content, output_path="README.md")

    logger.info("Pipeline build completed successfully.")
    return True


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="GitHub Profile 2.0 Build Orchestrator")
    parser.add_argument("--config", default="config.yml", help="Path to config.yml")
    parser.add_argument("--force", action="store_true", help="Force rewrite all assets")

    args = parser.parse_args()

    try:
        success = run_pipeline(config_path=args.config, force=args.force)
        return 0 if success else 1
    except Exception as e:
        logger.error(f"Build pipeline failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
