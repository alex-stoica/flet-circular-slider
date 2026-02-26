"""Minimal circular slider — core values + on_change event."""

import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    output = ft.Text("Drag the slider", color="#888888", size=14)

    def on_change(e):
        output.value = f"Value: {int(float(e.data))}"
        output.update()

    slider = FletCircularSlider(
        min=0,
        max=100,
        value=25,
        size=200,
        on_change=on_change,
    )

    page.add(slider, output)


ft.run(main)
