#!/usr/bin/env python3
"""Generate a catalog of AI daily ideas from markdown frontmatter.

Usage:
  python3 scripts/generate_index.py
  python3 scripts/generate_index.py --check
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, cast

ROOT = Path(__file__).resolve().parents[1]
IDEAS_DIR = ROOT / "ideas"
INDEX_PATH = ROOT / "INDEX.md"

REQUIRED_FIELDS = [
    "title",
    "date",
    "status",
    "category",
    "tags",
    "monetization",
    "effort",
    "slug",
    "summary",
]

ALLOWED_STATUS = {"draft", "ready", "validating", "building", "launched", "archived"}
ALLOWED_EFFORT = {"small", "medium", "large"}


@dataclass(frozen=True)
class Idea:
    path: Path
    title: str
    idea_date: str
    status: str
    category: str
    tags: list[str]
    monetization: str
    effort: str
    slug: str
    summary: str


def parse_frontmatter(text: str, path: Path) -> dict[str, object]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML-style frontmatter block")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: frontmatter block must end with ---")

    raw = text[4:end]
    meta: dict[str, object] = {}

    for line_no, line in enumerate(raw.splitlines(), start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{line_no}: expected 'key: value'")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"{path}:{line_no}: empty frontmatter key")
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip('"\'') for item in value[1:-1].split(",")]
            meta[key] = [item for item in items if item]
        else:
            meta[key] = value.strip('"\'')

    return meta


def validate_meta(meta: dict[str, object], path: Path) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in meta or meta[field] in ("", [])]
    if missing:
        raise ValueError(f"{path}: missing required frontmatter field(s): {', '.join(missing)}")

    try:
        date.fromisoformat(str(meta["date"]))
    except ValueError as exc:
        raise ValueError(f"{path}: date must use YYYY-MM-DD") from exc

    status = str(meta["status"])
    if status not in ALLOWED_STATUS:
        raise ValueError(f"{path}: status '{status}' must be one of {sorted(ALLOWED_STATUS)}")

    effort = str(meta["effort"])
    if effort not in ALLOWED_EFFORT:
        raise ValueError(f"{path}: effort '{effort}' must be one of {sorted(ALLOWED_EFFORT)}")

    tags = meta["tags"]
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag for tag in tags):
        raise ValueError(f"{path}: tags must be an inline list, e.g. [agent, saas]")

    slug = str(meta["slug"])
    expected_slug = path.stem
    if slug != expected_slug:
        raise ValueError(f"{path}: slug '{slug}' must match filename stem '{expected_slug}'")


def idea_from_file(path: Path) -> Idea:
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text, path)
    validate_meta(meta, path)
    tags = cast(list[str], meta["tags"])
    return Idea(
        path=path,
        title=str(meta["title"]),
        idea_date=str(meta["date"]),
        status=str(meta["status"]),
        category=str(meta["category"]),
        tags=tags,
        monetization=str(meta["monetization"]),
        effort=str(meta["effort"]),
        slug=str(meta["slug"]),
        summary=str(meta["summary"]),
    )


def collect_ideas() -> list[Idea]:
    if not IDEAS_DIR.exists():
        raise ValueError(f"missing ideas directory: {IDEAS_DIR}")
    paths = sorted(IDEAS_DIR.glob("*.md"))
    if not paths:
        raise ValueError(f"no idea markdown files found in {IDEAS_DIR}")
    ideas = [idea_from_file(path) for path in paths]
    return sorted(ideas, key=lambda idea: idea.idea_date, reverse=True)


def render_index(ideas: Iterable[Idea]) -> str:
    ideas = list(ideas)
    lines = [
        "# Idea Catalog",
        "",
        "Generated from `ideas/*.md` frontmatter.",
        "",
        f"Total ideas: {len(ideas)}",
        "",
        "| Date | Idea | Status | Category | Effort | Monetization | Tags |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idea in ideas:
        rel_path = idea.path.relative_to(ROOT).as_posix()
        tags = ", ".join(f"`{tag}`" for tag in idea.tags)
        lines.append(
            "| {date} | [{title}]({path}) | {status} | {category} | {effort} | {monetization} | {tags} |".format(
                date=idea.idea_date,
                title=escape_table(idea.title),
                path=rel_path,
                status=idea.status,
                category=escape_table(idea.category),
                effort=idea.effort,
                monetization=escape_table(idea.monetization),
                tags=tags,
            )
        )

    lines.extend([
        "",
        "## Summaries",
        "",
    ])
    for idea in ideas:
        rel_path = idea.path.relative_to(ROOT).as_posix()
        lines.extend([
            f"### [{idea.title}]({rel_path})",
            "",
            idea.summary,
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def escape_table(value: str) -> str:
    return value.replace("|", "\\|")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate that INDEX.md is up to date without writing")
    args = parser.parse_args()

    try:
        ideas = collect_ideas()
        rendered = render_index(ideas)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        current = INDEX_PATH.read_text(encoding="utf-8") if INDEX_PATH.exists() else ""
        if current != rendered:
            print("error: INDEX.md is out of date; run python3 scripts/generate_index.py", file=sys.stderr)
            return 1
        print(f"INDEX.md is up to date ({len(ideas)} ideas).")
        return 0

    INDEX_PATH.write_text(rendered, encoding="utf-8")
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)} with {len(ideas)} ideas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
