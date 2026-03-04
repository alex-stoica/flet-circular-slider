from dataclasses import field
from typing import Callable, Optional

import flet as ft
from flet.controls.control_event import ControlEventHandler


def _canonical_key(val: float) -> str:
    if val == int(val):
        return str(int(val))
    return f"{val:.10f}".rstrip("0").rstrip(".")


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
    progress_bar_colors: Optional[list[ft.ColorValue]] = None

    # Interaction
    disabled: bool = False

    # Labels
    top_label: Optional[str] = None
    bottom_label: Optional[str] = None
    inner_text: Optional[str] = None
    inner_text_color: Optional[ft.ColorValue] = None
    inner_text_size: Optional[float] = None
    inner_text_font_weight: Optional[str] = None
    inner_text_font_family: Optional[str] = None
    top_label_color: Optional[ft.ColorValue] = None
    top_label_size: Optional[float] = None
    top_label_font_weight: Optional[str] = None
    top_label_font_family: Optional[str] = None
    bottom_label_color: Optional[ft.ColorValue] = None
    bottom_label_size: Optional[float] = None
    bottom_label_font_weight: Optional[str] = None
    bottom_label_font_family: Optional[str] = None
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
                cache_key = (self.min, self.max, self.divisions, id(self.label_formatter))
                if getattr(self, "_label_cache_key", None) == cache_key:
                    return
                step = (self.max - self.min) / self.divisions
                self.label_map = {}
                for i in range(self.divisions + 1):
                    val = self.min + i * step
                    self.label_map[_canonical_key(val)] = self.label_formatter(val)
                self._label_cache_key = cache_key
            else:
                raise ValueError(
                    "label_formatter requires divisions to be set — "
                    "it controls how many labels are pre-computed"
                )
