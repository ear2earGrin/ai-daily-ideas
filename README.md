# ai-daily-ideas

Daily AI agent project ideas for one-person teams — monetizable or fun.

A repository of validated, evidence-backed AI agent project ideas that solo developers and small teams can build and monetize.

## What lives here

- `ideas/` — one Markdown file per daily idea. Existing ideas stay here and should not be overwritten when adding new workflow structure.
- `templates/` — copy-paste starting points for new ideas, metadata, validation plans, execution logs, and automation payloads.
- `docs/idea-schema.md` — required normalized metadata fields and allowed values.
- `docs/lifecycle.md` — the capture → normalize → validate → execute workflow.
- `docs/daily-idea-automation.md` — automation scaffold for adding ideas from CLI flags or JSON payloads.
- `docs/plans/market-problem-scanner.md` — plan for mining evidence-backed monetizable pain points from public sources.
- `INDEX.md` — generated catalog of all ideas.

## Current Ideas

Browse the `ideas/` directory for existing project ideas. Each idea includes:
- Problem statement
- Monetization strategy
- Execution steps
- Status

## Add a new daily idea

### Manual path

1. Pick a date and slug, then create `ideas/YYYY-MM-DD-short-slug.md` from the template:

   ```bash
   cp templates/daily-idea.md ideas/YYYY-MM-DD-short-slug.md
   ```

2. Fill in the frontmatter. The metadata block must include the required fields from `docs/idea-schema.md`:

   - `title`
   - `date`
   - `status`
   - `category`
   - `tags`
   - `monetization`
   - `effort`
   - `slug`
   - `summary`

3. Make sure the filename stem and `slug` match exactly.
4. Replace the placeholder body with a concise concept, target user, monetization hypothesis, validation plan, and first execution step.
5. Regenerate the catalog:

   ```bash
   python3 scripts/generate_index.py
   ```

6. Verify before committing:

   ```bash
   python3 scripts/generate_index.py --check
   ```

### Automation scaffold

Use `scripts/add_daily_idea.py` to render a new idea into `ideas/YYYY-MM-DD-slug.md` from CLI flags or a JSON payload:

```bash
python3 scripts/add_daily_idea.py --from-json templates/example_idea_payload.json --dry-run
```

See `docs/daily-idea-automation.md` for the full workflow, verification commands, and the GitHub Actions stub for future LLM wiring.

## Next Phase: Market Problem Scanner

We're building an automated pipeline to discover and validate new opportunities from public sources like Reddit, HackerNews, and web searches.

**See:** [docs/plans/market-problem-scanner.md](docs/plans/market-problem-scanner.md)

**Key features:**
- Automated discovery of repeated pain points
- Evidence-based validation, not guesswork
- Multi-agent workflow: local Qwen for extraction, Claude for strategy
- Scored opportunities: intensity, frequency, buyer quality, MVP simplicity
- Weekly reports with top 3-5 actionable ideas

### Running the Prototype

The scanner prototype is now available:

```bash
# Run scanner on sample fixtures (no API credentials needed)
python3 scripts/run_scanner.py

# Specify custom fixture and output directory
python3 scripts/run_scanner.py --fixture fixtures/custom.json --output reports/custom

# Persist findings to a local SQLite DB for dashboard review
python3 scripts/run_scanner.py --fixture fixtures/sample_pain_points.json --output reports --db data/scanner.sqlite

# Start the local dashboard on 127.0.0.1 only
python3 scripts/run_dashboard.py --db data/scanner.sqlite --host 127.0.0.1 --port 8765

# Then open:
# http://127.0.0.1:8765

# Run tests
python3 tests/run_tests.py
```

**Components:**
- `src/scanner/` — Core scanner modules (models, scoring, extraction, reporting)
- `fixtures/sample_pain_points.json` — Synthetic test data
- `scripts/run_scanner.py` — CLI entry point
- `scripts/run_dashboard.py` — local-only dashboard for reviewing stored findings, ranked opportunities, and cluster detail pages
- `src/scanner/sqlite_storage.py` — SQLite persistence for scan runs, pain points, clusters, ranking fields, statuses, and notes
- `tests/` — Unit tests for scanner components
- `reports/` — Generated opportunity reports

**Ranking model:**
- `profitability_score` estimates buyer urgency, budget, existing spend, frequency, reachability, revenue clarity, and workaround pain.
- `build_probability_score` estimates MVP simplicity, data/API access proxy, automation fit, competition gap, compliance risk, maintenance burden, and founder-fit default.
- `priority_score = profitability_score × build_probability_score`, which punishes sexy-but-hard ideas and easy-but-worthless ideas.
- Priority bands: `validate immediately` (≥900), `promising` (650-899), `keep watching` (400-649), `ignore` (<400).

**Current status:** Prototype v0.2.0 with heuristic extraction, SQLite dashboard storage, and opportunity ranking. Next steps: integrate local Qwen for LLM-based extraction, add real Reddit/HN collectors.

## Lifecycle

The workflow is intentionally lightweight:

1. Capture the idea in `ideas/` with normalized metadata.
2. Normalize the idea so the catalog and future agents can scan it consistently.
3. Validate demand or feasibility using `templates/validation-plan.md`.
4. Execute the smallest useful build using `templates/execution-log.md`.
5. Maintain `INDEX.md` with the generator instead of editing it by hand.

See `docs/lifecycle.md` for the detailed checklist.

## Metadata convention

Every idea must include frontmatter fields for title, date, status, category, tags, monetization, effort, slug, and summary. This keeps the ideas easy to scan and lets the catalog be generated without hand-editing tables.

See `docs/idea-schema.md` for the full schema and `templates/idea-metadata.yaml` for a copy-paste metadata block.

## Catalog

The generated catalog lives in `INDEX.md` and lists every idea by date, status, category, effort, monetization model, and tags.

## Current repeatable check

```bash
python3 scripts/generate_index.py --check
```

## Contributing

New ideas and improvements welcome. Open a PR with your suggestion.
