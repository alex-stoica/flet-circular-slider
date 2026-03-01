from dataclasses import field
from typing import Callable, Optional

import flet as ft
from flet.controls.control_event import ControlEventHandler


@ft.control("flet_circular_slider")
class FletCircularSlider(ft.LayoutControl):
    """A circular/radial slider control wrapping sleek_circular_slider Flutter package.

    Use as a duration picker, volume knob, or any value selector with a circular UI.
    """

    # Core values
    min: float = 0
    max: float = 100
    value: float = 50
    divisions: Optional[int] = None

    # Appearance
    size: float = 150
    start_angle: float = 150
    angle_range: float = 240
    counter_clockwise: bool = False
    animation_enabled: bool = True

    # Widths
    progress_bar_width: Optional[float] = None
    track_width: Optional[float] = None
    handler_size: Optional[float] = None

    # Colors
    track_color: Optional[ft.ColorValue] = None
    dot_color: Optional[ft.ColorValue] = None
    shadow_color: Optional[ft.ColorValue] = None
    hide_shadow: bool = False
    progress_bar_start_color: Optional[ft.ColorValue] = None
    progress_bar_end_color: Optional[ft.ColorValue] = None

    # Labels
    top_label: Optional[str] = None
    bottom_label: Optional[str] = None
    inner_text: Optional[str] = None
    inner_text_color: Optional[ft.ColorValue] = None
    label_formatter: Optional[Callable[[float], str]] = field(default=None, metadata={"skip": True})
    label_map: Optional[dict[str, str]] = None

    # Throttle
    change_throttle_ms: Optional[int] = None

    # Events
    on_change: Optional[ControlEventHandler["FletCircularSlider"]] = None
    on_change_start: Optional[ControlEventHandler["FletCircularSlider"]] = None
    on_change_end: Optional[ControlEventHandler["FletCircularSlider"]] = None

    def before_update(self):
        super().before_update()
        if self.label_formatter is not None:
            if self.divisions is not None and self.divisions > 0:
                step = (self.max - self.min) / self.divisions
                self.label_map = {}
                for i in range(self.divisions + 1):
                    val = self.min + i * step
                    snapped = round(val)
                    self.label_map[str(snapped)] = self.label_formatter(
                        float(snapped)
                    )
            else:
                raise ValueError(
                    "label_formatter requires divisions to be set — "
                    "it controls how many labels are pre-computed"
                )
