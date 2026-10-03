"""Regression checks for pm-workload-board.html.

Serves the repo on a local port, opens tools/check.html in headless Chrome (1920x1080, real time),
and collects the results the page POSTs back. Prints every check; exit code 1 if any fails.

    python tools/check.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT_S = 180
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]

state = {"results": [], "done": threading.Event()}


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.isfile(c) or shutil.which(c):
            return c
    sys.exit("Chrome not found — install Google Chrome or edit CHROME_CANDIDATES")


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")   # always test the file on disk
        super().end_headers()

    def do_POST(self):
        # check.html posts {results, done} after every check, so a hang still leaves partial results
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        state["results"] = body.get("results", [])
        if body.get("done"):
            state["done"].set()
        self.send_response(204)
        self.end_headers()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to cp1252

    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Handler, directory=ROOT))
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    profile = tempfile.mkdtemp(prefix="pmwb-check-")
    chrome = subprocess.Popen(
        [find_chrome(), "--headless=new", f"--user-data-dir={profile}", "--window-size=1920,1180",
         "--force-device-scale-factor=1", "--no-first-run", "--no-default-browser-check",
         f"http://127.0.0.1:{port}/tools/check.html"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    finished = state["done"].wait(TIMEOUT_S)
    chrome.kill()
    chrome.wait()
    server.shutdown()
    shutil.rmtree(profile, ignore_errors=True)

    results = list(state["results"])
    if not finished:
        results.append({"name": f"harness finished within {TIMEOUT_S}s (it hung right after the last check above)", "ok": False})
    failed = [r for r in results if not r["ok"]]
    for r in results:
        mark = "OK  " if r["ok"] else "FAIL"
        detail = f"  ({r['detail']})" if r.get("detail") not in (None, "") else ""
        print(f"{mark} {r['name']}{detail}")
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed or not results else 0


if __name__ == "__main__":
    sys.exit(main())
