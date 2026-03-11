"""Feature demo -- disabled mode, text styling, and multi-color gradients."""

import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 40
    page.scroll = ft.ScrollMode.AUTO

    # -- Slider 1: disabled gauge with toggle --

    temp_slider = FletCircularSlider(
        min=0,
        max=120,
        value=72,
        size=200,
        divisions=120,
        disabled=True,
        start_angle=150,
        angle_range=240,
        progress_bar_start_color="#FF6B35",
        progress_bar_end_color="#FF2020",
        track_color="#2a2a4a",
        inner_text="{value}°C",
        inner_text_color="#FF6B35",
        top_label="CPU TEMP",
        top_label_color="#FF6B35",
        top_label_size=14,
        bottom_label="disabled",
        bottom_label_color="#666666",
        bottom_label_size=11,
        hide_shadow=True,
    )

    toggle_btn = ft.Button(
        "Enable",
        on_click=lambda _: _toggle_disabled(),
        bgcolor="#2a2a4a",
        color="#ffffff",
    )

    def _toggle_disabled():
        temp_slider.disabled = not temp_slider.disabled
        toggle_btn.text = "Enable" if temp_slider.disabled else "Disable"
        temp_slider.bottom_label = "disabled" if temp_slider.disabled else "enabled"
        temp_slider.update()
        toggle_btn.update()

    # -- Slider 2: text styling -- default vs custom side by side --

    default_slider = FletCircularSlider(
        min=0,
        max=100,
        value=75,
        size=140,
        divisions=100,
        progress_bar_start_color="#6C63FF",
        progress_bar_end_color="#00D2FF",
        track_color="#2a2a4a",
        top_label="VOLUME",
        bottom_label="default sizes",
        hide_shadow=True,
    )

    styled_slider = FletCircularSlider(
        min=0,
        max=100,
        value=75,
        size=140,
        divisions=100,
        progress_bar_start_color="#6C63FF",
        progress_bar_end_color="#00D2FF",
        track_color="#2a2a4a",
        inner_text_color="#00D2FF",
        inner_text_size=52,
        top_label="VOLUME",
        top_label_color="#FF4081",
        top_label_size=20,
        bottom_label="custom sizes",
        bottom_label_color="#00D2FF",
        bottom_label_size=14,
        hide_shadow=True,
    )

    # -- Slider 3: rainbow gradient --

    rainbow_slider = FletCircularSlider(
        min=0,
        max=100,
        value=80,
        size=200,
        divisions=100,
        progress_bar_colors=["#FF0000", "#FF8800", "#FFDD00", "#00CC44", "#00BBFF"],
        track_color="#2a2a4a",
        inner_text_color="#FFDD00",
        inner_text_size=36,
        top_label="SPECTRUM",
        top_label_color="#FF8800",
        top_label_size=14,
        bottom_label="5-color gradient",
        bottom_label_color="#00BBFF",
        bottom_label_size=11,
        hide_shadow=True,
    )

    # -- Layout --

    def _section(title, content):
        return ft.Column(
            [ft.Text(title, size=14, color="#888888"), content],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

    styled_pair = ft.Row(
        [
            ft.Column([default_slider, ft.Text("default", size=11, color="#555555")],
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Text("vs", size=16, color="#555555"),
            ft.Column([styled_slider, ft.Text("custom", size=11, color="#555555")],
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )

    page.add(
        ft.Text("Feature demo", size=24, weight=ft.FontWeight.BOLD, color="#ffffff"),
        ft.Divider(color="#333333"),
        ft.ResponsiveRow(
            [
                ft.Container(
                    _section("Disabled mode", ft.Column(
                        [temp_slider, toggle_btn],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10,
                    )),
                    col={"xs": 12, "md": 4},
                ),
                ft.Container(
                    _section("Text styling", styled_pair),
                    col={"xs": 12, "md": 4},
                ),
                ft.Container(
                    _section("Multi-color gradient", rainbow_slider),
                    col={"xs": 12, "md": 4},
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


ft.run(main)
