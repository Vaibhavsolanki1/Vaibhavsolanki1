# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-01

### Added
- **Design System Engine**: Programmatic frozen dataclass color palette (`#0D1117` baseline, `#58A6FF` accent), 4px grid spacing, and Base64 font loader.
- **Core SVG Rendering Engine**: Jinja2 SVG template engine with style injection and XML AST syntax validation.
- **GitHub GraphQL API Client**: Single payload fetch with retries, language percentage normalization, disk caching, and static mock fallback.
- **Animated Hero Generator**: Terminal window banner with ASCII portrait parser and SMIL pulsing status indicator.
- **Analytics Visualization**: 52-week contribution heatmap grid, trigonometric polar-to-Cartesian donut arc chart, and summary statistics cards.
- **Project Showcase Generator**: Dynamic project cards grid with status badges and hashtag tech stack labels.
- **Build Pipeline & CLI**: Incremental SHA-256 asset diff checker and markdown profile compiler (`python scripts/build.py`).
- **Automation & Quality Toolchain**: Daily GitHub Actions workflow (`generate-readme.yml`), PR QA workflow (`qa-checks.yml`), SVG minification pass, and comprehensive test suite with 92% statement coverage.
