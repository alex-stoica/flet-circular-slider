# Errors log

## 2026-03-08: build.py --skip-flet doesn't update Dart code

**What went wrong:** after changing Dart event format from `value.toString()` to `_canonicalKey(value)`,
ran `build.py --skip-flet` which only patches Python files in app.zip. The Dart code is compiled into the
Flutter binary during `flet build apk` (step 1), so skipping it means the old Dart code runs with new Python
expectations. Result: `int(e.data)` fails on `"50.0"` strings the old Dart still sends.

**Fix:** always run full `python build.py` (no `--skip-flet`) when Dart source files change.

## 2026-03-08: deleting build/flutter or build/site-packages breaks flet build

**What went wrong:** tried to do a clean rebuild by deleting `build/flutter` and `build/site-packages`.
`flet build apk` then failed with `NotADirectoryError: [WinError 267]` because it expects certain paths
inside `build/flutter/` to exist (Dart SDK references, project structure). Partial deletion leaves the
build in an unrecoverable state for `flet build`.

**Fix:** if you need a clean rebuild, delete the entire `build/` directory (`rm -rf build`), not just
subdirectories. `flet build apk` can recreate everything from scratch, but not recover from a
half-deleted state.

## 2026-03-08: two on_change handlers fighting over same status text

**What went wrong:** in the controller demo section, the big slider had its own `on_change` handler
writing "Big: X" to `ctrl_status`, while the controller's handler also wrote "Controller -> X" to the
same `ctrl_status`. When dragging the controller, it sets `big_slider.value` and calls `.update()`,
which triggers the big slider's `on_change` in turn. Both handlers fire in rapid succession, causing
visible text flickering.

**Why it seemed right:** each slider having its own on_change handler seems natural. The issue is that
programmatic `.update()` also triggers on_change events on the Dart side, creating a feedback loop.

**Fix:** only one handler should write to a shared status text. Removed `on_change` from the big slider
since the controller's handler already reports the value.
