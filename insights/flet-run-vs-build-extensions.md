# `flet run` does not support custom Flutter extensions

## The problem

Running a Flet app with custom Flutter extensions (like `flet-circular-slider`) via `flet run` results in:
```
Unknown control: flet_circular_slider
```

The Python side works fine (import succeeds, `@ft.control` decorator registers), but the Dart/Flutter widget never renders.

## Root cause

`flet run` and `flet build` handle extensions completely differently:

### `flet run` (development server)
- Only reads `tool.flet.app.path` from `pyproject.toml`
- **Ignores `[tool.flet.dev_packages]` entirely**
- Launches the **pre-built** `flet.exe`/`flet-desktop` binary
- That binary contains only official Flet controls
- No Flutter compilation happens — no mechanism to load custom Dart code

### `flet build` (production build)
- Reads `[tool.flet.dev_packages]` from `pyproject.toml`
- Resolves local paths, installs the extension package
- Extracts Flutter code from installed packages into `build/flutter-packages/`
- Registers extensions in the Flutter project's `pubspec.yaml`
- Runs `flutter build` which compiles custom Dart code into the app binary

## Workaround: `flet run` after `flet build`

After a successful `flet build windows`, the compiled binary lives in `build/windows/`. Subsequent `flet run` invocations detect this compiled binary and use it instead of the pre-built `flet.exe`. So the workflow is:

1. `flet build windows --yes` (first time, compiles everything)
2. `flet run` (uses the compiled binary with extensions included)

**Note:** If you change Flutter/Dart code in the extension, you must `flet build` again.

## Build gotchas on Windows

### Unicode error with Rich progress display
`flet build` uses Rich for progress output. On Windows terminals with cp1252 encoding, Rich fails with:
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u25cf'
```
Fix: set `PYTHONIOENCODING=utf-8` before running `flet build`.

### Flutter SDK auto-install prompt
If the required Flutter SDK version isn't installed, `flet build` prompts interactively. Use `--yes` flag to auto-confirm in scripts/CI:
```bash
PYTHONIOENCODING=utf-8 flet build windows --yes
```

### Visual Studio required for Windows desktop builds
`flet build windows` requires Visual Studio with "Desktop development with C++" workload. Without it, build for web instead:
```bash
PYTHONIOENCODING=utf-8 flet build web --yes
```

### Dart dependency constraint: use `>=` not `^`
The extension's `pubspec.yaml` must use a wide version range for the `flet` dependency. Caret syntax `^0.80.5` means `>=0.80.5 <0.81.0`, which breaks when flet-cli is 0.81.x. Use:
```yaml
flet: ">=0.80.5 <2.0.0"
```

### Flet 0.81.0 breaking change: `sendEvent` → `triggerEvent`
In the Dart extension code, `control.sendEvent(name, data)` was renamed to `control.triggerEvent(name, data)`. This is a compile-time error, not a runtime one — the build itself fails.

## Correct development workflow for extension authors

```bash
cd examples/flet_circular_slider_example

# Build for web (no Visual Studio needed)
PYTHONIOENCODING=utf-8 flet build web --yes

# Serve the built web app
python -m http.server 8550 --directory build/web
# Then open http://localhost:8550

# Or build for Windows (requires Visual Studio with C++ workload)
PYTHONIOENCODING=utf-8 flet build windows --yes
./build/windows/flet-circular-slider-example.exe
```

After changing **Python code only**, `flet run` is sufficient.
After changing **Dart/Flutter code**, re-run `flet build`.
