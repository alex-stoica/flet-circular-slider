# Testing Notes — Running Examples

## What was done

### Package changes
- Added `src/flutter/__init__.py` and `src/flutter/flet_circular_slider/__init__.py` (empty files) so Poetry includes the Dart source as a proper Python package in the wheel
- `pyproject.toml` uses `packages = [{ include = "flet_circular_slider", from = "src" }, { include = "flutter", from = "src" }]`
- Verified with `poetry build` — the wheel contains `flutter/flet_circular_slider/pubspec.yaml` at the correct path
- `poetry check` passes clean, `poetry install` works

### Examples project
- Created `examples/pyproject.toml` with:
  ```toml
  [tool.flet.dev_packages]
  flet-circular-slider = ".."
  ```
  (Must be a plain string path, NOT a dict like `{ path = ".." }` — flet-cli 0.81.0 passes value directly to `Path()`)

### flet build web
- `flet build web` from `examples/` succeeds
- The built `pubspec.yaml` at `examples/build/flutter/pubspec.yaml` DOES include `flet_circular_slider` as a path dependency — the extension IS compiled into the Flutter output
- `app.zip` at `examples/build/web/assets/app/app.zip` contains `main.py`, `__pypackages__/flet_circular_slider/` etc.

### What failed at runtime

#### 1. `flet serve build/web` — white screen with Flet logo, never loads
- Tried multiple ports (8550, 8551, 8552)
- Also tried `python -m http.server` — same result (plus MIME type issues with .wasm)
- The Flet splash shows but the Python/Pyodide app never initializes
- Could NOT see browser console errors (no way from CLI)
- **Root cause unknown** — could be Pyodide loading issue, CORS, or something else in the web pipeline

#### 2. `flet run -w main.py` — works for Python but no custom control
- This starts a dev web server that runs Python server-side (NOT Pyodide)
- Custom controls show "Unknown control: flet_circular_slider" because `flet run` uses pre-built Flutter binary without the extension
- BUT this is useful for catching Python errors before doing `flet build`

### Flet 0.81.0 API gotchas discovered
- `ft.Tab` uses `label=` not `text=`, and has NO `content` parameter
- `ft.Tabs` requires `content` (a Control) and `length` (int) — uses `TabBar` + `TabBarView` pattern internally
- `ft.ElevatedButton` is deprecated → use `ft.Button(content=ft.Text("..."), ...)`
- `ft.Button` uses `content=` not `text=`
- `ft.Dropdown` uses `on_select=` not `on_change=`, and `Option(key=..., text=...)`

### Current state of main.py
- Python code runs without errors under `flet run -w`
- Uses `ft.Button` with a dropdown-like UI to switch between 3 examples
- All 3 standalone example files (`basic.py`, `styled_timer.py`, `rgb_mixer.py`) parse as valid Python

## What to try next

### Option A: Desktop build (recommended if Visual Studio gets installed)
```bash
# Install Visual Studio with "Desktop development with C++" workload first
cd examples
flet build windows
# Then run the built .exe directly
```

### Option B: Debug the web build
- Open `http://localhost:PORT` in Chrome, press F12, check Console tab for errors
- The Pyodide worker logs to console — errors during Python init will appear there
- Check if `assets/app/app.zip` loads (Network tab)
- Try with `--no-web-animation` flag if available

### Option C: Android build
```bash
cd examples
flet build apk
# Flutter doctor shows Android SDK is available
```

### Option D: Try flet run in desktop mode (if extension can be pre-built)
```bash
# From examples dir, after flet build windows:
flet run main.py
# Desktop flet run should pick up the compiled binary
```

## Key file locations
- Main package: `src/flet_circular_slider/`
- Flutter extension source: `src/flutter/flet_circular_slider/`
- Examples launcher: `examples/main.py`
- Examples project config: `examples/pyproject.toml`
- Build output: `examples/build/web/`

## Environment
- Flet 0.81.0, Flutter 3.41.2
- Windows 11 Pro, Python 3.12
- NO Visual Studio (needed for Windows desktop builds)
- Android SDK 35.0.0 available
- Chrome available
