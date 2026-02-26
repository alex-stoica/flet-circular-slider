# Progress Log — Getting flet-circular-slider Examples Running

## 2026-02-26

### Attempt 1: Previous `flet build web` (default settings)
- **Result:** White screen with Flet splash logo — app never initializes
- **Root cause:** `index.html` has `noCdn: false`, so Pyodide loads from CDN (`cdn.jsdelivr.net`). But cross-origin isolation headers (`Cross-Origin-Embedder-Policy: require-corp`) block CDN resources that lack `Cross-Origin-Resource-Policy` headers. Pyodide worker silently fails.

### Attempt 2: Rebuild with `--no-cdn`
- **Command:** `flet build web --no-cdn --no-rich-output`
- **Goal:** Force all resources (Pyodide, CanvasKit) to load from same-origin, eliminating COEP conflicts
- **Result:** Build succeeded. `index.html` now has `noCdn: "True"`. All resources (Pyodide, CanvasKit) served from same-origin.

### Serving with custom server
- **Server:** `examples/serve_web.py` on port 8550
- **Headers verified:** COOP: same-origin, COEP: require-corp, Cache-Control: no-cache
- **MIME types verified:** .wasm → application/wasm, .js → application/javascript
- **Status:** Server returns 200 for index.html, pyodide.js, main.dart.wasm
- **Next step:** Open http://localhost:8550 in Chrome to visually verify the app renders

### Attempt 3 (if needed): CanvasKit renderer
- **Command:** `flet build web --no-cdn --web-renderer canvaskit --no-rich-output`
- **Goal:** CanvasKit doesn't require `crossOriginIsolated`, avoiding all COEP issues

### Attempt 4 (if needed): Desktop build (Windows)
- Requires VS Build Tools with VCTools workload
- **Command:** `flet build windows --no-rich-output`

### Attempt 5 (last resort): Android APK
- Android SDK at `D:\Android\Sdk`
- **Command:** `flet build apk --no-rich-output`

---

### Attempt 6: Debugging Wall — White Screen Investigation

**Problem:** Every web approach shows white screen. Can't see what error is occurring because:
1. **Service worker caching**: `flutter_service_worker.js` caches `index.html`. Even hard-refresh doesn't bypass it. Verified server serves correct files (via curl) but browser returns cached versions.
2. **Worker isolation**: Python runs in a Web Worker (`python-worker.js`). Errors inside the worker are caught and posted as strings to `console.log`, which is invisible without DevTools.

**Approaches tried and failed:**
| # | Approach | Result |
|---|----------|--------|
| 1 | `flet build web` (default CDN) | White screen — COEP headers blocked CDN |
| 2 | `flet build web --no-cdn` + custom server | White screen — resources load, app doesn't init |
| 3 | Changed `webRenderer: "canvaskit"` | White screen — same |
| 4 | `flet serve -p 8550` | White screen — same |
| 5 | Added error overlay to index.html | No visible change — service worker served cached version |
| 6 | `flet run -w main.py` | Works but "Unknown control: flet_circular_slider" |

**Solution: Phase 1 — Diagnostic HTML files**

Created two diagnostic pages that bypass both caching and worker isolation:

1. **`clear.html`** — Unregisters all service workers, deletes all Cache Storage entries, then provides links to boot-test.html and index.html.

2. **`boot-test.html`** — Runs the **entire** Python boot sequence on the main thread (not in a Worker), displaying each step with PASS/FAIL:
   - Step 1: Load `/pyodide/pyodide.js` script tag
   - Step 2: Call `loadPyodide({indexURL: "/pyodide/"})`
   - Step 3: Register `flet_js` mock module
   - Step 4: `loadPackage("micropip")`
   - Step 5: Fetch & unpack `app.zip`
   - Step 6: Add `__pypackages__` to `sys.path`
   - Step 7: `import flet`
   - Step 8: `from flet_circular_slider import FletCircularSlider`
   - Step 9: `runpy.run_module("main", run_name="__main__")`
   - Step 10: Check if `flet_js.start_connection` was set

**Test sequence:**
1. Start server: `python examples/serve_web.py` (port 8550)
2. Visit `http://localhost:8550/clear.html` → clears caches
3. Visit `http://localhost:8550/boot-test.html` → reveals exact failure point
4. Report which step fails and the error message

**Diagnostic results:**
- `boot-test.html`: ALL 10 PYTHON STEPS PASSED (3.1s)
- `flutter-test.html`: ALL 8 FLUTTER STEPS PASSED (4.1s)
- Both halves work individually — the problem was the **server**, not the app

### ROOT CAUSE FOUND: Single-threaded HTTP server

**Problem:** Python's `http.server.HTTPServer` is single-threaded. Flutter's loader fetches multiple large files concurrently (`canvaskit.wasm` ~5.5MB, `main.dart.js` ~7.9MB, `pyodide.asm.wasm`, etc.). The second request blocks until the first completes, causing a deadlock where the browser times out waiting.

**Fix:** Changed `serve_web.py` to use `socketserver.ThreadingMixIn` for concurrent request handling:
```python
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
```

**Result:** App loads in ~4 seconds. All three examples (Basic, Styled Timer, RGB Mixer) work correctly with the circular slider control.

**Cleanup:** Removed the debug error overlay from `index.html` (was intercepting console.log/warn/error and displaying them in a DOM overlay — no longer needed).

### Reworked Examples: Basic & Advanced

**Changes:**
- **Removed** RGB Mixer example (`rgb_mixer.py`, `rgb_mixer.html`)
- **Removed** Styled Timer example (`styled_timer.py`, `styled_timer.html`)
- **Created** Advanced example (`advanced.py`, `advanced.html`) — showcases every customization: cyan-to-green gradient, custom geometry (start_angle=270, angle_range=300), sizing (progress_bar_width=20, handler_size=10), labels (top/bottom/inner text), hide_shadow, all 3 events (on_change, on_change_start, on_change_end)
- **Updated** Basic example (`basic.py`) — minimal usage with visible value display, only sets min/max/value/size/on_change
- **Updated** Launcher (`main.py`) — 2 buttons: Basic and Advanced
- **Rebuilt** `app.zip` with updated Python files

**URLs:**
- `http://localhost:8551/` — launcher with Basic + Advanced buttons
- `http://localhost:8551/basic.html` — standalone basic (default purple gradient, simple value display)
- `http://localhost:8551/advanced.html` — standalone advanced (cyan-green neon, labels, custom geometry, event feedback)
