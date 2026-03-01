"""Programmatic value updates demo — two sliders + auto-animation.

Works in flet build web (no buttons needed). The main slider is driven by:
1. Auto-animation on load (cycles through preset values)
2. A controller slider whose drag drives the main slider
3. Direct drag on the main slider itself
"""

import asyncio

import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 40

    status = ft.Text("Starting auto-demo...", color="#888888", size=14)

    # --- Main slider ---
    slider = FletCircularSlider(
        min=0,
        max=100,
        value=0,
        size=250,
        progress_bar_start_color="#6C63FF",
        progress_bar_end_color="#00D2FF",
        track_color="#1a1a3a",
        inner_text_color="#00D2FF",
        hide_shadow=True,
        on_change=lambda e: _on_main_drag(e),
    )

    def _on_main_drag(e):
        v = int(float(e.data))
        status.value = f"Dragged to {v}"
        status.update()

    # --- Controller slider (smaller, drives main) ---
    controller_label = ft.Text("Controller", color="#FFA726", size=12)

    controller = FletCircularSlider(
        min=0,
        max=100,
        value=0,
        size=120,
        change_throttle_ms=200,
        progress_bar_start_color="#FFA726",
        progress_bar_end_color="#FFEE58",
        track_color="#1a1a3a",
        inner_text_color="#FFA726",
        hide_shadow=True,
        on_change=lambda e: _on_controller(e),
    )

    def _on_controller(e):
        v = int(float(e.data))
        slider.value = v
        slider.update()
        status.value = f"Controller: {v}"
        status.update()

    # --- Auto-animation on startup ---
    async def auto_demo():
        await asyncio.sleep(1)
        for v in [0, 25, 50, 75, 100, 50]:
            slider.value = v
            slider.update()
            status.value = f"Auto-demo: {v}"
            status.update()
            await asyncio.sleep(1)
        status.value = "Done — drag either slider"
        status.update()

    # --- Layout ---
    page.add(
        ft.Text(
            "Programmatic Updates",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#ffffff",
        ),
        slider,
        status,
        ft.Row(
            [ft.Column([controller, controller_label], horizontal_alignment=ft.CrossAxisAlignment.CENTER)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    page.run_task(auto_demo)


ft.run(main)
