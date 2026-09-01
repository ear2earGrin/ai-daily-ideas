#!/usr/bin/env python3
"""Tests for the idea assessment scorer and ranker."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import rank_ideas as ri


def _assessment(**overrides):
    scores = {k: 3 for k in ri.VIABILITY_FIELDS + ri.BUILDABILITY_FIELDS}
    costs = {"setup_cost_usd": 0, "monthly_cost_usd": 0, "time_to_mvp_days": 0}
    scores.update({k: v for k, v in overrides.items() if k in scores})
    costs.update({k: v for k, v in overrides.items() if k in costs})
    return ri.score_assessment(
        ri.Assessment(
            path=Path("assessments/x.md"),
            slug=overrides.get("slug", "x"),
            idea_title=overrides.get("idea_title", "X"),
            assessed_on="2026-09-01",
            assessed_by="test",
            scores=scores,
            costs=costs,
        )
    )


def test_axis_scores_scale_to_100():
    a = _assessment(**{k: 5 for k in ri.VIABILITY_FIELDS + ri.BUILDABILITY_FIELDS})
    assert a.viability_score == 100, a.viability_score
    assert a.buildability_score == 100, a.buildability_score
    print("✓ test_axis_scores_scale_to_100")


def test_perfect_free_idea_scores_100():
    a = _assessment(**{k: 5 for k in ri.VIABILITY_FIELDS + ri.BUILDABILITY_FIELDS})
    assert a.priority_score == 100, a.priority_score
    assert a.priority_band == "build-next", a.priority_band
    print("✓ test_perfect_free_idea_scores_100")


def test_multiplication_punishes_one_weak_axis():
    """A lucrative-but-unbuildable idea must not outrank a balanced one."""
    lopsided = _assessment(
        **{k: 5 for k in ri.VIABILITY_FIELDS},
        **{k: 1 for k in ri.BUILDABILITY_FIELDS},
    )
    balanced = _assessment()  # all 3s
    assert lopsided.viability_score > balanced.viability_score
    assert lopsided.priority_score < balanced.priority_score, (
        lopsided.priority_score,
        balanced.priority_score,
    )
    print("✓ test_multiplication_punishes_one_weak_axis")


def test_cost_index_and_bands():
    # 1000 setup + 100/mo + 7 days == 1 + 1 + 1 == 3.0 -> lean, inclusive upper bound.
    a = _assessment(setup_cost_usd=1000, monthly_cost_usd=100, time_to_mvp_days=7)
    assert a.cost_index == 3.0, a.cost_index
    assert a.cost_band == "lean", a.cost_band
    assert a.cost_multiplier == 1.00

    b = _assessment(setup_cost_usd=2000, monthly_cost_usd=200, time_to_mvp_days=14)
    assert b.cost_index == 6.0 and b.cost_band == "moderate", (b.cost_index, b.cost_band)

    c = _assessment(setup_cost_usd=4000, monthly_cost_usd=400, time_to_mvp_days=28)
    assert c.cost_index == 12.0 and c.cost_band == "heavy", (c.cost_index, c.cost_band)

    d = _assessment(setup_cost_usd=50000, monthly_cost_usd=500, time_to_mvp_days=90)
    assert d.cost_band == "capital-intensive" and d.cost_multiplier == 0.45
    print("✓ test_cost_index_and_bands")


def test_expensive_idea_ranks_below_identical_cheap_one():
    cheap = _assessment()
    pricey = _assessment(setup_cost_usd=50000, monthly_cost_usd=1000, time_to_mvp_days=120)
    assert cheap.viability_score == pricey.viability_score
    assert cheap.buildability_score == pricey.buildability_score
    assert cheap.priority_score > pricey.priority_score
    print("✓ test_expensive_idea_ranks_below_identical_cheap_one")


def test_priority_bands():
    assert ri.priority_band(100) == "build-next"
    assert ri.priority_band(60) == "build-next"
    assert ri.priority_band(59) == "queued"
    assert ri.priority_band(45) == "queued"
    assert ri.priority_band(44) == "revisit"
    assert ri.priority_band(30) == "revisit"
    assert ri.priority_band(29) == "park"
    assert ri.priority_band(0) == "park"
    print("✓ test_priority_bands")


def test_raw_drop_without_frontmatter_is_parsed():
    """Grok's daily drops arrive with no frontmatter and must still enter the queue."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "2026-07-01-some-idea.md"
        path.write_text(
            "## Daily AI Solo Idea - July 1, 2026\n\n"
            "**Idea: Widget Sorting Agent**\n\n"
            "**Description:** Sorts widgets.\n",
            encoding="utf-8",
        )
        idea = ri.idea_from_file(path)
    assert idea.normalized is False
    assert idea.idea_date == "2026-07-01", idea.idea_date
    # The "**Idea: ...**" line wins over the generic date heading above it.
    assert idea.title == "Widget Sorting Agent", idea.title
    print("✓ test_raw_drop_without_frontmatter_is_parsed")


def test_undated_raw_drop_still_parses():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "some-loose-idea.md"
        path.write_text("# A Loose Idea\n\nBody.\n", encoding="utf-8")
        idea = ri.idea_from_file(path)
    assert idea.idea_date == ""
    assert idea.title == "A Loose Idea"
    print("✓ test_undated_raw_drop_still_parses")


def test_frontmatter_idea_is_marked_normalized():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "2026-07-02-x.md"
        path.write_text(
            "---\ntitle: Real Title\ndate: 2026-07-02\nslug: 2026-07-02-x\n---\n\n# Ignored\n",
            encoding="utf-8",
        )
        idea = ri.idea_from_file(path)
    assert idea.normalized is True
    assert idea.title == "Real Title"
    print("✓ test_frontmatter_idea_is_marked_normalized")


def test_slug_mismatch_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "2026-07-03-x.md"
        path.write_text("---\nslug: wrong-slug\n---\n\nbody\n", encoding="utf-8")
        try:
            ri.idea_from_file(path)
        except ri.AssessmentError as exc:
            assert "must match filename stem" in str(exc)
        else:
            raise AssertionError("expected AssessmentError for slug mismatch")
    print("✓ test_slug_mismatch_is_rejected")


def test_out_of_range_score_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "a.md"
        fields = "\n".join(
            f"{k}: 3" for k in ri.VIABILITY_FIELDS + ri.BUILDABILITY_FIELDS
        )
        path.write_text(
            "---\nslug: a\nidea_title: A\nassessed_on: 2026-09-01\nassessed_by: t\n"
            + fields.replace("pain_intensity: 3", "pain_intensity: 9")
            + "\nsetup_cost_usd: 0\nmonthly_cost_usd: 0\ntime_to_mvp_days: 0\n---\n\nbody\n",
            encoding="utf-8",
        )
        try:
            ri.assessment_from_file(path)
        except ri.AssessmentError as exc:
            assert "between 0 and 5" in str(exc), str(exc)
        else:
            raise AssertionError("expected AssessmentError for out-of-range score")
    print("✓ test_out_of_range_score_is_rejected")


def test_missing_field_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "a.md"
        path.write_text(
            "---\nslug: a\nidea_title: A\nassessed_on: 2026-09-01\nassessed_by: t\n---\n\nbody\n",
            encoding="utf-8",
        )
        try:
            ri.assessment_from_file(path)
        except ri.AssessmentError as exc:
            assert "missing required field" in str(exc)
        else:
            raise AssertionError("expected AssessmentError for missing field")
    print("✓ test_missing_field_is_rejected")


def test_rank_orders_by_priority_then_viability_then_oldest():
    def entry(slug, date_str, **kw):
        idea = ri.Idea(
            path=Path(f"ideas/{slug}.md"),
            slug=slug,
            idea_date=date_str,
            title=slug,
            normalized=True,
        )
        return ri.RankedIdea(idea=idea, assessment=_assessment(slug=slug, **kw))

    # Two identical scorers plus one clear winner.
    older = entry("2026-01-01-a", "2026-01-01")
    newer = entry("2026-02-01-b", "2026-02-01")
    winner = entry(
        "2026-03-01-c",
        "2026-03-01",
        **{k: 5 for k in ri.VIABILITY_FIELDS + ri.BUILDABILITY_FIELDS},
    )

    ranked = ri.rank([newer, winner, older])
    assert [e.slug for e in ranked] == [
        "2026-03-01-c",
        "2026-01-01-a",
        "2026-02-01-b",
    ], [e.slug for e in ranked]
    assert [e.rank for e in ranked] == [1, 2, 3]
    print("✓ test_rank_orders_by_priority_then_viability_then_oldest")


def test_pending_is_oldest_first():
    def idea(slug, date_str):
        return ri.RankedIdea(
            idea=ri.Idea(
                path=Path(f"ideas/{slug}.md"),
                slug=slug,
                idea_date=date_str,
                title=slug,
                normalized=True,
            )
        )

    entries = [idea("c", "2026-03-01"), idea("a", "2026-01-01"), idea("b", "2026-02-01")]
    assert [e.slug for e in ri.pending(entries)] == ["a", "b", "c"]
    print("✓ test_pending_is_oldest_first")


def test_pending_excludes_assessed_ideas():
    assessed = ri.RankedIdea(
        idea=ri.Idea(Path("ideas/a.md"), "a", "2026-01-01", "A", True),
        assessment=_assessment(slug="a"),
    )
    todo = ri.RankedIdea(idea=ri.Idea(Path("ideas/b.md"), "b", "2026-02-01", "B", True))
    assert [e.slug for e in ri.pending([assessed, todo])] == ["b"]
    print("✓ test_pending_excludes_assessed_ideas")


def test_repo_state_is_consistent():
    """The real repo must parse, and RANKING.md must match what the scorer produces."""
    entries = ri.build_entries()
    assert entries, "no ideas found"
    rendered = ri.render_ranking(entries)
    current = ri.RANKING_PATH.read_text(encoding="utf-8")
    assert current == rendered, "RANKING.md is stale; run python3 scripts/rank_ideas.py"
    print(f"✓ test_repo_state_is_consistent ({len(entries)} ideas)")


print("Running tests...")
test_axis_scores_scale_to_100()
test_perfect_free_idea_scores_100()
test_multiplication_punishes_one_weak_axis()
test_cost_index_and_bands()
test_expensive_idea_ranks_below_identical_cheap_one()
test_priority_bands()
test_raw_drop_without_frontmatter_is_parsed()
test_undated_raw_drop_still_parses()
test_frontmatter_idea_is_marked_normalized()
test_slug_mismatch_is_rejected()
test_out_of_range_score_is_rejected()
test_missing_field_is_rejected()
test_rank_orders_by_priority_then_viability_then_oldest()
test_pending_is_oldest_first()
test_pending_excludes_assessed_ideas()
test_repo_state_is_consistent()
print("\nAll tests passed! ✓")
