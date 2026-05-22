"""Tests for dashboard source provenance display."""

import importlib.util
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import PainPoint
from scanner.sqlite_storage import ScannerDatabase

DASHBOARD_PATH = Path(__file__).parent.parent / "scripts" / "run_dashboard.py"
spec = importlib.util.spec_from_file_location("run_dashboard", DASHBOARD_PATH)
assert spec is not None
run_dashboard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run_dashboard)


def test_dashboard_marks_synthetic_sources_and_real_hn_links():
    with tempfile.TemporaryDirectory() as tmp:
        db = ScannerDatabase(str(Path(tmp) / "scanner.sqlite"))
        synthetic = PainPoint(
            source_url="https://news.ycombinator.com/synthetic/002",
            quote="Synthetic fixture quote about invoices.",
            pain="invoice fixture",
            audience="solo founders",
            source_type="hn",
        )
        real = PainPoint(
            source_url="https://news.ycombinator.com/item?id=12345",
            quote="Real HN quote about spreadsheets.",
            pain="spreadsheet sync",
            audience="solo founders",
            source_type="hn",
        )
        db.persist_scan("fixtures/sample_pain_points.json", "report.md", 2, [synthetic, real], [])
        rows = db.top_pain_points()
        body = "\n".join(run_dashboard.pain_point_row(row) for row in rows)

        assert "synthetic fixture" in body
        assert "real source" in body
        assert "https://news.ycombinator.com/item?id=12345" in body


if __name__ == "__main__":
    print("Running tests...")
    test_dashboard_marks_synthetic_sources_and_real_hn_links()
    print("✓ test_dashboard_marks_synthetic_sources_and_real_hn_links")
    print("\nAll tests passed! ✓")
