# GitHub Profile 2.0 — Hybrid System Architecture

## Overview
GitHub Profile 2.0 implements a **Hybrid Architecture** combining locally generated vector SVG personal branding components with real-time live GitHub statistics widgets.

```
                  HYBRID ARCHITECTURE FLOW
+------------------------------------------------------------------------+
|                                                                        |
|  LOCAL PYTHON SVG GENERATION ENGINE                                    |
|  +------------------+     +---------------+     +-------------------+  |
|  | config.yml       | --> | ProfileConfig | --> | Jinja2 SVGEngine  |  |
|  +------------------+     +---------------+     +-------------------+  |
|                                                           |            |
|                                                           v            |
|  [ Personal Branding SVGs: hero.svg, projects.svg ] ──────+            |
|                                                           |            |
+-----------------------------------------------------------|------------+
                                                            |
                                                            v
+------------------------------------------------------------------------+
|  HYBRID README ASSEMBLER (readme_builder.py)                           |
|  +------------------------------------------------------------------+  |
|  | 1. Hero Terminal SVG (Generated)                                 |  |
|  | 2. About Me Section (Markdown)                                   |  |
|  | 3. Live GitHub Statistics Widget (anuraghazra/github-readme-stats)|  |
|  | 4. Live GitHub Streak Widget (denvercoder1/readme-streak-stats)  |  |
|  | 5. Live Top Languages Widget (anuraghazra/top-langs)             |  |
|  | 6. Featured Projects Showcase SVG (Generated)                    |  |
|  | 7. Tech Stack & Skills (Markdown)                                |  |
|  | 8. Engineering Timeline & ICPC Journey (Markdown)                |  |
|  | 9. Connect & Contact Section (Markdown)                          |  |
|  | 10. Footer (Generated SVG / Markdown)                            |  |
|  +------------------------------------------------------------------+  |
+------------------------------------------------------------------------+
```

## Why Hybrid Architecture?
1. **Zero Maintenance for Stats**: GitHub statistics, commit totals, streaks, and language byte percentages are rendered dynamically by trusted live widgets in real-time without requiring API key management or background sync jobs.
2. **Branding Control**: High-impact visual branding sections (Hero Terminal with ASCII name, pulsing status indicator, and project cards) remain 100% custom-crafted by your own Python engine.
3. **Ultra-Fast Build Time**: Build pipeline execution runs in **< 0.1 seconds** locally.

## Core Modules
- `scripts/design_tokens.py`: Single source of truth for color palette (`#0D1117` baseline, `#58A6FF` accent), typography scale, 4px grid spacing, and CSS custom properties.
- `scripts/font_subset.py`: Embedded Base64 font loader for custom monospaced typography.
- `scripts/config_loader.py`: Pydantic schema validation for `config.yml`.
- `scripts/svg_engine.py`: Jinja2 template renderer with design token injection & XML validation.
- `scripts/hero.py`: Animated terminal hero banner generator (`generated/hero.svg`).
- `scripts/projects.py`: Showcase grid generator for featured software projects (`generated/projects.svg`).
- `scripts/svg_optimizer.py`: SVG minifier stripping comments and truncating float precision.
- `scripts/build.py`: Main hybrid execution pipeline orchestrator.
- `deprecated/stats.py`: Legacy stat calculation module (deprecated in v1.1.0).
