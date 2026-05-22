"""Tests for pain point fingerprint deduplication."""

import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import PainPoint
from scanner.sqlite_storage import ScannerDatabase, pain_point_fingerprint


def _pain(source_url="https://news.ycombinator.com/item?id=1", quote="I manually copy invoices every week."):
    return PainPoint(
        source_url=source_url,
        source_type="hn",
        quote=quote,
        audience="freelancers",
        pain="manual invoice copying",
        intensity=4,
        frequency=4,
        buyer_quality=3,
        workaround_cost=4,
        existing_spend=2,
        reachability=4,
        mvp_simplicity=4,
        competition_gap=3,
        total_score=28,
    )


def test_pain_point_fingerprint_normalizes_url_and_quote_spacing():
    a = _pain("https://news.ycombinator.com/item?id=1", "I manually copy invoices every week.")
    b = _pain("https://news.ycombinator.com/item?id=1&utm_source=x", "  I   manually copy invoices every week.  ")

    assert pain_point_fingerprint(a) == pain_point_fingerprint(b)


def test_persist_scan_dedupes_duplicate_pain_points_across_runs():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "scanner.sqlite")
        db = ScannerDatabase(db_path)

        first = _pain()
        second = _pain(quote="  I manually copy invoices every week. ")

        db.persist_scan("hn-pack:finance-admin", "report1.md", 1, [first], [])
        db.persist_scan("hn-pack:finance-admin", "report2.md", 1, [second], [])

        with sqlite3.connect(db_path) as con:
            pain_count = con.execute("SELECT COUNT(*) FROM pain_points").fetchone()[0]
            scan_count = con.execute("SELECT COUNT(*) FROM scan_runs").fetchone()[0]
            fingerprint = con.execute("SELECT fingerprint FROM pain_points").fetchone()[0]

        assert scan_count == 2
        assert pain_count == 1
        assert fingerprint == pain_point_fingerprint(first)


if __name__ == "__main__":
    print("Running tests...")
    test_pain_point_fingerprint_normalizes_url_and_quote_spacing()
    print("✓ test_pain_point_fingerprint_normalizes_url_and_quote_spacing")
    test_persist_scan_dedupes_duplicate_pain_points_across_runs()
    print("✓ test_persist_scan_dedupes_duplicate_pain_points_across_runs")
    print("\nAll tests passed! ✓")
