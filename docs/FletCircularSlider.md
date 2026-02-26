# FletCircularSlider

A circular/radial slider control. Wraps the [sleek_circular_slider](https://pub.dev/packages/sleek_circular_slider) Flutter package.

```python
from flet_circular_slider import FletCircularSlider
```

## Properties

### Core values

| Property | Type | Default | Description |
|---|---|---|---|
| `min` | `float` | `0` | Minimum slider value |
| `max` | `float` | `100` | Maximum slider value |
| `value` | `float` | `50` | Initial slider value (clamped to min/max) |

### Appearance

| Property | Type | Default | Description |
|---|---|---|---|
| `size` | `float` | `150` | Diameter of the slider in pixels |
| `start_angle` | `float` | `150` | Starting angle of the arc in degrees (0 = right, 90 = bottom, 180 = left, 270 = top) |
| `angle_range` | `float` | `240` | Total arc range in degrees. Use `360` for a full circle |
| `counter_clockwise` | `bool` | `False` | Reverse the drag direction |
| `animation_enabled` | `bool` | `True` | Animate from 0 to the initial value on first render |

### Sizing

These control the thickness of the slider components. If not set, they scale proportionally based on `size`.

| Property | Type | Default | Description |
|---|---|---|---|
| `progress_bar_width` | `float` | `size / 10` | Width of the colored progress arc |
| `track_width` | `float` | `progress_bar_width / 4` | Width of the background track |
| `handler_size` | `float` | `progress_bar_width / 5` | Radius of the drag handle dot |

### Colors

All color properties accept hex strings (`"#FF5733"`), Flet color constants (`ft.Colors.BLUE`), or `None` for the default.

| Property | Type | Default | Description |
|---|---|---|---|
| `progress_bar_start_color` | `ColorValue` | purple-pink-blue gradient | Gradient start color of the filled arc |
| `progress_bar_end_color` | `ColorValue` | purple-pink-blue gradient | Gradient end color of the filled arc. Both start and end must be set for a custom gradient |
| `track_color` | `ColorValue` | `#DCBEFB` (light purple) | Color of the unfilled background track |
| `dot_color` | `ColorValue` | white | Color of the drag handle |
| `shadow_color` | `ColorValue` | `#2C57C0` (blue) | Shadow color behind the progress arc |
| `inner_text_color` | `ColorValue` | matches gradient end | Color of the center text |
| `hide_shadow` | `bool` | `False` | Remove the shadow entirely |

### Labels

| Property | Type | Default | Description |
|---|---|---|---|
| `inner_text` | `str` | raw value | Text displayed in the center of the circle. Use `{value}` as a placeholder for the current value (e.g. `"{value}m"` renders as `"30m"`) |
| `top_label` | `str` | none | Small label rendered above the center text |
| `bottom_label` | `str` | none | Small label rendered below the center text |

## Events

All event callbacks receive a standard Flet event where `e.data` contains the current value as a string. Convert with `float(e.data)` or `int(float(e.data))`.

| Event | When it fires | Description |
|---|---|---|
| `on_change` | Continuously while dragging | Use for live updates (updating a label, previewing a value) |
| `on_change_start` | Once when the drag begins | Use to capture the starting value or begin a transaction |
| `on_change_end` | Once when the drag ends | Use to commit the final value |

## Examples

### Duration picker

A time picker with gradient arc and inner text showing minutes:

```python
slider = FletCircularSlider(
    min=5,
    max=120,
    value=30,
    size=220,
    progress_bar_start_color="#6C63FF",
    progress_bar_end_color="#E040FB",
    track_color="#2a2a4a",
    dot_color="#FFFFFF",
    inner_text="{value}m",
    inner_text_color="#E040FB",
    progress_bar_width=18,
    track_width=4,
    handler_size=8,
    on_change_end=lambda e: print(f"Set to {int(float(e.data))} minutes"),
)
```

### Volume knob

A compact green knob with no shadow:

```python
slider = FletCircularSlider(
    min=0,
    max=100,
    value=50,
    size=120,
    progress_bar_start_color="#4CAF50",
    progress_bar_end_color="#8BC34A",
    track_color="#333333",
    dot_color="#FFFFFF",
    inner_text="{value}%",
    hide_shadow=True,
    progress_bar_width=10,
    track_width=3,
)
```

### Full circle slider

A 360-degree slider starting from the top:

```python
slider = FletCircularSlider(
    min=0,
    max=360,
    value=90,
    size=180,
    start_angle=270,
    angle_range=360,
    progress_bar_start_color="#FF5733",
    progress_bar_end_color="#FFC300",
)
```

### With labels

Top and bottom labels around the center value:

```python
slider = FletCircularSlider(
    min=0,
    max=200,
    value=72,
    size=200,
    top_label="Heart rate",
    bottom_label="BPM",
    progress_bar_start_color="#E53935",
    progress_bar_end_color="#FF7043",
    track_color="#2a2a2a",
)
```

### Reacting to events

```python
def main(page: ft.Page):
    label = ft.Text("Drag the slider", color=ft.Colors.WHITE)

    def on_change(e):
        val = int(float(e.data))
        label.value = f"Current: {val}"
        page.update()

    def on_change_end(e):
        val = int(float(e.data))
        label.value = f"Set to: {val}"
        page.update()

    slider = FletCircularSlider(
        min=0,
        max=100,
        value=50,
        on_change=on_change,
        on_change_end=on_change_end,
    )

    page.add(slider, label)
```
