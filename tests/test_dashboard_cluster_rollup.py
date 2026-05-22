"""Tests for dashboard opportunity rollups."""

import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import OpportunityCluster, PainPoint
from scanner.scoring import score_opportunity_ranking
from scanner.sqlite_storage import ScannerDatabase


def _pain(source_url: str, quote: str) -> PainPoint:
    return PainPoint(
        source_url=source_url,
        source_type="hn",
        quote=quote,
        audience="builders",
        pain="manual update workflow",
        intensity=4,
        frequency=4,
        buyer_quality=4,
        workaround_cost=4,
        existing_spend=2,
        reachability=4,
        mvp_simplicity=4,
        competition_gap=3,
    )


def _cluster(title: str, pain: PainPoint, summary: str) -> OpportunityCluster:
    cluster = OpportunityCluster(
        title=title,
        pain_points=[pain],
        audience="builders",
        executive_summary=summary,
    )
    score_opportunity_ranking(cluster)
    return cluster


def test_top_clusters_rolls_up_duplicate_titles_across_scan_runs():
    with tempfile.TemporaryDirectory() as tmp:
        db = ScannerDatabase(str(Path(tmp) / "scanner.sqlite"))
        pain1 = _pain("https://news.ycombinator.com/item?id=1", "I manually update screenshots every release.")
        pain2 = _pain("https://news.ycombinator.com/item?id=2", "I manually update docs every release.")
        cluster1 = _cluster("Automated Pain Point Opportunities", pain1, "first duplicate")
        cluster2 = _cluster("Automated Pain Point Opportunities", pain2, "second duplicate")

        db.persist_scan("hn:manual update", "report1.md", 1, [pain1], [cluster1])
        db.persist_scan("hn:manual update", "report2.md", 1, [pain2], [cluster2])

        rows = db.top_clusters()

        assert len(rows) == 1
        assert rows[0]["title"] == "Automated Pain Point Opportunities"
        assert rows[0]["evidence_count"] == 2
        assert rows[0]["total_mentions"] == 2
        assert rows[0]["executive_summary"] == "2 scan runs rolled up for this opportunity. Open detail for evidence."
        evidence = db.pain_points_for_cluster(rows[0]["id"])
        assert len(evidence) == 2
        assert {row["source_url"] for row in evidence} == {
            "https://news.ycombinator.com/item?id=1",
            "https://news.ycombinator.com/item?id=2",
        }


if __name__ == "__main__":
    print("Running tests...")
    test_top_clusters_rolls_up_duplicate_titles_across_scan_runs()
    print("✓ test_top_clusters_rolls_up_duplicate_titles_across_scan_runs")
    print("\nAll tests passed! ✓")
