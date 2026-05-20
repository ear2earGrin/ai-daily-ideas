# ai-daily-ideas

Daily AI agent project ideas for one-person teams — monetizable or fun.

## What lives here

- `ideas/` — one Markdown file per daily idea. Existing ideas stay here and should not be overwritten when adding new workflow structure.
- `templates/` — copy-paste starting points for new ideas, metadata, validation plans, and execution logs.
- `docs/idea-schema.md` — required normalized metadata fields and allowed values.
- `docs/lifecycle.md` — the capture → normalize → validate → execute workflow.
- `INDEX.md` — generated catalog of all ideas.

## Add a new daily idea

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
