#!/usr/bin/env python3
"""Local web dashboard for Market Problem Scanner findings."""

from __future__ import annotations

import argparse
import html
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.sqlite_storage import STATUS_VALUES, ScannerDatabase


CSS = """
:root { color-scheme: dark; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0b0f17; color: #e5e7eb; }
a { color: #7dd3fc; }
header { padding: 28px 32px; background: linear-gradient(135deg, #111827, #1e1b4b); border-bottom: 1px solid #243042; }
main { padding: 24px 32px 48px; max-width: 1280px; margin: 0 auto; }
h1 { margin: 0 0 8px; font-size: 30px; }
h2 { margin-top: 34px; border-bottom: 1px solid #243042; padding-bottom: 8px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; }
.card { background: #111827; border: 1px solid #243042; border-radius: 14px; padding: 16px; box-shadow: 0 10px 25px rgba(0,0,0,.18); }
.metric { font-size: 28px; font-weight: 800; color: #facc15; }
.label { color: #9ca3af; font-size: 13px; text-transform: uppercase; letter-spacing: .05em; }
table { width: 100%; border-collapse: collapse; background: #111827; border: 1px solid #243042; border-radius: 14px; overflow: hidden; }
th, td { padding: 10px 12px; border-bottom: 1px solid #243042; vertical-align: top; text-align: left; }
th { color: #9ca3af; font-size: 12px; text-transform: uppercase; letter-spacing: .05em; background: #0f172a; }
tr:last-child td { border-bottom: 0; }
.badge { display: inline-block; padding: 3px 8px; border-radius: 999px; background: #172554; color: #bfdbfe; font-size: 12px; }
.score { font-weight: 800; color: #facc15; }
.excerpt { max-width: 420px; }
form.inline { display: grid; gap: 6px; min-width: 220px; }
select, input, button { background: #020617; color: #e5e7eb; border: 1px solid #334155; border-radius: 8px; padding: 7px 9px; }
button { cursor: pointer; background: #2563eb; border-color: #2563eb; font-weight: 700; }
button:hover { background: #1d4ed8; }
.small { color: #9ca3af; font-size: 12px; }
.empty { color: #9ca3af; padding: 16px; background: #111827; border-radius: 14px; border: 1px solid #243042; }
"""


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def status_form(kind: str, item_id: str, status: str, notes: str) -> str:
    options = "".join(
        f'<option value="{esc(s)}" {"selected" if s == status else ""}>{esc(s)}</option>'
        for s in sorted(STATUS_VALUES)
    )
    return f"""
    <form class="inline" method="post" action="/update">
      <input type="hidden" name="kind" value="{esc(kind)}">
      <input type="hidden" name="id" value="{esc(item_id)}">
      <select name="status">{options}</select>
      <input name="notes" value="{esc(notes)}" placeholder="notes">
      <button type="submit">Save</button>
    </form>
    """


def render_home(db: ScannerDatabase) -> str:
    summary = db.summary()
    runs = db.recent_scan_runs()
    clusters = db.top_clusters()
    pains = db.top_pain_points()

    run_rows = "".join(
        f"""
        <tr>
          <td>#{row['id']}</td>
          <td>{esc(row['created_at'])}</td>
          <td>{esc(row['source_count'])}</td>
          <td>{esc(row['pain_point_count'])}</td>
          <td>{esc(row['cluster_count'])}</td>
          <td><code>{esc(row['report_path'])}</code></td>
        </tr>
        """
        for row in runs
    ) or '<tr><td colspan="6" class="small">No scan runs yet. Run the scanner with --db first.</td></tr>'

    cluster_rows = "".join(
        f"""
        <tr>
          <td><span class="score">{esc(round(row['avg_score'], 1))}</span></td>
          <td><strong>{esc(row['title'])}</strong><div class="small">{esc(row['executive_summary'])}</div></td>
          <td>{esc(row['domain'])}</td>
          <td>{esc(row['audience'])}</td>
          <td>{esc(row['evidence_count'])}</td>
          <td><span class="badge">{esc(row['status'])}</span></td>
          <td>{status_form('cluster', row['id'], row['status'], row['notes'])}</td>
        </tr>
        """
        for row in clusters
    ) or '<tr><td colspan="7" class="small">No clusters yet.</td></tr>'

    pain_rows = "".join(
        f"""
        <tr>
          <td><span class="score">{esc(row['total_score'])}</span></td>
          <td class="excerpt"><strong>{esc(row['pain'] or row['quote'])}</strong><div class="small">{esc(row['quote'])}</div></td>
          <td>{esc(row['audience'])}</td>
          <td><a href="{esc(row['source_url'])}" target="_blank" rel="noreferrer">source</a><div class="small">{esc(row['source_type'])}</div></td>
          <td><span class="badge">{esc(row['status'])}</span></td>
          <td>{status_form('pain', row['id'], row['status'], row['notes'])}</td>
        </tr>
        """
        for row in pains
    ) or '<tr><td colspan="6" class="small">No pain points yet.</td></tr>'

    return f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Market Problem Scanner Dashboard</title>
      <style>{CSS}</style>
    </head>
    <body>
      <header>
        <h1>Market Problem Scanner Dashboard</h1>
        <div class="small">Local-first review board for stored pain points, source evidence, and opportunity clusters.</div>
      </header>
      <main>
        <section class="grid">
          <div class="card"><div class="metric">{summary['scan_runs']}</div><div class="label">Scan runs</div></div>
          <div class="card"><div class="metric">{summary['pain_points']}</div><div class="label">Pain points</div></div>
          <div class="card"><div class="metric">{summary['clusters']}</div><div class="label">Clusters</div></div>
          <div class="card"><div class="metric">{summary['high_score_pain_points']}</div><div class="label">High-score pains</div></div>
          <div class="card"><div class="metric">{summary['interesting_items']}</div><div class="label">Marked useful</div></div>
        </section>

        <h2>Top Opportunity Clusters</h2>
        <table>
          <thead><tr><th>Score</th><th>Cluster</th><th>Domain</th><th>Audience</th><th>Evidence</th><th>Status</th><th>Review</th></tr></thead>
          <tbody>{cluster_rows}</tbody>
        </table>

        <h2>Pain Points</h2>
        <table>
          <thead><tr><th>Score</th><th>Pain</th><th>Audience</th><th>Source</th><th>Status</th><th>Review</th></tr></thead>
          <tbody>{pain_rows}</tbody>
        </table>

        <h2>Recent Scan Runs</h2>
        <table>
          <thead><tr><th>ID</th><th>Created</th><th>Sources</th><th>Pain points</th><th>Clusters</th><th>Report</th></tr></thead>
          <tbody>{run_rows}</tbody>
        </table>
      </main>
    </body>
    </html>
    """


class DashboardHandler(BaseHTTPRequestHandler):
    db_path = "data/scanner.sqlite"

    def log_message(self, format, *args):
        return

    @property
    def db(self) -> ScannerDatabase:
        return ScannerDatabase(self.db_path)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path not in {"/", "/index.html"}:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        body = render_home(self.db).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/update":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        data: Dict[str, list[str]] = parse_qs(raw)
        kind = data.get("kind", [""])[0]
        item_id = data.get("id", [""])[0]
        status = data.get("status", ["new"])[0]
        notes = data.get("notes", [""])[0]
        table = {"pain": "pain_points", "cluster": "clusters"}.get(kind)
        if not table or not item_id:
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid update payload")
            return
        try:
            self.db.update_status_notes(table, item_id, status, notes)
        except ValueError as exc:
            self.send_error(HTTPStatus.BAD_REQUEST, str(exc))
            return
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", "/")
        self.end_headers()


def make_server(db_path: str, host: str, port: int) -> ThreadingHTTPServer:
    ScannerDatabase(db_path)
    handler = type("ConfiguredDashboardHandler", (DashboardHandler,), {"db_path": db_path})
    return ThreadingHTTPServer((host, port), handler)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local Market Problem Scanner dashboard")
    parser.add_argument("--db", default="data/scanner.sqlite", help="SQLite database path")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host. Defaults to local-only 127.0.0.1")
    parser.add_argument("--port", default=8765, type=int, help="Bind port")
    args = parser.parse_args()

    server = make_server(args.db, args.host, args.port)
    url = f"http://{args.host}:{args.port}"
    print(f"📊 Market Problem Scanner dashboard")
    print(f"🗄️  Database: {args.db}")
    print(f"🌐 Listening locally at: {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
