# GitHub Profile 2.0 — System Architecture

## Overview
GitHub Profile 2.0 is a zero-runtime-dependency self-generating profile engine built in Python.

```
+------------------+      +-------------------+      +---------------------+
|   config.yml     | ---> | ConfigLoader      | ---> | ProfileConfig       |
+------------------+      +-------------------+      +---------------------+
                                                                |
+------------------+      +-------------------+                 v
| GitHub GraphQL   | ---> | GitHubAPIClient   | ---> [ SVG Engine (Jinja2) ]
+------------------+      +-------------------+                 |
                                                                v
+------------------+      +-------------------+      +---------------------+
| SVGOptimizer     | <--- | build.py          | ---> | READMEBuilder       |
+------------------+      +-------------------+      +---------------------+
                                    |                           |
                                    v                           v
                           [ generated/*.svg ]            [ README.md ]
```

## Core Modules
- `scripts/design_tokens.py`: Single source of truth for color palette, typography scale, 4px grid spacing, and CSS custom properties.
- `scripts/font_subset.py`: Embedded Base64 font loader for custom monospaced typography.
- `scripts/config_loader.py`: Pydantic schema validation for `config.yml`.
- `scripts/svg_engine.py`: Jinja2 template renderer with design token injection & XML validation.
- `scripts/cache_manager.py`: Atomic disk caching layer with TTL expiration.
- `scripts/github_api.py`: Resilient GraphQL API client with retries and mock fallback.
- `scripts/hero.py`: Animated terminal hero banner generator.
- `scripts/stats.py`: Analytics cards, contribution heatmaps, and language breakdown charts.
- `scripts/projects.py`: Showcase grid generator for featured software projects.
- `scripts/svg_optimizer.py`: SVG minifier stripping comments and truncating float precision.
- `scripts/build.py`: Main execution pipeline orchestrator.
