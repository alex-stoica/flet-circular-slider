"""Comprehensive demo app for flet-circular-slider.

Mobile-friendly, scrollable, dark-themed. Tests all major features across 7 sections.
"""

import flet as ft
from flet_circular_slider import FletCircularSlider

BG = "#1a1a2e"
ACCENT = "#6C63FF"
ACCENT2 = "#00D2FF"


def section_title(text: str) -> ft.Text:
    return ft.Text(text, size=20, weight=ft.FontWeight.BOLD, color="#ffffff")


def hint(text: str) -> ft.Text:
    return ft.Text(text, size=12, color="#666666")


def divider() -> ft.Divider:
    return ft.Divider(color="#333355", height=30)


def main(page: ft.Page):
    page.bgcolor = BG
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    # ── 1. Basic ──
    basic_status = ft.Text("Drag the slider", color="#888888", size=14)
    basic_slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        divisions=100,
        size=200,
        progress_bar_start_color=ACCENT,
        progress_bar_end_color=ACCENT2,
        track_color="#1a1a3a",
        inner_text_color=ACCENT2,
        hide_shadow=True,
        on_change=lambda e: _update_text(basic_status, f"Value: {int(float(e.data))}"),
    )

    # ── 2. Styled ──
    styled_status = ft.Text("Multi-color gradient", color="#888888", size=14)
    styled_slider = FletCircularSlider(
        min=0,
        max=100,
        value=70,
        divisions=100,
        size=200,
        progress_bar_width=15,
        track_width=10,
        handler_size=18,
        progress_bar_colors=["#FF6B6B", "#FFA726", "#FFEE58", "#66BB6A", "#42A5F5"],
        track_color="#2a2a4a",
        inner_text_color="#FFA726",
        inner_text_size=28,
        inner_text_font_weight="bold",
        hide_shadow=True,
        on_change=lambda e: _update_text(styled_status, f"Styled: {int(float(e.data))}"),
    )

    # ── 3. Duration picker ──
    duration_status = ft.Text("15 min", color="#888888", size=14)

    def format_duration(val: float) -> str:
        return f"{int(val)} min"

    duration_slider = FletCircularSlider(
        min=0,
        max=60,
        value=15,
        divisions=12,
        size=200,
        progress_bar_start_color="#CE93D8",
        progress_bar_end_color="#F48FB1",
        track_color="#1a1a3a",
        inner_text_color="#CE93D8",
        hide_shadow=True,
        label_formatter=format_duration,
        on_change=lambda e: _update_text(duration_status, format_duration(int(float(e.data)))),
    )

    # ── 4. Disabled toggle ──
    disabled_status = ft.Text("Slider is enabled", color="#888888", size=14)
    disabled_slider = FletCircularSlider(
        min=0,
        max=100,
        value=40,
        divisions=100,
        size=180,
        progress_bar_start_color="#4DB6AC",
        progress_bar_end_color="#80CBC4",
        track_color="#1a1a3a",
        inner_text_color="#4DB6AC",
        hide_shadow=True,
        disabled=False,
    )

    def toggle_disabled(_e):
        disabled_slider.disabled = not disabled_slider.disabled
        disabled_slider.update()
        state = "disabled" if disabled_slider.disabled else "enabled"
        disabled_status.value = f"Slider is {state}"
        disabled_status.update()

    toggle_btn = ft.ElevatedButton("Toggle disabled", on_click=toggle_disabled)

    # ── 5. Programmatic update ──
    prog_status = ft.Text("Press a button", color="#888888", size=14)
    prog_slider = FletCircularSlider(
        min=0,
        max=100,
        value=0,
        divisions=100,
        size=180,
        animation_enabled=False,
        progress_bar_start_color="#FFB74D",
        progress_bar_end_color="#FF8A65",
        track_color="#1a1a3a",
        inner_text_color="#FFB74D",
        hide_shadow=True,
    )

    def set_value(val):
        def handler(_e):
            prog_slider.value = val
            prog_slider.update()
            prog_status.value = f"Set to {val}"
            prog_status.update()
        return handler

    prog_buttons = ft.Row(
        [ft.ElevatedButton(str(v), on_click=set_value(v)) for v in [0, 25, 50, 75, 100]],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
    )

    # ── 6. Controller ──
    ctrl_status = ft.Text("Small drives big", color="#888888", size=14)
    big_slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        divisions=100,
        size=220,
        animation_enabled=False,
        progress_bar_start_color="#7986CB",
        progress_bar_end_color="#9FA8DA",
        track_color="#1a1a3a",
        inner_text_color="#7986CB",
        hide_shadow=True,
    )

    def on_ctrl_change(e):
        v = int(float(e.data))
        big_slider.value = v
        big_slider.update()
        ctrl_status.value = f"Controller -> {v}"
        ctrl_status.update()

    ctrl_slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        divisions=100,
        size=120,
        progress_bar_start_color="#FFA726",
        progress_bar_end_color="#FFEE58",
        track_color="#1a1a3a",
        inner_text_color="#FFA726",
        hide_shadow=True,
        change_throttle_ms=100,
        on_change=on_ctrl_change,
    )

    # ── 7. Event log ──
    event_log = ft.Column([], scroll=ft.ScrollMode.AUTO, height=150)

    def log_event(event_type: str):
        def handler(e):
            val = int(float(e.data))
            entry = ft.Text(f"{event_type}: {val}", size=11, color="#aaaaaa")
            event_log.controls.append(entry)
            if len(event_log.controls) > 30:
                event_log.controls.pop(0)
            event_log.update()
        return handler

    log_slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        divisions=100,
        size=180,
        progress_bar_start_color="#EF5350",
        progress_bar_end_color="#E57373",
        track_color="#1a1a3a",
        inner_text_color="#EF5350",
        hide_shadow=True,
        on_change=log_event("change"),
        on_change_start=log_event("start"),
        on_change_end=log_event("end"),
    )

    def _update_text(text_ctrl: ft.Text, value: str):
        text_ctrl.value = value
        text_ctrl.update()

    # ── Layout ──
    page.add(
        ft.Text("flet-circular-slider demo", size=26, weight=ft.FontWeight.BOLD, color="#ffffff"),
        hint("Scroll to see all 7 sections"),
        divider(),

        # 1
        section_title("1. Basic slider"),
        hint("Default config, value display on change"),
        basic_slider,
        basic_status,
        divider(),

        # 2
        section_title("2. Styled slider"),
        hint("Custom widths, multi-color gradient, font weight"),
        styled_slider,
        styled_status,
        divider(),

        # 3
        section_title("3. Duration picker"),
        hint("label_formatter + 12 divisions"),
        duration_slider,
        duration_status,
        divider(),

        # 4
        section_title("4. Disabled toggle"),
        hint("Button enables/disables the slider"),
        disabled_slider,
        toggle_btn,
        disabled_status,
        divider(),

        # 5
        section_title("5. Programmatic update"),
        hint("Buttons set specific values via .value + .update()"),
        prog_slider,
        prog_buttons,
        prog_status,
        divider(),

        # 6
        section_title("6. Controller"),
        hint("Small slider drives big slider via on_change"),
        big_slider,
        ft.Row(
            [ft.Column([ctrl_slider, ft.Text("Controller", size=12, color="#FFA726")],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ctrl_status,
        divider(),

        # 7
        section_title("7. Event log"),
        hint("on_change, on_change_start, on_change_end"),
        log_slider,
        ft.Container(
            content=event_log,
            bgcolor="#0d0d1a",
            border_radius=8,
            padding=10,
            width=350,
        ),
    )


ft.run(main)
