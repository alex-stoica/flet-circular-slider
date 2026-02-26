# flet-circular-slider

A circular/radial slider control for [Flet](https://flet.dev), wrapping the [sleek_circular_slider](https://pub.dev/packages/sleek_circular_slider) Flutter package.

Use it as a duration picker, volume knob, or any value selector with a circular UI.

## Installation

Add the dependency to your Flet app's `pyproject.toml`:

```toml
[project]
dependencies = [
    "flet-circular-slider @ git+https://github.com/alex-stoica/flet-circular-slider",
    "flet>=0.80.5",
]
```

Register it as a Flet dev package so the Flutter widget gets compiled into your app:

```toml
[tool.flet.dev_packages]
flet-circular-slider = {git = "https://github.com/alex-stoica/flet-circular-slider"}
```

For local development, point to a local path instead:

```toml
[tool.flet.dev_packages]
flet-circular-slider = "../path/to/flet-circular-slider"

[tool.uv.sources]
flet-circular-slider = { path = "../path/to/flet-circular-slider", editable = true }
```

## Why `flet build` is required

This is a custom Flutter extension, not a pure-Python Flet control. `flet run` uses a pre-built binary that only includes official Flet controls, so custom widgets show up as "Unknown control". You need to use `flet build` at least once to compile the Dart code into the app binary:

```bash
# Pick your platform
flet build web        # no extra tooling needed
flet build apk        # Android
flet build windows    # requires Visual Studio with C++ workload
flet build macos      # requires Xcode
```

After the first build, `flet run` will detect the compiled binary and use it for subsequent runs. You only need to rebuild when the Dart/Flutter code changes — Python-only changes work with `flet run`.

## Quick start

```python
import flet as ft
from flet_circular_slider import FletCircularSlider


def main(page: ft.Page):
    page.bgcolor = "#1a1a2e"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_change(e):
        print(f"Value: {int(float(e.data))}")

    def on_change_end(e):
        print(f"Final: {int(float(e.data))}")

    slider = FletCircularSlider(
        min=0,
        max=120,
        value=30,
        size=200,
        progress_bar_start_color="#6C63FF",
        progress_bar_end_color="#E040FB",
        track_color="#2a2a4a",
        dot_color="#FFFFFF",
        inner_text="{value}m",
        inner_text_color="#E040FB",
        on_change=on_change,
        on_change_end=on_change_end,
    )

    page.add(slider)


ft.run(main)
```

## Next steps

- [FletCircularSlider reference](FletCircularSlider.md) — all properties, events, and examples
