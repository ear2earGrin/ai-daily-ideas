"""Tests for SQLite scanner persistence."""

import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import OpportunityCluster, PainPoint
from scanner.scoring import score_cluster, score_pain_point
from scanner.sqlite_storage import ScannerDatabase


def test_persist_scan_and_summary():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "scanner.sqlite")
        db = ScannerDatabase(db_path)
        pain = PainPoint(
            source_url="https://reddit.com/r/test/synthetic/001",
            quote="I waste hours manually reconciling client invoices every Friday.",
            audience="small agencies",
            source_type="reddit",
            pain="manual invoice reconciliation",
        )
        score_pain_point(pain)
        cluster = OpportunityCluster(
            title="Invoice reconciliation automation",
            pain_points=[pain],
            domain="finance ops",
            audience="small agencies",
            executive_summary="Small agencies need lighter invoice automation.",
        )
        score_cluster(cluster)

        scan_id = db.persist_scan(
            fixture_path="fixtures/sample.json",
            report_path="reports/sample.md",
            source_count=1,
            pain_points=[pain],
            clusters=[cluster],
        )

        summary = db.summary()
        assert scan_id == 1
        assert summary["scan_runs"] == 1
        assert summary["pain_points"] == 1
        assert summary["clusters"] == 1
        assert db.recent_scan_runs()[0]["report_path"] == "reports/sample.md"
        assert db.top_pain_points()[0]["source_url"] == pain.source_url
        assert db.top_clusters()[0]["evidence_count"] == 1


def test_update_status_notes():
    with tempfile.TemporaryDirectory() as tmp:
        db = ScannerDatabase(str(Path(tmp) / "scanner.sqlite"))
        pain = PainPoint(
            source_url="https://news.ycombinator.com/synthetic/002",
            quote="No good simple dashboard exists for this workflow.",
            audience="solo founders",
        )
        db.persist_scan("fixture.json", "report.md", 1, [pain], [])
        db.update_status_notes("pain_points", pain.id, "interesting", "worth validating")
        row = db.top_pain_points()[0]
        assert row["status"] == "interesting"
        assert row["notes"] == "worth validating"


if __name__ == "__main__":
    print("Running tests...")
    test_persist_scan_and_summary()
    print("✓ test_persist_scan_and_summary")
    test_update_status_notes()
    print("✓ test_update_status_notes")
    print("\nAll tests passed! ✓")
