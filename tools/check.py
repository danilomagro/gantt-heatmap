"""Regression checks for pm-workload-board.html.

Serves the repo on a local port, opens tools/check.html in headless Chrome (1920x1080),
and prints the result of every check. Exit code 1 if any check fails.

    python tools/check.py
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.isfile(c) or shutil.which(c):
            return c
    sys.exit("Chrome not found — install Google Chrome or edit CHROME_CANDIDATES")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")   # always test the file on disk
        super().end_headers()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to cp1252
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=ROOT))
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    profile = tempfile.mkdtemp(prefix="pmwb-check-")
    try:
        out = subprocess.run(
            [find_chrome(), "--headless=new", f"--user-data-dir={profile}", "--window-size=1920,1180",
             "--force-device-scale-factor=1", "--virtual-time-budget=300000", "--dump-dom",
             f"http://127.0.0.1:{port}/tools/check.html"],
            capture_output=True, text=True, encoding="utf-8", timeout=300,
        ).stdout
    finally:
        server.shutdown()
        shutil.rmtree(profile, ignore_errors=True)

    m = re.search(r'<pre id="result"[^>]*>(.*?)</pre>', out, re.S)
    if not m or 'data-done="1"' not in out:
        print("Checks did not finish. Raw output tail:\n" + out[-2000:])
        return 1
    results = json.loads(html.unescape(m.group(1)))
    failed = [r for r in results if not r["ok"]]
    for r in results:
        mark = "OK  " if r["ok"] else "FAIL"
        detail = f"  ({r['detail']})" if r.get("detail") not in (None, "") else ""
        print(f"{mark} {r['name']}{detail}")
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
