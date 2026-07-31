"""
GitHub Profile 2.0 - SVG Math & Chart Primitives Engine

Generates SVG element geometries for contribution heatmaps, donut chart arcs,
bar chart rects, and summary stat cards.
"""

import math
from typing import Any


def calculate_contribution_color(count: int) -> str:
    """Map daily contribution count into design token contribution color variable."""
    if count <= 0:
        return "var(--contribution-0)"
    elif count <= 3:
        return "var(--contribution-1)"
    elif count <= 7:
        return "var(--contribution-2)"
    elif count <= 12:
        return "var(--contribution-3)"
    else:
        return "var(--contribution-4)"


def render_heatmap_grid(
    weeks: list[dict[str, Any]],
    start_x: float = 24.0,
    start_y: float = 40.0,
    cell_size: float = 10.0,
    cell_gap: float = 3.0,
) -> str:
    """Render 52-week x 7-day contribution heatmap grid rect elements."""
    rects: list[str] = []

    for w_idx, week in enumerate(weeks):
        x = start_x + w_idx * (cell_size + cell_gap)
        days = week.get("contributionDays", [])

        for day in days:
            weekday = day.get("weekday", 0)  # 0 = Sunday, 6 = Saturday
            y = start_y + weekday * (cell_size + cell_gap)
            count = day.get("contributionCount", 0)
            date_str = day.get("date", "")
            fill_color = calculate_contribution_color(count)

            rects.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" '
                f'fill="{fill_color}"><title>{count} contributions on {date_str}</title></rect>'
            )

    return "\n".join(rects)


def render_donut_chart_paths(
    languages: list[dict[str, Any]],
    cx: float = 100.0,
    cy: float = 100.0,
    radius: float = 60.0,
    inner_radius: float = 40.0,
) -> str:
    """
    Render SVG donut chart arc paths from language percentage distribution list.
    Uses polar-to-Cartesian trigonometry math.
    """
    paths: list[str] = []
    current_angle = -90.0  # Start at top (12 o'clock)

    for lang in languages:
        percentage = lang.get("percentage", 0.0)
        if percentage <= 0:
            continue

        angle_span = (percentage / 100.0) * 360.0
        start_angle = current_angle
        end_angle = current_angle + angle_span
        current_angle = end_angle

        # If angle span is 360 degrees (single language), render circle
        if angle_span >= 359.9:
            color = lang.get("color", "var(--accent-primary)")
            paths.append(
                f'<circle cx="{cx}" cy="{cy}" r="{(radius + inner_radius)/2:.1f}" '
                f'stroke="{color}" stroke-width="{radius - inner_radius:.1f}" fill="none"/>'
            )

            break

        # Trigonometric polar to Cartesian coordinates
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        x1_outer = cx + radius * math.cos(start_rad)
        y1_outer = cy + radius * math.sin(start_rad)
        x2_outer = cx + radius * math.cos(end_rad)
        y2_outer = cy + radius * math.sin(end_rad)

        x1_inner = cx + inner_radius * math.cos(end_rad)
        y1_inner = cy + inner_radius * math.sin(end_rad)
        x2_inner = cx + inner_radius * math.cos(start_rad)
        y2_inner = cy + inner_radius * math.sin(start_rad)

        large_arc_flag = 1 if angle_span > 180 else 0
        color = lang.get("color", "var(--accent-primary)")

        path_d = (
            f"M {x1_outer:.2f} {y1_outer:.2f} "
            f"A {radius:.2f} {radius:.2f} 0 {large_arc_flag} 1 {x2_outer:.2f} {y2_outer:.2f} "
            f"L {x1_inner:.2f} {y1_inner:.2f} "
            f"A {inner_radius:.2f} {inner_radius:.2f} 0 {large_arc_flag} 0 {x2_inner:.2f} {y2_inner:.2f} "
            "Z"
        )

        paths.append(
            f'<path d="{path_d}" fill="{color}"><title>{lang["name"]}: {percentage}%</title></path>'
        )

    return "\n".join(paths)
