"""
Frosty API Key Rotator
======================
A lightweight reverse proxy that round-robins Google API keys
to avoid rate limits. Sits between Open Code and Google's API.

Usage:
  1. Add your API keys to keys.txt (one per line)
  2. Run: python rotator.py
  3. Configure Open Code's Google provider baseURL to http://127.0.0.1:5555
"""

import asyncio
import html
import itertools
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from string import Template

# --- Auto-install dependencies ---
def ensure_dependencies():
    req_file = Path(__file__).parent / "requirements.txt"
    try:
        import aiohttp  # noqa: F401
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file), "--quiet"]
        )
        print("Dependencies installed.\n")

ensure_dependencies()

import aiohttp  # noqa: E402
from aiohttp import web  # noqa: E402

# --- Config ---
LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 5555
GOOGLE_BASE = "https://generativelanguage.googleapis.com/v1beta"
MAX_RETRIES = 3
KEYS_FILE = Path(__file__).parent / "keys.txt"
REQUESTS_PER_KEY = 3

# --- Key Management ---
class KeyPool:
    def __init__(self, keys_file: Path):
        self.keys_file = keys_file
        self.keys: list[str] = []
        self.stats: dict[str, dict] = {}
        self._current_index: int = 0
        self._current_count: int = 0
        self.start_time = datetime.now()
        self.total_requests = 0
        self.total_retries = 0
        self.request_log: list[dict] = []  # last 50 requests
        self.load_keys()

    def load_keys(self):
        if not self.keys_file.exists():
            print(f"  ERROR: {self.keys_file} not found.")
            sys.exit(1)

        self.keys = [
            line.strip()
            for line in self.keys_file.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        if not self.keys:
            print(f"  ERROR: No API keys found in {self.keys_file}")
            sys.exit(1)

        for key in self.keys:
            short = f"...{key[-6:]}"
            self.stats[key] = {
                "short": short,
                "requests": 0,
                "errors": 0,
                "rate_limits": 0,
                "last_used": None,
                "active": False,
            }
        # Mark first key as active
        self.stats[self.keys[0]]["active"] = True

    def next_key(self) -> str:
        if self._current_count >= REQUESTS_PER_KEY:
            self.stats[self.keys[self._current_index]]["active"] = False
            self._current_index = (self._current_index + 1) % len(self.keys)
            self._current_count = 0
            self.stats[self.keys[self._current_index]]["active"] = True
            short = self.stats[self.keys[self._current_index]]["short"]
            print(f"  \033[36m↻ ROTATE\033[0m  Switching to key {short}")

        key = self.keys[self._current_index]
        self._current_count += 1
        self.stats[key]["requests"] += 1
        self.stats[key]["last_used"] = datetime.now().strftime("%H:%M:%S")
        self.total_requests += 1
        return key

    def force_rotate(self):
        self.stats[self.keys[self._current_index]]["active"] = False
        self._current_index = (self._current_index + 1) % len(self.keys)
        self._current_count = 0
        self.stats[self.keys[self._current_index]]["active"] = True
        self.total_retries += 1
        short = self.stats[self.keys[self._current_index]]["short"]
        print(f"  \033[33m⚡ FORCE ROTATE\033[0m  429 hit → key {short}")

    def record_error(self, key: str, status: int):
        self.stats[key]["errors"] += 1
        if status == 429:
            self.stats[key]["rate_limits"] += 1

    def log_request(self, method: str, path: str, status: int, key_short: str):
        self.request_log.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "method": method,
            "path": path[:80],
            "status": status,
            "key": key_short,
        })
        if len(self.request_log) > 50:
            self.request_log.pop(0)

    def get_uptime(self) -> str:
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"


pool: KeyPool = None  # type: ignore

# --- Favicon ---
ICON_PATH = Path(__file__).parent.parent / "opencode-profile-pic" / "frosty_icon.png"

async def favicon_handler(request: web.Request) -> web.Response:
    if ICON_PATH.exists():
        return web.Response(body=ICON_PATH.read_bytes(), content_type="image/png")
    return web.Response(status=404)

# --- Proxy Handler ---
async def proxy_handler(request: web.Request) -> web.StreamResponse:
    path = request.match_info.get("path", "")

    # Skip noise: favicon, well-known, devtools probes
    if path in ("favicon.ico",) or path.startswith(".well-known/"):
        return web.Response(status=404)

    body = await request.read()

    forward_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "x-goog-api-key", "content-length", "transfer-encoding")
    }

    params = {k: v for k, v in request.query.items() if k.lower() != "key"}

    for attempt in range(MAX_RETRIES):
        if attempt == 0:
            key = pool.next_key()
        else:
            pool.force_rotate()
            key = pool.keys[pool._current_index]
            pool.stats[key]["requests"] += 1
            pool.stats[key]["last_used"] = datetime.now().strftime("%H:%M:%S")
            pool.total_requests += 1

        short = pool.stats[key]["short"]
        params["key"] = key
        target_url = f"{GOOGLE_BASE}/{path}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=request.method,
                    url=target_url,
                    headers=forward_headers,
                    params=params,
                    data=body if body else None,
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as upstream:

                    # Retry on 401 (bad key), 429 (rate limit), or 500+ (server error)
                    if upstream.status in (401, 403, 429) or upstream.status >= 500:
                        pool.record_error(key, upstream.status)
                        error_body = await upstream.text()
                        label = "rate limited" if upstream.status == 429 else "server error"
                        print(f"  \033[31m✗ {upstream.status}\033[0m  Key {short} {label} (attempt {attempt + 1}/{MAX_RETRIES})")
                        pool.log_request(request.method, path, upstream.status, short)
                        if attempt < MAX_RETRIES - 1:
                            continue
                        return web.Response(status=upstream.status, text=error_body, content_type="application/json")

                    resp_headers = {
                        k: v for k, v in upstream.headers.items()
                        if k.lower() not in ("content-encoding", "transfer-encoding", "content-length")
                    }

                    response = web.StreamResponse(status=upstream.status, headers=resp_headers)
                    await response.prepare(request)

                    async for chunk in upstream.content.iter_any():
                        await response.write(chunk)

                    await response.write_eof()

                    status_color = "\033[32m" if upstream.status == 200 else "\033[33m"
                    print(f"  {status_color}✓ {upstream.status}\033[0m  {request.method} /{path[:50]}  →  {short}")
                    pool.log_request(request.method, path, upstream.status, short)
                    return response

        except asyncio.TimeoutError:
            pool.record_error(key, 0)
            print(f"  \033[31m✗ TIMEOUT\033[0m  Key {short} (attempt {attempt + 1}/{MAX_RETRIES})")
            pool.log_request(request.method, path, 504, short)
            if attempt < MAX_RETRIES - 1:
                continue
            return web.Response(status=504, text="Gateway Timeout")

        except Exception as e:
            pool.record_error(key, 0)
            print(f"  \033[31m✗ ERROR\033[0m  Key {short}: {e}")
            pool.log_request(request.method, path, 502, short)
            if attempt < MAX_RETRIES - 1:
                continue
            return web.Response(status=502, text=f"Proxy Error: {e}")

    return web.Response(status=502, text="All retry attempts failed")


# --- Dashboard ---
def build_dashboard_html(uptime, host, port, rpk, num_keys, max_retries,
                         total_requests, total_success, total_rate_limits,
                         total_errors, key_cards, log_rows):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Frosty Key Rotator</title>
<link rel="icon" type="image/png" href="/favicon.ico">
<meta http-equiv="refresh" content="5">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'Segoe UI',-apple-system,sans-serif;background:#0a0e17;color:#e0e6f0;min-height:100vh;padding:24px}}
  .header{{display:flex;align-items:center;gap:16px;margin-bottom:32px;padding-bottom:20px;border-bottom:1px solid #1e2a3a}}
  .header h1{{font-size:22px;font-weight:600;color:#00bfff}}
  .header .badge{{background:#0d3320;color:#34d399;font-size:11px;font-weight:600;padding:4px 10px;border-radius:20px;letter-spacing:.5px}}
  .header .uptime{{margin-left:auto;font-size:13px;color:#6b7a8d}}
  .stats-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px}}
  .stat-card{{background:#111827;border:1px solid #1e2a3a;border-radius:12px;padding:20px}}
  .stat-card .label{{font-size:12px;color:#6b7a8d;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px}}
  .stat-card .value{{font-size:28px;font-weight:700}}
  .stat-card .value.blue{{color:#00bfff}}
  .stat-card .value.green{{color:#34d399}}
  .stat-card .value.yellow{{color:#fbbf24}}
  .stat-card .value.red{{color:#f87171}}
  .section-title{{font-size:15px;font-weight:600;color:#94a3b8;margin-bottom:16px;text-transform:uppercase;letter-spacing:.8px}}
  .keys-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-bottom:32px}}
  .key-card{{background:#111827;border:1px solid #1e2a3a;border-radius:10px;padding:16px;transition:border-color .2s}}
  .key-card.active{{border-color:#00bfff;box-shadow:0 0 0 1px rgba(0,191,255,.15)}}
  .key-header{{display:flex;align-items:center;gap:8px;margin-bottom:12px}}
  .key-dot{{width:8px;height:8px;border-radius:50%;background:#374151}}
  .key-card.active .key-dot{{background:#00bfff;box-shadow:0 0 6px rgba(0,191,255,.5)}}
  .key-name{{font-family:Consolas,Monaco,monospace;font-size:13px;color:#cbd5e1}}
  .key-stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
  .key-stat{{text-align:center}}
  .key-stat .num{{font-size:18px;font-weight:700}}
  .key-stat .lbl{{font-size:10px;color:#6b7a8d;text-transform:uppercase}}
  .key-stat .num.ok{{color:#34d399}}
  .key-stat .num.warn{{color:#fbbf24}}
  .key-stat .num.err{{color:#f87171}}
  .log-table{{width:100%;border-collapse:collapse;font-size:13px}}
  .log-table th{{text-align:left;padding:10px 12px;color:#6b7a8d;font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #1e2a3a}}
  .log-table td{{padding:8px 12px;border-bottom:1px solid #111827;font-family:Consolas,Monaco,monospace}}
  .log-table tr:hover{{background:#111827}}
  .status-badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600}}
  .status-badge.s2xx{{background:#0d3320;color:#34d399}}
  .status-badge.s4xx{{background:#3b1313;color:#f87171}}
  .status-badge.s5xx{{background:#3b2813;color:#fbbf24}}
  .config-bar{{background:#111827;border:1px solid #1e2a3a;border-radius:8px;padding:12px 16px;margin-bottom:32px;font-size:13px;color:#6b7a8d;display:flex;gap:32px;flex-wrap:wrap}}
  .config-bar span{{color:#94a3b8}}
  .config-bar code{{color:#00bfff;background:#0a1628;padding:2px 6px;border-radius:4px;font-size:12px}}
</style>
</head>
<body>

<div class="header">
  <h1>Frosty Key Rotator</h1>
  <div class="badge">RUNNING</div>
  <div class="uptime">Uptime: {uptime}</div>
</div>

<div class="config-bar">
  <div><span>Proxy:</span> <code>http://{host}:{port}</code></div>
  <div><span>Rotate:</span> <code>every {rpk} requests</code></div>
  <div><span>Keys:</span> <code>{num_keys} loaded</code></div>
  <div><span>Retries:</span> <code>{max_retries} on 429/5xx</code></div>
</div>

<div class="stats-row">
  <div class="stat-card">
    <div class="label">Total Requests</div>
    <div class="value blue">{total_requests}</div>
  </div>
  <div class="stat-card">
    <div class="label">Successful</div>
    <div class="value green">{total_success}</div>
  </div>
  <div class="stat-card">
    <div class="label">Rate Limited</div>
    <div class="value yellow">{total_rate_limits}</div>
  </div>
  <div class="stat-card">
    <div class="label">Errors</div>
    <div class="value red">{total_errors}</div>
  </div>
</div>

<div class="section-title">API Keys</div>
<div class="keys-grid">
  {key_cards}
</div>

<div class="section-title">Recent Requests</div>
<table class="log-table">
  <thead>
    <tr><th>Time</th><th>Method</th><th>Path</th><th>Status</th><th>Key</th></tr>
  </thead>
  <tbody>
    {log_rows}
  </tbody>
</table>

</body>
</html>"""


async def dashboard_handler(request: web.Request) -> web.Response:
    # Build key cards
    key_cards = ""
    for key in pool.keys:
        s = pool.stats[key]
        active_class = "active" if s["active"] else ""
        last = s["last_used"] or "—"
        key_cards += (
            f'<div class="key-card {active_class}">'
            f'<div class="key-header">'
            f'<div class="key-dot"></div>'
            f'<div class="key-name">{html.escape(s["short"])}</div>'
            f'<div style="margin-left:auto;font-size:11px;color:#6b7a8d">Last: {last}</div>'
            f'</div>'
            f'<div class="key-stats">'
            f'<div class="key-stat"><div class="num ok">{s["requests"]}</div><div class="lbl">Requests</div></div>'
            f'<div class="key-stat"><div class="num warn">{s["rate_limits"]}</div><div class="lbl">429s</div></div>'
            f'<div class="key-stat"><div class="num err">{s["errors"]}</div><div class="lbl">Errors</div></div>'
            f'</div></div>'
        )

    # Build log rows (most recent first)
    log_rows = ""
    for entry in reversed(pool.request_log):
        sc = entry["status"]
        badge_class = "s2xx" if 200 <= sc < 300 else ("s4xx" if 400 <= sc < 500 else "s5xx")
        path_display = html.escape(entry["path"][:60])
        log_rows += (
            f'<tr>'
            f'<td style="color:#6b7a8d">{entry["time"]}</td>'
            f'<td>{entry["method"]}</td>'
            f'<td>{path_display}</td>'
            f'<td><span class="status-badge {badge_class}">{sc}</span></td>'
            f'<td style="color:#6b7a8d">{entry["key"]}</td>'
            f'</tr>'
        )

    if not log_rows:
        log_rows = '<tr><td colspan="5" style="text-align:center;color:#374151;padding:24px">No requests yet</td></tr>'

    # Totals
    total_rl = sum(s["rate_limits"] for s in pool.stats.values())
    total_err = sum(s["errors"] for s in pool.stats.values())
    total_success = pool.total_requests - total_err

    page = build_dashboard_html(
        uptime=pool.get_uptime(),
        host=LISTEN_HOST,
        port=LISTEN_PORT,
        rpk=REQUESTS_PER_KEY,
        num_keys=len(pool.keys),
        max_retries=MAX_RETRIES,
        total_requests=pool.total_requests,
        total_success=max(0, total_success),
        total_rate_limits=total_rl,
        total_errors=total_err,
        key_cards=key_cards,
        log_rows=log_rows,
    )
    return web.Response(text=page, content_type="text/html")


# JSON stats endpoint
async def stats_json_handler(request: web.Request) -> web.Response:
    total_rl = sum(s["rate_limits"] for s in pool.stats.values())
    total_err = sum(s["errors"] for s in pool.stats.values())
    return web.json_response({
        "uptime": pool.get_uptime(),
        "total_requests": pool.total_requests,
        "total_rate_limits": total_rl,
        "total_errors": total_err,
        "total_retries": pool.total_retries,
        "keys": {
            pool.stats[k]["short"]: {
                "requests": pool.stats[k]["requests"],
                "rate_limits": pool.stats[k]["rate_limits"],
                "errors": pool.stats[k]["errors"],
                "active": pool.stats[k]["active"],
                "last_used": pool.stats[k]["last_used"],
            }
            for k in pool.keys
        },
    })


# --- App Setup ---
def create_app() -> web.Application:
    app = web.Application()
    app.router.add_route("GET", "/favicon.ico", favicon_handler)
    app.router.add_route("GET", "/_stats", dashboard_handler)
    app.router.add_route("GET", "/_stats/json", stats_json_handler)
    app.router.add_route("*", "/{path:.*}", proxy_handler)
    return app


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print()
    print("  \033[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    print("  \033[1m\033[36m  Frosty API Key Rotator\033[0m")
    print("  \033[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    print()
    print(f"  \033[37mProxy\033[0m      http://{LISTEN_HOST}:{LISTEN_PORT}")
    print(f"  \033[37mDashboard\033[0m  http://{LISTEN_HOST}:{LISTEN_PORT}/_stats")
    print(f"  \033[37mKeys\033[0m       {len(pool.keys)} loaded")
    print(f"  \033[37mRotation\033[0m   every {REQUESTS_PER_KEY} requests per key")
    print(f"  \033[37mOn 429\033[0m     instant switch + retry (up to {MAX_RETRIES}x)")
    print()
    print("  \033[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    print("  \033[90mRequest log:\033[0m")
    print()

    app = create_app()
    web.run_app(app, host=LISTEN_HOST, port=LISTEN_PORT, print=None)


if __name__ == "__main__":
    pool = KeyPool(KEYS_FILE)
    main()
