"""Advanced circular slider — every customization option demonstrated."""

import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#0a0a1a"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    status = ft.Text("Drag the slider", color="#888888", size=14)

    def on_change(e):
        val = int(float(e.data))
        status.value = f"Level: {val}%"
        status.update()

    def on_change_start(e):
        status.value = "Adjusting..."
        status.update()

    def on_change_end(e):
        status.value = "Set!"
        status.update()

    slider = FletCircularSlider(
        min=0,
        max=100,
        value=60,
        size=280,
        # Geometry
        start_angle=270,
        angle_range=300,
        # Sizing
        progress_bar_width=20,
        track_width=4,
        handler_size=10,
        # Colors — cyan-to-green neon theme
        progress_bar_start_color="#00E5FF",
        progress_bar_end_color="#76FF03",
        track_color="#1a1a3a",
        dot_color="#FFFFFF",
        # Labels & inner text
        top_label="LEVEL",
        bottom_label="percent",
        inner_text="{value}%",
        inner_text_color="#00E5FF",
        # Shadow
        hide_shadow=True,
        # All 3 events
        on_change=on_change,
        on_change_start=on_change_start,
        on_change_end=on_change_end,
    )

    page.add(slider, status)


ft.run(main)
