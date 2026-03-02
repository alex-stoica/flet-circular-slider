# Performance fixes — learnings

## Flet control lifecycle

- `before_update()` runs during patch serialization on **every** `.update()` call, not just on
  property changes. Any expensive work here (dict construction, formatting) adds latency to every
  update cycle, even when unrelated properties changed.
- Non-field instance attributes on dataclass controls (e.g. `self._label_cache_key`) are safe for
  caching — they're invisible to flet's serialization and won't be sent over the wire.

## triggerEvent cost

- `triggerEvent` sends a websocket message to the Python side. Treat it like a network call.
- During drag, `SleekCircularSlider` fires `onChange` per animation frame (~60/sec). With 20
  divisions, the snapped value only changes ~20 times total. Deduplicating by canonical key cuts
  event volume by ~60-90%.

## Dart widget.control mutation

- `widget.control` is mutated in-place by flet when properties change. `didUpdateWidget` won't fire
  for property-only changes (same widget identity). This means you can't rely on widget lifecycle
  to detect property changes — you must re-read from `widget.control` in `build()`.

## SleekCircularSlider per-frame callbacks

- `innerWidget`, `modifier`, and `onChange` are all called per-frame during drag. Any work inside
  these closures (color parsing, map lookups, control property reads) runs 60 times per second.
- Hoist invariant reads (colors, text, throttle config) into `build()` and capture in closures.
- The local `snapValue()` function pattern (defined in `build()`, captures pre-read `step`/`min`)
  avoids re-reading control properties on every frame while staying simple.

## Key format agreement

- Python generates `label_map` keys, Dart looks them up. Both sides **must** produce identical
  strings for the same float value.
- `round()` in Python returns int, `.round()` in Dart returns int — but both silently break for
  fractional ranges (e.g. min=0, max=1, divisions=4 produces values 0.25, 0.5, 0.75 which all
  round to 0 or 1).
- Solution: `_canonical_key` / `_canonicalKey` — format to 10 decimal places, strip trailing zeros.
  Both sides use IEEE 754 doubles and the same `min + i * step` formula, so the raw values match
  exactly and the string formatting produces identical keys.

## Why the wrong path seemed right

- Using `round()` for keys worked perfectly for the original use case (duration picker with integer
  minutes). The bug only surfaces with fractional ranges, which no existing example exercises. The
  implicit assumption was "slider values are integers" — reasonable given the examples, but wrong
  as a general invariant.
