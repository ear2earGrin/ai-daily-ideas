"""Tests for turning extracted pain points into named opportunities."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import PainPoint
from scanner.opportunity_builder import build_opportunity_clusters, synthesize_opportunity_title


def _pain(pain: str, audience: str = "freelancers", quote: str = "") -> PainPoint:
    return PainPoint(
        source_url="https://news.ycombinator.com/item?id=123",
        source_type="hn",
        quote=quote or f"I keep dealing with {pain} every week.",
        audience=audience,
        pain=pain,
        intensity=4,
        frequency=4,
        buyer_quality=3,
        workaround_cost=4,
        existing_spend=2,
        reachability=4,
        mvp_simplicity=4,
        competition_gap=3,
    )


def test_synthesize_opportunity_title_uses_pain_and_audience_not_generic_label():
    title = synthesize_opportunity_title([
        _pain("manual invoice spreadsheet entry", "freelancers"),
        _pain("copying invoices into spreadsheets", "freelancers"),
    ])

    assert title == "Freelancer invoice spreadsheet automation"
    assert title != "Automated Pain Point Opportunities"


def test_build_opportunity_clusters_groups_related_pains_and_names_each_group():
    pains = [
        _pain("manual invoice spreadsheet entry", "freelancers"),
        _pain("copying invoices into spreadsheets", "freelancers"),
        _pain("manually updating product screenshots", "developers"),
    ]

    clusters = build_opportunity_clusters(pains, source_label="hn:manual work")

    assert len(clusters) == 2
    titles = [cluster.title for cluster in clusters]
    assert "Freelancer invoice spreadsheet automation" in titles
    assert "Developer screenshot update automation" in titles
    assert "Automated Pain Point Opportunities" not in titles

    invoice_cluster = next(cluster for cluster in clusters if "invoice" in cluster.title.lower())
    assert invoice_cluster.domain == "finance-ops"
    assert invoice_cluster.audience == "freelancers"
    assert invoice_cluster.total_mentions == 2
    assert "2 public evidence posts" in invoice_cluster.executive_summary


def test_fixture_like_titles_ignore_sentence_filler_words():
    pains = [
        _pain("manual syncing inventory between shopify and", "e-commerce"),
        _pain("i wish there was a simple tool that could auto-generate invoices from my time logs without all the e", "general users"),
        _pain(
            "lack of solution for automate this without paying",
            "general users",
            "There's no good way to automate this without paying $200/month for a full CRM like Salesforce.",
        ),
        _pain("manual tracking my travel expenses for", "general users"),
    ]

    titles = [cluster.title for cluster in build_opportunity_clusters(pains, source_label="fixture")]

    assert "E-commerce inventory sync automation" in titles
    assert "General users invoice time-log automation" in titles
    assert "General users CRM follow-up automation" in titles
    assert "General users travel expense automation" in titles
    banned_fragments = ["between", "all auto-generate", "paying this", "expenses tracking"]
    for title in titles:
        assert not any(fragment in title.lower() for fragment in banned_fragments)


if __name__ == "__main__":
    print("Running tests...")
    test_synthesize_opportunity_title_uses_pain_and_audience_not_generic_label()
    print("✓ test_synthesize_opportunity_title_uses_pain_and_audience_not_generic_label")
    test_build_opportunity_clusters_groups_related_pains_and_names_each_group()
    print("✓ test_build_opportunity_clusters_groups_related_pains_and_names_each_group")
    test_fixture_like_titles_ignore_sentence_filler_words()
    print("✓ test_fixture_like_titles_ignore_sentence_filler_words")
    print("\nAll tests passed! ✓")
