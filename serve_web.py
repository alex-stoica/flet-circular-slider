"""
Custom HTTP server for serving the Flet web build.

Provides:
- Correct MIME types for .wasm, .mjs, .js files
- COOP/COEP headers for cross-origin isolation (needed for SharedArrayBuffer / Pyodide)
- Cache-Control: no-cache to prevent stale service worker cache
- Toggle to disable cross-origin isolation for debugging

Usage:
    python serve_web.py              # default: port 8550, cross-origin isolation ON
    python serve_web.py --port 9000  # custom port
    python serve_web.py --no-coi     # disable cross-origin isolation headers
"""

import argparse
import http.server
import os
import socketserver
import sys

# Serve from build/web/ relative to this script
SERVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "web")

# Extra MIME types Flet/Flutter needs
EXTRA_MIME = {
    ".wasm": "application/wasm",
    ".mjs": "application/javascript",
    ".js": "application/javascript",
    ".json": "application/json",
    ".zip": "application/zip",
}


class FletHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with COOP/COEP headers and correct MIME types."""

    enable_coi = True  # toggled by --no-coi flag

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def guess_type(self, path):
        _, ext = os.path.splitext(path)
        if ext in EXTRA_MIME:
            return EXTRA_MIME[ext]
        return super().guess_type(path)

    def end_headers(self):
        # Cross-origin isolation headers (required for SharedArrayBuffer / Pyodide)
        if self.enable_coi:
            self.send_header("Cross-Origin-Opener-Policy", "same-origin")
            self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        # Prevent stale caching
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description="Serve Flet web build")
    parser.add_argument("--port", type=int, default=8550, help="Port to serve on (default: 8550)")
    parser.add_argument("--no-coi", action="store_true", help="Disable cross-origin isolation headers")
    args = parser.parse_args()

    if not os.path.isdir(SERVE_DIR):
        print(f"ERROR: Build directory not found: {SERVE_DIR}")
        print("Run 'flet build web --no-cdn' first.")
        sys.exit(1)

    FletHandler.enable_coi = not args.no_coi

    class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    server = ThreadedHTTPServer(("0.0.0.0", args.port), FletHandler)
    coi_status = "OFF" if args.no_coi else "ON"
    print(f"Serving {SERVE_DIR}")
    print(f"  -> http://localhost:{args.port}")
    print(f"  -> Cross-origin isolation: {coi_status}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
