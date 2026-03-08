"""Performance and correctness demo — shows event dedup + fractional range fix."""

import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#0f0f1a"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    page.add(ft.Text("Performance & correctness demo", size=22, weight=ft.FontWeight.BOLD, color="#e0e0e0"))

    # --- Section 1: event counter (shows dedup working) ---
    event_count = 0
    value_changes = 0
    last_value = [None]

    count_label = ft.Text("Events fired: 0  |  Value changes: 0", color="#aaaaaa", size=13)
    current_val = ft.Text("Drag the slider", color="#888888", size=14)

    def on_change_counted(e):
        nonlocal event_count, value_changes
        event_count += 1
        val = int(e.data)
        if last_value[0] != val:
            value_changes += 1
            last_value[0] = val
        count_label.value = f"Events fired: {event_count}  |  Value changes: {value_changes}"
        current_val.value = f"Value: {val}"
        count_label.update()
        current_val.update()

    def reset_counter(e):
        nonlocal event_count, value_changes
        event_count = 0
        value_changes = 0
        last_value[0] = None
        count_label.value = "Events fired: 0  |  Value changes: 0"
        current_val.value = "Drag the slider"
        count_label.update()
        current_val.update()

    counter_slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        divisions=20,
        size=220,
        inner_text="{value}%",
        inner_text_color="#76FF03",
        progress_bar_start_color="#76FF03",
        progress_bar_end_color="#00E5FF",
        track_color="#1a1a3a",
        top_label="EVENT DEDUP",
        hide_shadow=True,
        on_change=on_change_counted,
    )

    page.add(
        ft.Container(height=20),
        ft.Text("1. Event deduplication", size=16, weight=ft.FontWeight.W_600, color="#76FF03"),
        ft.Text(
            "With 20 divisions, dragging across the full range should fire ~20 events, not ~60/sec.",
            color="#777777", size=12,
        ),
        ft.Container(height=10),
        counter_slider,
        count_label,
        current_val,
        ft.TextButton("Reset counter", on_click=reset_counter),
    )

    # --- Section 2: fractional range (correctness fix) ---
    frac_label = ft.Text("Drag to see fractional labels", color="#888888", size=14)

    def on_frac_change(e):
        frac_label.value = f"Raw event data: {e.data}"
        frac_label.update()

    frac_slider = FletCircularSlider(
        min=0,
        max=1,
        value=0.5,
        divisions=4,
        size=220,
        label_formatter=lambda v: f"{v:.0%}",
        inner_text_color="#FF6B35",
        progress_bar_start_color="#FF6B35",
        progress_bar_end_color="#F7C948",
        track_color="#1a1a3a",
        top_label="FRACTIONAL",
        hide_shadow=True,
        on_change=on_frac_change,
    )

    page.add(
        ft.Container(height=30),
        ft.Text("2. Fractional range fix", size=16, weight=ft.FontWeight.W_600, color="#FF6B35"),
        ft.Text(
            "min=0, max=1, divisions=4. Labels should show 0%, 25%, 50%, 75%, 100% — not all '0%' or '1%'.",
            color="#777777", size=12,
        ),
        ft.Container(height=10),
        frac_slider,
        frac_label,
    )

    # --- Section 3: integer range regression check ---
    int_label = ft.Text("Set a duration", color="#888888", size=14)

    def fmt_duration(minutes: float) -> str:
        m = int(minutes)
        if m == 0:
            return "0m"
        h, rem = divmod(m, 60)
        if h == 0:
            return f"{rem}m"
        return f"{h}h {rem}m" if rem else f"{h}h"

    def on_int_change(e):
        int_label.value = fmt_duration(int(e.data))
        int_label.update()

    int_slider = FletCircularSlider(
        min=0,
        max=120,
        value=45,
        divisions=120,
        size=220,
        label_formatter=fmt_duration,
        inner_text_color="#00BCD4",
        progress_bar_start_color="#00BCD4",
        progress_bar_end_color="#B2FF59",
        track_color="#1a1a3a",
        top_label="DURATION",
        hide_shadow=True,
        on_change=on_int_change,
    )

    page.add(
        ft.Container(height=30),
        ft.Text("3. Integer range regression", size=16, weight=ft.FontWeight.W_600, color="#00BCD4"),
        ft.Text(
            "min=0, max=120 minutes, divisions=120. Labels should still show '45m', '1h 30m', etc.",
            color="#777777", size=12,
        ),
        ft.Container(height=10),
        int_slider,
        int_label,
    )


ft.run(main)
