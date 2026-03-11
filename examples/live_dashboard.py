"""Live dashboard -- full showcase of programmatic value updates.

Three ways to drive the main slider (all work in flet build web):
1. Auto-animation on startup -- cycles through preset values automatically
2. Controller slider -- drag the small slider to drive the big one
3. Colored preset squares -- click a Container to jump to a value
4. Direct drag on the main slider itself
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
        v = int(e.data)
        status.value = f"Dragged to {v}"
        status.update()

    # --- Controller slider ---
    controller = FletCircularSlider(
        min=0,
        max=100,
        value=0,
        size=120,
        progress_bar_start_color="#FFA726",
        progress_bar_end_color="#FFEE58",
        track_color="#1a1a3a",
        inner_text_color="#FFA726",
        hide_shadow=True,
        on_change=lambda e: _on_controller(e),
    )

    def _on_controller(e):
        v = int(e.data)
        slider.value = v
        slider.update()
        status.value = f"Controller: {v}"
        status.update()

    # --- Colored preset squares ---
    # Container on_click + adjacent Text labels (content children don't render in web)
    presets = [
        (0, "#EF5350", "0%"),
        (25, "#AB47BC", "25%"),
        (50, "#42A5F5", "50%"),
        (75, "#66BB6A", "75%"),
        (100, "#FFA726", "100%"),
    ]

    def make_preset(value, color, label):
        def on_click(e):
            slider.value = value
            slider.update()
            status.value = f"Preset: {value}"
            status.update()

        return ft.Column(
            [
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor=color,
                    border_radius=8,
                    on_click=on_click,
                ),
                ft.Text(label, color=color, size=11),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        )

    preset_row = ft.Row(
        [make_preset(v, c, l) for v, c, l in presets],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
    )

    # --- Auto-animation on startup ---
    async def auto_demo():
        await asyncio.sleep(1)
        for v in [0, 25, 50, 75, 100, 50]:
            slider.value = v
            slider.update()
            status.value = f"Auto-demo: {v}"
            status.update()
            await asyncio.sleep(0.8)
        status.value = "Done -- try the controller or presets"
        status.update()

    # --- Layout ---
    page.add(
        ft.Text(
            "Live Dashboard",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#ffffff",
        ),
        slider,
        status,
        ft.Row(
            [
                ft.Column(
                    [controller, ft.Text("Controller", color="#FFA726", size=12)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(height=16),
        ft.Text("Presets", color="#666666", size=12),
        preset_row,
    )

    page.run_task(auto_demo)


ft.run(main)
