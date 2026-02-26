# Publishing flet-circular-slider

## Current state

- Python package: `flet-circular-slider` v0.1.0
- Build system: Poetry (`poetry-core` backend)
- Dart/Flutter extension: `flet_circular_slider` wrapping `sleek_circular_slider`
- License: MIT (file exists)
- README: exists, needs minor update (still references old examples)
- GitHub repo URL in pyproject.toml: `https://github.com/alex-stoica/flet-circular-slider` (not yet created)

## Steps

### 1. Create the GitHub repo

```bash
cd C:\Users\alexs\Desktop\flet-circular-slider
git init
git add -A
git commit -m "Initial commit"
gh repo create alex-stoica/flet-circular-slider --public --source . --push
```

Before committing, make sure `.gitignore` excludes:
- `examples/build/` (large web build artifacts)
- `__pycache__/`
- `.venv/`
- `*.egg-info/`

### 2. Update README.md

- Replace the Examples section — `styled_timer.py` and `rgb_mixer.py` no longer exist
- Should reference `basic.py` and `advanced.py` instead

### 3. Publish the Python package to PyPI

#### One-time setup
1. Create a PyPI account at https://pypi.org/account/register/
2. Go to Account Settings > API tokens > Add API token (scope: entire account for first upload)
3. Install build tools:
   ```bash
   pip install build twine
   ```

#### Build and upload
```bash
cd C:\Users\alexs\Desktop\flet-circular-slider
python -m build          # creates dist/flet_circular_slider-0.1.0.tar.gz and .whl
twine check dist/*       # verify package metadata
twine upload dist/*      # prompts for API token
```

After first upload, create a project-scoped token and save it for future releases.

#### What gets published
The `[tool.poetry] packages` config controls what's included:
- `src/flet_circular_slider/` — the Python control class
- `src/flutter/` — the Dart extension source

This is critical — users need the Dart source so `flet build` can compile it.

### 4. Register as a Flet extension package

Flet has a convention for extension packages. Users of your package will need two things in their project:

**pyproject.toml (their project):**
```toml
[project]
dependencies = ["flet-circular-slider>=0.1.0"]

[tool.flet.dev_packages]
flet-circular-slider = ">=0.1.0"
```

The `[tool.flet.dev_packages]` entry tells `flet build` to compile your Dart extension. Without it, the Python class loads but the Flutter widget is missing ("Unknown control").

Make sure your README explains this clearly — it's the #1 thing people will get wrong.

### 5. Verify the published package works

In a fresh directory:
```bash
mkdir test-project && cd test-project
pip install flet flet-circular-slider
```

Create a minimal `main.py`:
```python
import flet as ft
from flet_circular_slider import FletCircularSlider

def main(page: ft.Page):
    page.add(FletCircularSlider(min=0, max=100, value=50, size=200))

ft.run(main)
```

Then:
```bash
flet build web
```

If it builds and renders the slider, the package is correctly published.

### 6. Optional: publish the Dart package to pub.dev

Currently `pubspec.yaml` has `publish_to: none`. Publishing to pub.dev is **not required** — Flet compiles extensions from source shipped inside the PyPI package. But if you want it discoverable on pub.dev:

1. Remove `publish_to: none` from `pubspec.yaml`
2. Add `homepage` and `repository` fields
3. Run `dart pub publish` from `src/flutter/flet_circular_slider/`

This is optional and most Flet extension authors skip it.

## Version bumps for future releases

Update version in **two** places:
1. `pyproject.toml` → `version = "X.Y.Z"`
2. `src/flutter/flet_circular_slider/pubspec.yaml` → `version: X.Y.Z`

Then rebuild and upload:
```bash
python -m build
twine upload dist/*
```

## Checklist

- [ ] `.gitignore` covers build artifacts
- [ ] README references correct examples (basic.py, advanced.py)
- [ ] GitHub repo created and pushed
- [ ] PyPI account + API token
- [ ] `python -m build` succeeds
- [ ] `twine upload` succeeds
- [ ] Fresh install + `flet build web` works end-to-end
