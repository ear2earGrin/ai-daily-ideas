"""Tests for local dashboard routes."""

import http.client
import importlib.util
import tempfile
import threading
from pathlib import Path
import sys
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import OpportunityCluster, PainPoint
from scanner.scoring import score_opportunity_ranking
from scanner.sqlite_storage import ScannerDatabase

_dashboard_path = Path(__file__).parent.parent / "scripts" / "run_dashboard.py"
_spec = importlib.util.spec_from_file_location("run_dashboard", _dashboard_path)
assert _spec and _spec.loader
_dashboard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_dashboard)
make_server = _dashboard.make_server


def _start_server(db_path):
    server = make_server(db_path, "127.0.0.1", 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, server.server_address[1]


def test_dashboard_home_and_update():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "scanner.sqlite")
        db = ScannerDatabase(db_path)
        pain = PainPoint(
            source_url="https://reddit.com/r/test/synthetic/003",
            quote="I need a local dashboard for reviewing findings.",
            audience="builders",
            pain="reviewing findings manually",
            intensity=4,
            frequency=4,
            buyer_quality=3,
            workaround_cost=4,
            existing_spend=3,
            reachability=4,
            mvp_simplicity=5,
            competition_gap=4,
        )
        cluster = OpportunityCluster(
            title="Dashboard review workflow",
            pain_points=[pain],
            audience="builders",
            executive_summary="Builders need a way to rank scanner findings.",
        )
        score_opportunity_ranking(cluster)
        db.persist_scan("fixture.json", "report.md", 1, [pain], [cluster])

        server, thread, port = _start_server(db_path)
        try:
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            conn.request("GET", "/")
            resp = conn.getresponse()
            body = resp.read().decode("utf-8")
            assert resp.status == 200
            assert "Market Problem Scanner Dashboard" in body
            assert "reviewing findings manually" in body
            assert "Ranked Opportunities" in body
            assert "Profitability" in body
            assert "Build probability" in body
            assert "Dashboard review workflow" in body
            assert "fixture.json" in body

            conn.request("GET", f"/cluster?id={cluster.id}")
            resp = conn.getresponse()
            detail = resp.read().decode("utf-8")
            assert resp.status == 200
            assert "Opportunity Detail" in detail
            assert "Next validation" in detail
            assert "48-hour concierge MVP" in detail

            payload = urlencode({
                "kind": "pain",
                "id": pain.id,
                "status": "validate",
                "notes": "dashboard route test",
            })
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            conn.request("POST", "/update", payload, headers)
            resp = conn.getresponse()
            resp.read()
            assert resp.status == 303

            row = db.top_pain_points()[0]
            assert row["status"] == "validate"
            assert row["notes"] == "dashboard route test"
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    print("Running tests...")
    test_dashboard_home_and_update()
    print("✓ test_dashboard_home_and_update")
    print("\nAll tests passed! ✓")
