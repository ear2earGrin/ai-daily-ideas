#!/usr/bin/env python3
"""Create a daily AI agent idea markdown file from local inputs.

This script is intentionally LLM-provider agnostic. It accepts structured input
from flags or a JSON file, then renders the repository's daily idea format.
Future automation can call an LLM, save its response as JSON, and pass it to
this script without storing API keys or provider code in the repository.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from string import Template
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = REPO_ROOT / "templates" / "daily_idea.md.tmpl"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "ideas"
SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Convert a title to a stable lower-kebab-case slug."""
    slug = SLUG_RE.sub("-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def parse_iso_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"{value!r} is not a valid ISO date; expected YYYY-MM-DD"
        ) from exc


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("input JSON must contain an object at the top level")
    return data


def merged_data(args: argparse.Namespace) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if args.from_json:
        data.update(load_json(args.from_json))

    explicit = {
        "date": args.date.isoformat() if args.date else None,
        "title": args.title,
        "slug": args.slug,
        "concept": args.concept,
        "monetization": args.monetization or None,
        "execution_steps": args.execution_step or None,
        "status": args.status,
    }
    data.update({key: value for key, value in explicit.items() if value is not None})

    required = ["date", "title", "concept"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")

    data.setdefault("slug", slugify(str(data["title"])))
    data.setdefault("monetization", ["Define pricing and distribution after validation."])
    data.setdefault("execution_steps", ["Validate demand", "Build a small MVP", "Launch and collect feedback"])
    data.setdefault("status", "Drafted by automation scaffold; review before publishing.")

    if not isinstance(data["monetization"], list) or not all(
        isinstance(item, str) for item in data["monetization"]
    ):
        raise ValueError("monetization must be a list of strings")
    if not isinstance(data["execution_steps"], list) or not all(
        isinstance(item, str) for item in data["execution_steps"]
    ):
        raise ValueError("execution_steps must be a list of strings")

    idea_date = parse_iso_date(str(data["date"]))
    data["display_date"] = f"{idea_date:%B} {idea_date.day}, {idea_date:%Y}"
    return data


def render(template_path: Path, data: dict[str, Any]) -> str:
    template = Template(template_path.read_text(encoding="utf-8"))
    return template.substitute(
        date=data["display_date"],
        title=data["title"],
        concept=data["concept"],
        monetization=bullet_list(data["monetization"]),
        execution_steps=numbered_list(data["execution_steps"]),
        status=data["status"],
    ).rstrip() + "\n"


def output_path(output_dir: Path, data: dict[str, Any]) -> Path:
    return output_dir / f"{data['date']}-{data['slug']}.md"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render one daily AI agent idea markdown file from structured input."
    )
    parser.add_argument("--from-json", type=Path, help="Path to JSON idea payload.")
    parser.add_argument("--date", type=parse_iso_date, help="Idea date, YYYY-MM-DD.")
    parser.add_argument("--title", help="Idea title without the 'Idea:' prefix.")
    parser.add_argument("--slug", help="Optional filename slug; defaults to slugified title.")
    parser.add_argument("--concept", help="Concept paragraph.")
    parser.add_argument(
        "--monetization",
        action="append",
        default=[],
        help="Monetization bullet. Repeat for multiple bullets.",
    )
    parser.add_argument(
        "--execution-step",
        action="append",
        default=[],
        help="Execution step. Repeat for multiple ordered steps.",
    )
    parser.add_argument(
        "--status",
        default=None,
        help="Status line; defaults to a review reminder.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help=f"Template path. Default: {DEFAULT_TEMPLATE}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print rendered markdown and target path without writing a file.",
    )
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        help="Allow replacing an existing idea file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        data = merged_data(args)
        rendered = render(args.template, data)
        target = output_path(args.output_dir, data)
        if args.dry_run:
            print(f"Target: {target}")
            print(rendered, end="")
            return 0

        if target.exists() and not args.allow_overwrite:
            raise FileExistsError(
                f"{target} already exists; pass --allow-overwrite to replace it"
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        print(f"Created {target}")
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI should print clean errors.
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
