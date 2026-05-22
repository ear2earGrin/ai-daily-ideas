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


def test_existing_database_migrates_ranking_columns_before_index_creation():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "old_scanner.sqlite"
        import sqlite3
        con = sqlite3.connect(db_path)
        con.executescript(
            """
            CREATE TABLE clusters (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                avg_score REAL NOT NULL DEFAULT 0
            );
            CREATE INDEX idx_clusters_score ON clusters(avg_score DESC);
            """
        )
        con.close()

        db = ScannerDatabase(str(db_path))
        with db.connect() as con:
            columns = {row[1] for row in con.execute("PRAGMA table_info(clusters)")}
            indexes = {row[1] for row in con.execute("PRAGMA index_list(clusters)")}

        assert "priority_score" in columns
        assert "profitability_score" in columns
        assert "idx_clusters_priority" in indexes


def test_existing_database_migrates_pain_fingerprint_before_index_creation():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "old_pain.sqlite"
        import sqlite3
        con = sqlite3.connect(db_path)
        con.executescript(
            """
            CREATE TABLE pain_points (
                id TEXT PRIMARY KEY,
                quote TEXT NOT NULL,
                pain TEXT,
                source_url TEXT NOT NULL,
                source_type TEXT,
                audience TEXT,
                domain TEXT,
                total_score INTEGER NOT NULL DEFAULT 0,
                intensity INTEGER NOT NULL DEFAULT 0,
                frequency INTEGER NOT NULL DEFAULT 0,
                buyer_quality INTEGER NOT NULL DEFAULT 0,
                workaround_cost INTEGER NOT NULL DEFAULT 0,
                existing_spend INTEGER NOT NULL DEFAULT 0,
                reachability INTEGER NOT NULL DEFAULT 0,
                mvp_simplicity INTEGER NOT NULL DEFAULT 0,
                competition_gap INTEGER NOT NULL DEFAULT 0,
                collected_at TEXT,
                status TEXT NOT NULL DEFAULT 'new',
                notes TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            );
            INSERT INTO pain_points (id, quote, source_url, updated_at)
            VALUES ('pain_old', 'I manually copy invoices.', 'https://news.ycombinator.com/item?id=1', '2026-01-01T00:00:00');
            """
        )
        con.close()

        db = ScannerDatabase(str(db_path))
        with db.connect() as con:
            columns = {row[1] for row in con.execute("PRAGMA table_info(pain_points)")}
            indexes = {row[1] for row in con.execute("PRAGMA index_list(pain_points)")}
            fingerprint = con.execute("SELECT fingerprint FROM pain_points WHERE id='pain_old'").fetchone()[0]

        assert "fingerprint" in columns
        assert "idx_pain_points_fingerprint" in indexes
        assert fingerprint


if __name__ == "__main__":
    print("Running tests...")
    test_persist_scan_and_summary()
    print("✓ test_persist_scan_and_summary")
    test_update_status_notes()
    print("✓ test_update_status_notes")
    test_existing_database_migrates_ranking_columns_before_index_creation()
    print("✓ test_existing_database_migrates_ranking_columns_before_index_creation")
    test_existing_database_migrates_pain_fingerprint_before_index_creation()
    print("✓ test_existing_database_migrates_pain_fingerprint_before_index_creation")
    print("\nAll tests passed! ✓")
