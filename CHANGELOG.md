# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-01

### Changed
- **Hybrid Architecture Refactor**: Converted profile pipeline into a Hybrid system. Personal branding assets (Hero Terminal SVG, ASCII Name, Projects Showcase) are generated locally by Python engine; statistics, streaks, and top languages are now rendered via trusted live widgets (`github-readme-stats`, `github-readme-streak-stats`).
- **Streamlined Build Pipeline**: Updated `scripts/build.py` to generate only Hero and Projects SVGs and compile `README.md`, reducing build overhead to <0.1 seconds.
- **Deprecated Module**: Moved `scripts/stats.py` to `deprecated/stats.py` as a legacy module.

## [1.0.0] - 2026-08-01

### Added
- **Design System Engine**: Frozen dataclass color palette, 4px grid spacing, Base64 font loader.
- **Core SVG Engine**: Jinja2 template renderer with XML AST syntax validation.
- **Animated Hero Generator**: Terminal window banner with exact ASCII portrait banner for **VAIBHAV** and SMIL pulsing status indicator.
- **Project Showcase Generator**: Dynamic project cards grid with status badges.
- **Automation & Toolchain**: GitHub Actions workflow and full test suite with 92% statement coverage.
