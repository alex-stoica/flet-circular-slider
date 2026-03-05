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

    _valid_weights = frozenset({
        "w100", "w200", "w300", "w400", "w500", "w600", "w700", "w800", "w900",
        "thin", "extraLight", "light", "normal", "medium", "semiBold", "bold", "extraBold", "black",
    })

    def before_update(self):
        super().before_update()

        # --- Property validation ---
        if self.min >= self.max:
            raise ValueError(f"min ({self.min}) must be less than max ({self.max})")
        self.value = max(self.min, min(self.max, self.value))

        if self.divisions is not None and self.divisions <= 0:
            raise ValueError(f"divisions must be positive, got {self.divisions}")
        if self.size <= 0:
            raise ValueError(f"size must be positive, got {self.size}")
        if not (1 <= self.angle_range <= 360):
            raise ValueError(f"angle_range must be 1-360, got {self.angle_range}")

        for attr in ("progress_bar_width", "track_width", "handler_size",
                     "inner_text_size", "top_label_size", "bottom_label_size"):
            v = getattr(self, attr)
            if v is not None and v <= 0:
                raise ValueError(f"{attr} must be positive, got {v}")

        if self.change_throttle_ms is not None and self.change_throttle_ms <= 0:
            raise ValueError(f"change_throttle_ms must be positive, got {self.change_throttle_ms}")

        for attr in ("inner_text_font_weight", "top_label_font_weight", "bottom_label_font_weight"):
            v = getattr(self, attr)
            if v is not None and v not in self._valid_weights:
                raise ValueError(f"{attr} must be one of {sorted(self._valid_weights)}, got {v!r}")

        if self.progress_bar_colors is not None and len(self.progress_bar_colors) < 2:
            raise ValueError("progress_bar_colors requires at least 2 colors")

        # --- Label formatter ---
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
