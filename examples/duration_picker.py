"""Duration picker — label_formatter converts minutes to human-readable time."""

import flet as ft
from flet_circular_slider import FletCircularSlider


def format_duration(minutes: float) -> str:
    m = int(minutes)
    if m == 0:
        return "0m"
    h, rem = divmod(m, 60)
    if h == 0:
        return f"{rem}m"
    return f"{h}h {rem}m" if rem else f"{h}h"


def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    status = ft.Text("Set a duration", color="#888888", size=14)

    def on_change(e):
        mins = int(float(e.data))
        status.value = format_duration(mins)
        status.update()

    slider = FletCircularSlider(
        min=0,
        max=200,
        value=90,
        divisions=200,
        size=280,
        label_formatter=format_duration,
        top_label="DURATION",
        progress_bar_start_color="#FF6B35",
        progress_bar_end_color="#F7C948",
        track_color="#1a1a3a",
        inner_text_color="#F7C948",
        hide_shadow=True,
        on_change=on_change,
    )

    page.add(slider, status)


ft.run(main)
