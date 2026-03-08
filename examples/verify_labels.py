"""Verification demo for label fix and new text styling properties.

What to watch for:
1. LEFT slider — "SPEED" above, "km/h" below, bold number in the center.
   These labels were DEAD before the fix (innerWidget replaced SliderLabel entirely).
2. CENTER slider — "TEMP" in monospace font, thin (w300) center number, "celsius" in monospace.
   Demonstrates inner_text_font_weight, inner_text_font_family, top/bottom_label_font_family.
3. RIGHT slider — plain number, no labels at all.
   Should look identical to the old behavior (no layout shift from the Column change).
"""

import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#0e0e1a"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30

    # 1. Labels with default styling — core bug fix verification
    labels_slider = FletCircularSlider(
        min=0,
        max=200,
        value=120,
        size=200,
        divisions=200,
        progress_bar_start_color="#00E5FF",
        progress_bar_end_color="#76FF03",
        track_color="#1a1a3a",
        inner_text_color="#00E5FF",
        top_label="SPEED",
        bottom_label="km/h",
        hide_shadow=True,
        on_change=lambda e: print(f"speed: {int(e.data)}"),
    )

    # 2. Labels with custom font weight + family — new properties
    styled_slider = FletCircularSlider(
        min=0,
        max=50,
        value=22,
        size=200,
        divisions=50,
        progress_bar_start_color="#FF6B35",
        progress_bar_end_color="#FF2020",
        track_color="#2a2a4a",
        inner_text="{value}°",
        inner_text_color="#FF6B35",
        inner_text_font_weight="w300",
        inner_text_font_family="monospace",
        top_label="TEMP",
        top_label_color="#FF6B35",
        top_label_font_weight="w400",
        top_label_font_family="monospace",
        bottom_label="celsius",
        bottom_label_color="#666666",
        bottom_label_font_weight="w400",
        bottom_label_font_family="monospace",
        hide_shadow=True,
    )

    # 3. No labels — backward compatibility check
    plain_slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        size=200,
        divisions=100,
        progress_bar_start_color="#6C63FF",
        progress_bar_end_color="#00D2FF",
        track_color="#2a2a4a",
        hide_shadow=True,
    )

    def _col(slider, caption):
        return ft.Column(
            [slider, ft.Text(caption, size=11, color="#555555")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )

    page.add(
        ft.Text("Label verification", size=20, weight=ft.FontWeight.BOLD, color="#ffffff"),
        ft.Text(
            'Left: labels visible? Center: thin monospace font? Right: plain number, no labels?',
            size=12, color="#888888",
        ),
        ft.Divider(color="#333333"),
        ft.Row(
            [
                _col(labels_slider, "labels (bug fix)"),
                _col(styled_slider, "font weight + family"),
                _col(plain_slider, "no labels (backward compat)"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
    )


ft.run(main)
