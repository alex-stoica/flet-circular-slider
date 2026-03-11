# label_formatter -- Troubleshooting Log

## Goal
Add `label_formatter` callback that pre-computes a `{value: "label"}` map in Python, sends it to Dart.

## Attempt 1 -- Naive property addition
- Added `label_formatter: Optional[Callable[[float], str]] = None` as a plain field
- **Result:** `RuntimeError: Cannot serialize method: <function format_duration at 0x...>`
- **Cause:** Flet's msgpack serialization tried to pack the callable
- **Lesson:** Callables on Flet controls must be excluded with `field(default=None, metadata={"skip": True})`

## Attempt 2 -- `field(default=None, metadata={"skip": True})` + jsonDecode
- Fixed `label_formatter` with `metadata={"skip": True}` (correct)
- On Dart side, used `control.getString("label_map")` + `jsonDecode()` to read the map
- Deleted `examples/build/` to force rebuild
- **Result:** `Unknown control: flet_circular_slider`
- **Root causes (TWO bugs):**
  1. **Dart dict access was wrong.** Flet sends Python dicts as **native msgpack maps**, NOT JSON strings. `control.getString()` calls `.toString()` on the Map, producing Dart's `{key: val}` format -- NOT valid JSON. `jsonDecode()` crashes, the Dart widget constructor never completes, and Flet reports "Unknown control". The fix is `control.get("label_map")` which returns the raw Map directly.
  2. **Deleted pre-built Flutter extension.** `examples/build/` contained the compiled Flutter binary. `flet build windows` requires Visual Studio (not installed). Must use `flet build web --no-cdn` instead.

## Key Flet internals learned
- **Serialization:** Flet uses msgpack, not JSON. Python dicts → native msgpack maps → Dart `Map<dynamic, dynamic>`
- **Excluding fields:** `field(default=None, metadata={"skip": True})` or `skip_field()` helper
- **Event handlers:** `on_*` fields with `ControlEventHandler` type are auto-detected and serialized as boolean presence flags (not the callable itself)
- **Dart access:** `control.get("prop")` for raw value, `control.getString/getInt/getDouble/getBool` for typed access. No `getMap()` -- use `get()`.
- **Build:** Custom extensions need `flet build <platform>` in the examples dir. `ft.run()` uses pre-built binaries; it does NOT auto-compile custom Dart code.
