#!/usr/bin/env python3
"""Score and rank the ideas in ideas/ from their assessments in assessments/.

The scoring model lives in docs/idea-assessment-rubric.md. An assessment supplies
ten 0-5 judgements and three cost estimates; everything derived is computed here so
that no priority number is ever hand-written.

Usage:
  python3 scripts/rank_ideas.py            # regenerate RANKING.md
  python3 scripts/rank_ideas.py --check    # validate assessments and RANKING.md freshness
  python3 scripts/rank_ideas.py --next     # print the oldest idea with no assessment
  python3 scripts/rank_ideas.py --json     # dump the ranking as JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
IDEAS_DIR = ROOT / "ideas"
ASSESSMENTS_DIR = ROOT / "assessments"
RANKING_PATH = ROOT / "RANKING.md"

DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

VIABILITY_FIELDS = [
    "pain_intensity",
    "buyer_quality",
    "reachability",
    "monetization_clarity",
    "differentiation",
]
BUILDABILITY_FIELDS = [
    "mvp_simplicity",
    "data_access",
    "ai_fit",
    "low_maintenance",
    "low_compliance_risk",
]
COST_FIELDS = ["setup_cost_usd", "monthly_cost_usd", "time_to_mvp_days"]
TEXT_FIELDS = ["slug", "idea_title", "assessed_on", "assessed_by"]

# (upper bound on cost_index, band name, multiplier). Ordered, first match wins.
COST_BANDS = [
    (3.0, "lean", 1.00),
    (6.0, "moderate", 0.85),
    (12.0, "heavy", 0.65),
    (float("inf"), "capital-intensive", 0.45),
]

# (lower bound on priority_score, band name). Ordered, first match wins.
PRIORITY_BANDS = [
    (60, "build-next"),
    (45, "queued"),
    (30, "revisit"),
    (0, "park"),
]


class AssessmentError(ValueError):
    """Raised when an idea or assessment file cannot be used."""


@dataclass(frozen=True)
class Idea:
    """An idea file. Tolerant by design: raw daily drops have no frontmatter."""

    path: Path
    slug: str
    idea_date: str
    title: str
    normalized: bool


@dataclass
class Assessment:
    path: Path
    slug: str
    idea_title: str
    assessed_on: str
    assessed_by: str
    scores: dict[str, int]
    costs: dict[str, int]

    # Derived.
    viability_score: int = 0
    buildability_score: int = 0
    cost_index: float = 0.0
    cost_band: str = ""
    cost_multiplier: float = 0.0
    priority_score: int = 0
    priority_band: str = ""


@dataclass
class RankedIdea:
    idea: Idea
    assessment: Assessment | None = None
    rank: int | None = None

    @property
    def slug(self) -> str:
        return self.idea.slug

    @property
    def title(self) -> str:
        if self.assessment and self.assessment.idea_title:
            return self.assessment.idea_title
        return self.idea.title


# --------------------------------------------------------------------------- parsing


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (raw frontmatter, body). Frontmatter is None when absent."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def parse_frontmatter(raw: str, path: Path) -> dict[str, str]:
    """Parse the dependency-free `key: value` subset used across this repo."""
    meta: dict[str, str] = {}
    for line_no, line in enumerate(raw.splitlines(), start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise AssessmentError(f"{path}:{line_no}: expected 'key: value'")
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise AssessmentError(f"{path}:{line_no}: empty frontmatter key")
        meta[key] = value.strip().strip("\"'")
    return meta


IDEA_LINE_RE = re.compile(r"^\*\*Idea:\s*(.+?)\*\*\s*$")


def first_heading(body: str) -> str:
    """Best-effort title for an idea file with no frontmatter.

    Grok's raw drops lead with a generic "## Daily AI Solo Idea - <date>" heading and
    put the real name on a "**Idea: ...**" line underneath, so prefer that line when
    it exists and fall back to the first heading otherwise.
    """
    heading = ""
    for line in body.splitlines():
        stripped = line.strip()
        match = IDEA_LINE_RE.match(stripped)
        if match:
            return match.group(1).strip()
        if not heading and stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
    return heading


def idea_from_file(path: Path) -> Idea:
    """Read an idea file, tolerating unnormalized daily drops.

    Raw drops from the daily cron have no frontmatter and sometimes no date-prefixed
    filename. They still need to enter the ranking queue, so fall back to the filename
    stem and the first heading rather than rejecting them.
    """
    text = path.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    meta = parse_frontmatter(raw, path) if raw is not None else {}

    slug = path.stem
    if meta.get("slug") and meta["slug"] != slug:
        raise AssessmentError(
            f"{path}: slug '{meta['slug']}' must match filename stem '{slug}'"
        )

    idea_date = meta.get("date", "")
    if not idea_date:
        match = DATE_PREFIX_RE.match(slug)
        idea_date = match.group(1) if match else ""
    if idea_date:
        try:
            date.fromisoformat(idea_date)
        except ValueError as exc:
            raise AssessmentError(f"{path}: date must use YYYY-MM-DD") from exc

    title = meta.get("title") or first_heading(body) or slug
    return Idea(
        path=path,
        slug=slug,
        idea_date=idea_date,
        title=title,
        normalized=raw is not None,
    )


def _require_int(meta: dict[str, str], key: str, path: Path, lo: int, hi: int) -> int:
    if key not in meta or meta[key] == "":
        raise AssessmentError(f"{path}: missing required field '{key}'")
    try:
        value = int(meta[key])
    except ValueError as exc:
        raise AssessmentError(f"{path}: '{key}' must be an integer, got {meta[key]!r}") from exc
    if not lo <= value <= hi:
        raise AssessmentError(f"{path}: '{key}' must be between {lo} and {hi}, got {value}")
    return value


def assessment_from_file(path: Path) -> Assessment:
    text = path.read_text(encoding="utf-8")
    raw, _body = split_frontmatter(text)
    if raw is None:
        raise AssessmentError(f"{path}: missing YAML-style frontmatter block")
    meta = parse_frontmatter(raw, path)

    for key in TEXT_FIELDS:
        if not meta.get(key):
            raise AssessmentError(f"{path}: missing required field '{key}'")
    if meta["slug"] != path.stem:
        raise AssessmentError(
            f"{path}: slug '{meta['slug']}' must match filename stem '{path.stem}'"
        )
    try:
        date.fromisoformat(meta["assessed_on"])
    except ValueError as exc:
        raise AssessmentError(f"{path}: assessed_on must use YYYY-MM-DD") from exc

    scores = {
        key: _require_int(meta, key, path, 0, 5)
        for key in VIABILITY_FIELDS + BUILDABILITY_FIELDS
    }
    costs = {key: _require_int(meta, key, path, 0, 10_000_000) for key in COST_FIELDS}

    assessment = Assessment(
        path=path,
        slug=meta["slug"],
        idea_title=meta["idea_title"],
        assessed_on=meta["assessed_on"],
        assessed_by=meta["assessed_by"],
        scores=scores,
        costs=costs,
    )
    return score_assessment(assessment)


# --------------------------------------------------------------------------- scoring


def cost_index(costs: dict[str, int]) -> float:
    """Thousands of dollars up front, plus hundreds per month, plus weeks of work."""
    return (
        costs["setup_cost_usd"] / 1000
        + costs["monthly_cost_usd"] / 100
        + costs["time_to_mvp_days"] / 7
    )


def cost_band(index: float) -> tuple[str, float]:
    for upper, name, multiplier in COST_BANDS:
        if index <= upper:
            return name, multiplier
    raise AssertionError("COST_BANDS must end with an unbounded entry")


def priority_band(score: int) -> str:
    for lower, name in PRIORITY_BANDS:
        if score >= lower:
            return name
    raise AssertionError("PRIORITY_BANDS must end with a zero entry")


def score_assessment(assessment: Assessment) -> Assessment:
    """Compute every derived field. Pure: same inputs always give the same ranking."""
    assessment.viability_score = sum(assessment.scores[k] for k in VIABILITY_FIELDS) * 4
    assessment.buildability_score = sum(assessment.scores[k] for k in BUILDABILITY_FIELDS) * 4
    assessment.cost_index = round(cost_index(assessment.costs), 2)
    assessment.cost_band, assessment.cost_multiplier = cost_band(assessment.cost_index)
    assessment.priority_score = round(
        assessment.viability_score
        * assessment.buildability_score
        / 100
        * assessment.cost_multiplier
    )
    assessment.priority_band = priority_band(assessment.priority_score)
    return assessment


def rank(entries: list[RankedIdea]) -> list[RankedIdea]:
    """Sort assessed ideas by priority, then viability, then oldest-first.

    Oldest-first is the final tiebreak on purpose: it keeps the queue FIFO so an
    idea can never sit at the bottom forever just because it arrived early.
    """
    assessed = [e for e in entries if e.assessment is not None]
    assessed.sort(
        key=lambda e: (
            -e.assessment.priority_score,
            -e.assessment.viability_score,
            e.idea.idea_date or "9999-99-99",
            e.slug,
        )
    )
    for position, entry in enumerate(assessed, start=1):
        entry.rank = position
    return assessed


# --------------------------------------------------------------------------- collect


def collect_ideas() -> list[Idea]:
    if not IDEAS_DIR.exists():
        raise AssessmentError(f"missing ideas directory: {IDEAS_DIR}")
    paths = sorted(IDEAS_DIR.glob("*.md"))
    if not paths:
        raise AssessmentError(f"no idea markdown files found in {IDEAS_DIR}")
    return [idea_from_file(path) for path in paths]


def collect_assessments() -> dict[str, Assessment]:
    if not ASSESSMENTS_DIR.exists():
        return {}
    out: dict[str, Assessment] = {}
    for path in sorted(ASSESSMENTS_DIR.glob("*.md")):
        assessment = assessment_from_file(path)
        out[assessment.slug] = assessment
    return out


def build_entries() -> list[RankedIdea]:
    ideas = collect_ideas()
    assessments = collect_assessments()
    slugs = {idea.slug for idea in ideas}
    orphans = sorted(set(assessments) - slugs)
    if orphans:
        raise AssessmentError(
            "assessment(s) with no matching idea file: " + ", ".join(orphans)
        )
    return [RankedIdea(idea=idea, assessment=assessments.get(idea.slug)) for idea in ideas]


def pending(entries: Iterable[RankedIdea]) -> list[RankedIdea]:
    """Unassessed ideas, oldest first — the order the daily routine works through."""
    todo = [e for e in entries if e.assessment is None]
    todo.sort(key=lambda e: (e.idea.idea_date or "9999-99-99", e.slug))
    return todo


# --------------------------------------------------------------------------- render


def _money(value: int) -> str:
    return f"${value:,}"


def render_ranking(entries: list[RankedIdea]) -> str:
    ranked = rank(entries)
    todo = pending(entries)

    lines = [
        "# Idea Ranking",
        "",
        "Generated by `scripts/rank_ideas.py` from `assessments/*.md`. Do not edit by hand.",
        "",
        "Scoring model: `docs/idea-assessment-rubric.md`.",
        "`priority = viability x buildability / 100 x cost_multiplier`.",
        "",
        f"Assessed: {len(ranked)} of {len(entries)} ideas.",
        "",
    ]

    if ranked:
        leader = ranked[0]
        cleared = leader.assessment.priority_band == "build-next"
        lines.extend(
            [
                "## Build this first" if cleared else "## Top of the queue",
                "",
                f"**[{leader.title}](assessments/{leader.slug}.md)** "
                f"— priority {leader.assessment.priority_score}/100 "
                f"({leader.assessment.priority_band}), "
                f"{_money(leader.assessment.costs['setup_cost_usd'])} setup, "
                f"{leader.assessment.costs['time_to_mvp_days']} days to MVP.",
                "",
            ]
        )
        if not cleared:
            # Say so out loud. A ranking always has a first row, which is not the
            # same as having something worth starting on Monday.
            lines.extend(
                [
                    "No idea has cleared the `build-next` bar (priority 60+) yet. "
                    "This is the best of what has been assessed, not a green light.",
                    "",
                ]
            )

        lines.extend(
            [
                "## Ranking",
                "",
                "| # | Idea | Priority | Band | Viability | Buildability | Setup | Monthly | Days to MVP | Cost band |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for entry in ranked:
            a = entry.assessment
            lines.append(
                "| {rank} | [{title}](assessments/{slug}.md) | {priority} | {band} | {via} | {build} | {setup} | {monthly} | {days} | {cost_band} |".format(
                    rank=entry.rank,
                    title=escape_table(entry.title),
                    slug=entry.slug,
                    priority=a.priority_score,
                    band=a.priority_band,
                    via=a.viability_score,
                    build=a.buildability_score,
                    setup=_money(a.costs["setup_cost_usd"]),
                    monthly=_money(a.costs["monthly_cost_usd"]) + "/mo",
                    days=a.costs["time_to_mvp_days"],
                    cost_band=a.cost_band,
                )
            )
        lines.append("")

    lines.extend(["## Queue", ""])
    if todo:
        lines.append("Ideas awaiting assessment, oldest first:")
        lines.append("")
        for entry in todo:
            stamp = entry.idea.idea_date or "undated"
            lines.append(f"- {stamp} — [{escape_table(entry.title)}]({entry.idea.path.relative_to(ROOT).as_posix()})")
    else:
        lines.append("Every idea has been assessed.")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def escape_table(value: str) -> str:
    return value.replace("|", "\\|")


def as_json(entries: list[RankedIdea]) -> str:
    ranked = rank(entries)
    payload = {
        "ranked": [
            {
                "rank": e.rank,
                "slug": e.slug,
                "title": e.title,
                "priority_score": e.assessment.priority_score,
                "priority_band": e.assessment.priority_band,
                "viability_score": e.assessment.viability_score,
                "buildability_score": e.assessment.buildability_score,
                "cost_index": e.assessment.cost_index,
                "cost_band": e.assessment.cost_band,
                "cost_multiplier": e.assessment.cost_multiplier,
                "scores": e.assessment.scores,
                "costs": e.assessment.costs,
            }
            for e in ranked
        ],
        "pending": [
            {"slug": e.slug, "title": e.title, "date": e.idea.idea_date}
            for e in pending(entries)
        ],
    }
    return json.dumps(payload, indent=2) + "\n"


# --------------------------------------------------------------------------- cli


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--check",
        action="store_true",
        help="validate assessments and confirm RANKING.md is up to date",
    )
    group.add_argument(
        "--next",
        action="store_true",
        help="print the slug of the oldest idea with no assessment",
    )
    group.add_argument("--json", action="store_true", help="print the ranking as JSON")
    args = parser.parse_args()

    try:
        entries = build_entries()
    except AssessmentError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.next:
        todo = pending(entries)
        if not todo:
            print("All ideas assessed.")
            return 0
        entry = todo[0]
        print(entry.slug)
        print(f"  title: {entry.title}")
        print(f"  date:  {entry.idea.idea_date or 'undated'}")
        print(f"  file:  {entry.idea.path.relative_to(ROOT).as_posix()}")
        if not entry.idea.normalized:
            print("  note:  raw drop, no frontmatter yet")
        return 0

    if args.json:
        print(as_json(entries), end="")
        return 0

    rendered = render_ranking(entries)

    if args.check:
        current = RANKING_PATH.read_text(encoding="utf-8") if RANKING_PATH.exists() else ""
        if current != rendered:
            print(
                "error: RANKING.md is out of date; run python3 scripts/rank_ideas.py",
                file=sys.stderr,
            )
            return 1
        assessed = sum(1 for e in entries if e.assessment is not None)
        print(f"RANKING.md is up to date ({assessed}/{len(entries)} ideas assessed).")
        return 0

    RANKING_PATH.write_text(rendered, encoding="utf-8")
    assessed = sum(1 for e in entries if e.assessment is not None)
    print(f"Wrote RANKING.md ({assessed}/{len(entries)} ideas assessed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
