"""Launcher for examples — switch between Basic and Advanced with buttons."""

import flet as ft
from flet_circular_slider import FletCircularSlider


def basic_content():
    output = ft.Text("Drag the slider", color="#888888", size=14)

    def on_change(e):
        output.value = f"Value: {int(float(e.data))}"
        output.update()

    slider = FletCircularSlider(
        min=0, max=100, value=25, size=200,
        on_change=on_change,
    )
    return ft.Column([slider, output], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)


def advanced_content():
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
        min=0, max=100, value=60, size=280,
        start_angle=270, angle_range=300,
        progress_bar_width=20, track_width=4, handler_size=10,
        progress_bar_start_color="#00E5FF", progress_bar_end_color="#76FF03",
        track_color="#1a1a3a", dot_color="#FFFFFF",
        top_label="LEVEL", bottom_label="percent",
        inner_text="{value}%", inner_text_color="#00E5FF",
        hide_shadow=True,
        on_change=on_change, on_change_start=on_change_start, on_change_end=on_change_end,
    )
    return ft.Column([slider, status], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)


EXAMPLES = [
    ("Basic", basic_content),
    ("Advanced", advanced_content),
]


def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"
    page.title = "Circular Slider Examples"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    content_area = ft.Container(padding=30)
    buttons_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    def load_example(index):
        content_area.content = EXAMPLES[index][1]()
        content_area.update()
        for i, btn in enumerate(buttons_row.controls):
            btn.style = ft.ButtonStyle(
                bgcolor="#6C63FF" if i == index else "#2a2a4a",
                color="white",
            )
        buttons_row.update()

    for i, (name, _) in enumerate(EXAMPLES):
        buttons_row.controls.append(
            ft.Button(
                content=ft.Text(name),
                on_click=lambda e, idx=i: load_example(idx),
                style=ft.ButtonStyle(bgcolor="#2a2a4a", color="white"),
            )
        )

    page.add(buttons_row, content_area)
    load_example(0)


ft.run(main)
