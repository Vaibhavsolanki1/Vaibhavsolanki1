# GitHub Profile 2.0 — Manga Protagonist Hybrid System Architecture

## Overview
GitHub Profile 2.0 implements a **Manga-Themed Hybrid Architecture** where the profile portrays the developer as an anime/manga protagonist ("The Code Architect"). It combines custom-crafted vector SVG branding components with real-time live GitHub statistics widgets.

```
                  MANGA PROTAGONIST HYBRID ARCHITECTURE FLOW
+-----------------------------------------------------------------------------+
|                                                                             |
|  LOCAL PYTHON SVG GENERATION ENGINE                                         |
|  +------------------+     +--------------------+     +-------------------+  |
|  | config.yml       | --> | ProfileConfig      | --> | Jinja2 SVGEngine  |  |
|  | (manga enabled)  |     | + MangaConfigModel |     | + Manga Tokens    |  |
|  +------------------+     +--------------------+     +-------------------+  |
|                                                                |            |
|                                                                v            |
|  [ Generated Manga Assets:                                                  |
|    - hero.svg        (Manga Chapter Title Page & Protagonist Character Art) |
|    - projects.svg    (Active Quests Board - Maitri, Oasis, Mantri)          |
|    - power_level.svg (Anime Power Level Assessment & S-Tier Rank Gauge)     |
|    - story_arc.svg   (Connected Manga Story Panels & Timeline) ]            |
|                                                                |            |
+----------------------------------------------------------------|------------+
                                                                 |
                                                                 v
+-----------------------------------------------------------------------------+
|  HYBRID README ASSEMBLER (readme_builder.py)                                |
|  +-----------------------------------------------------------------------+  |
|  | 1. Hero Manga Chapter Banner (generated/hero.svg)                     |  |
|  | 2. Character Profile & Epithet (Markdown)                             |  |
|  | 3. Manga Power Level Assessment (generated/power_level.svg)           |  |
|  | 4. Live GitHub Statistics & Streaks (Manga Crimson Themed Widgets)    |  |
|  | 5. Active Quests Board (generated/projects.svg)                       |  |
|  | 6. Arsenal & Abilities Tech Stack (Markdown)                          |  |
|  | 7. Story Arc Timeline (generated/story_arc.svg)                        |  |
|  | 8. Guild Contact Section (Markdown)                                   |  |
|  | 9. Footer with "To Be Continued..." // 続く (Markdown)                |  |
|  +-----------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------+
```

## Why Hybrid Manga Architecture?
1. **Dynamic Protagonist Persona**: Portrays the engineer as a powerful anime protagonist with custom vector illustration, glowing aura effects, speed lines, and chapter titles.
2. **Zero Maintenance for Live Stats**: Commit totals, active streaks, and language byte percentages render dynamically via trusted live widgets with matching dark/crimson manga themes (`bg_color=0A0A0F&border_color=E94560`).
3. **Immersive Storytelling**: Transforms standard project cards into an "Active Quests Board" (Maitri, Oasis, Mantri) and the engineering timeline into a manga "Story Arc".
4. **Ultra-Fast Build Time**: Full SVG compilation and README assembly completes in **< 0.15 seconds**.

## Core Modules
- `scripts/design_tokens.py`: Single source of truth for dark and manga color palettes (`#0A0A0F` canvas, `#E94560` crimson accent, `#00D4FF` energy glow), typography scale (`Bangers`, `Chakra Petch`), and CSS variables.
- `scripts/font_subset.py`: Typography and `@font-face` generation supporting both monospaced fonts and manga display typefaces.
- `scripts/config_loader.py`: Type-safe Pydantic schema validation for `config.yml` including `MangaConfigModel` and `StoryArcModel`.
- `scripts/svg_engine.py`: Jinja2 template renderer with dynamic design system token injection and XML validation.
- `scripts/protagonist.py`: Manga character vector illustration loader and renderer with dynamic SMIL aura and entrance animations.
- `scripts/hero.py`: Manga chapter title page banner generator (`generated/hero.svg`).
- `scripts/power_level.py`: GitHub activity to anime power gauge mapper with S/A/B/C tier calculation (`generated/power_level.svg`).
- `scripts/projects.py`: Quest board cards generator with difficulty ratings and status badges (`generated/projects.svg`).
- `scripts/story_arc.py`: Connected manga narrative timeline generator (`generated/story_arc.svg`).
- `scripts/animation.py`: SMIL SVG animation generators for speed lines, energy aura, power bar fills, and sparkles.
- `scripts/svg_optimizer.py`: SVG minifier and precision optimizer.
- `scripts/build.py`: Main hybrid execution pipeline orchestrator.
