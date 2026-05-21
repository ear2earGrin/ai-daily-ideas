"""Tests for profitability/probability opportunity ranking."""

import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import OpportunityCluster, PainPoint
from scanner.scoring import score_opportunity_ranking, rank_clusters
from scanner.sqlite_storage import ScannerDatabase


def _pain(**kwargs):
    defaults = {
        "source_url": "https://reddit.com/r/test/synthetic/ranking",
        "quote": "We already pay for a clunky tool and still do manual work every week.",
        "audience": "small agencies",
        "pain": "manual ops work",
        "intensity": 4,
        "frequency": 4,
        "buyer_quality": 4,
        "workaround_cost": 4,
        "existing_spend": 4,
        "reachability": 3,
        "mvp_simplicity": 4,
        "competition_gap": 3,
    }
    defaults.update(kwargs)
    return PainPoint(**defaults)


def test_score_opportunity_ranking_calculates_two_axes_and_priority():
    cluster = OpportunityCluster(
        title="Agency invoice ops",
        pain_points=[_pain()],
        audience="small agencies",
        domain="finance ops",
    )

    scored = score_opportunity_ranking(cluster)

    assert scored.profitability_score == 27
    assert scored.build_probability_score == 26
    assert scored.priority_score == 702
    assert scored.priority_band == "promising"
    assert scored.buyer_type == "small agencies"
    assert "$49-199/mo or $500-2k setup" in scored.monetization_guess
    assert "48-hour concierge MVP" in scored.mvp_shape
    assert "Find 10 more public posts" in scored.next_validation_step
    assert "buyer budget" not in scored.missing_data.lower()


def test_ranking_penalizes_lopsided_ideas():
    sexy_but_hard = OpportunityCluster(
        title="Enterprise legal OS",
        pain_points=[_pain(buyer_quality=5, existing_spend=5, mvp_simplicity=1, reachability=1, competition_gap=1)],
    )
    boring_but_shippable = OpportunityCluster(
        title="Invoice reminder helper",
        pain_points=[_pain(buyer_quality=3, existing_spend=3, mvp_simplicity=5, reachability=5, competition_gap=4)],
    )

    ranked = rank_clusters([sexy_but_hard, boring_but_shippable])

    assert ranked[0].title == "Invoice reminder helper"
    assert ranked[0].priority_score > ranked[1].priority_score


def test_database_persists_ranking_fields_and_orders_by_priority():
    with tempfile.TemporaryDirectory() as tmp:
        db = ScannerDatabase(str(Path(tmp) / "scanner.sqlite"))
        weak = OpportunityCluster(title="Weak idea", pain_points=[_pain(intensity=1, frequency=1, existing_spend=0)])
        strong = OpportunityCluster(title="Strong idea", pain_points=[_pain(intensity=5, frequency=5, existing_spend=5)])
        score_opportunity_ranking(weak)
        score_opportunity_ranking(strong)

        db.persist_scan("fixture.json", "report.md", 2, weak.pain_points + strong.pain_points, [weak, strong])
        rows = db.top_clusters()

        assert rows[0]["title"] == "Strong idea"
        assert rows[0]["profitability_score"] > rows[1]["profitability_score"]
        assert rows[0]["build_probability_score"] > 0
        assert rows[0]["priority_score"] > rows[1]["priority_score"]
        assert rows[0]["priority_band"] in {"validate immediately", "promising"}


if __name__ == "__main__":
    print("Running tests...")
    test_score_opportunity_ranking_calculates_two_axes_and_priority()
    print("✓ test_score_opportunity_ranking_calculates_two_axes_and_priority")
    test_ranking_penalizes_lopsided_ideas()
    print("✓ test_ranking_penalizes_lopsided_ideas")
    test_database_persists_ranking_fields_and_orders_by_priority()
    print("✓ test_database_persists_ranking_fields_and_orders_by_priority")
    print("\nAll tests passed! ✓")
