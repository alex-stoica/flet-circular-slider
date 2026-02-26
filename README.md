# flet-circular-slider

A circular/radial slider control for [Flet](https://flet.dev), wrapping the [sleek_circular_slider](https://pub.dev/packages/sleek_circular_slider) Flutter package.

## Install

```bash
pip install flet-circular-slider
```

Then register it as a Flet extension in your project's `pyproject.toml` so the Flutter widget gets compiled:

```toml
[project]
dependencies = ["flet-circular-slider>=0.1.0"]

[tool.flet.dev_packages]
flet-circular-slider = ">=0.1.0"
```

Then run `flet build` (see [Building](#building) below). `flet run` alone won't compile extensions — you'll get "Unknown control" without a build step.

## Quick Start

```python
import flet as ft
from flet_circular_slider import FletCircularSlider

def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"

    slider = FletCircularSlider(
        min=0, max=100, value=25, size=200,
        on_change=lambda e: print(int(float(e.data))),
    )
    page.add(slider)

ft.run(main)
```

## Examples

- **[basic.py](examples/basic.py)** — Minimal slider with `on_change` event
- **[advanced.py](examples/advanced.py)** — Custom colors, geometry, labels, sizing, and all three events

## Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `min` | `float` | `0` | Minimum value |
| `max` | `float` | `100` | Maximum value |
| `value` | `float` | `50` | Initial value |
| `size` | `float` | `150` | Diameter in pixels |
| `start_angle` | `float` | `150` | Arc start angle (degrees) |
| `angle_range` | `float` | `240` | Arc total range (degrees) |
| `counter_clockwise` | `bool` | `False` | Reverse drag direction |
| `animation_enabled` | `bool` | `True` | Animate to initial value |
| | | | |
| `progress_bar_width` | `float` | `size/10` | Progress arc width |
| `track_width` | `float` | `bar/4` | Background track width |
| `handler_size` | `float` | `bar/5` | Drag handle size |
| | | | |
| `progress_bar_start_color` | `ColorValue` | purple | Gradient start color |
| `progress_bar_end_color` | `ColorValue` | pink | Gradient end color |
| `track_color` | `ColorValue` | light purple | Track color |
| `dot_color` | `ColorValue` | white | Handle dot color |
| `shadow_color` | `ColorValue` | blue | Shadow color |
| `hide_shadow` | `bool` | `False` | Remove the shadow |
| `inner_text_color` | `ColorValue` | gradient end | Center text color |
| | | | |
| `inner_text` | `str` | raw value | Center text (`{value}` placeholder) |
| `top_label` | `str` | none | Label above center |
| `bottom_label` | `str` | none | Label below center |

## Events

| Event | `e.data` | Description |
|---|---|---|
| `on_change` | current value | Fires continuously while dragging |
| `on_change_start` | value at drag start | Fires once when drag begins |
| `on_change_end` | value at drag end | Fires once when drag ends |

## Building

Custom Flet extensions require `flet build` to compile Dart/Flutter code. `flet run` alone shows "Unknown control" because it uses a pre-built binary.

```bash
flet build web       # no extra tooling needed
flet build windows   # requires Visual Studio C++ workload
flet build apk       # Android
flet build macos     # macOS
```

After building, `flet run` works for Python-only changes. Rebuild when you change Dart code.

## License

MIT
