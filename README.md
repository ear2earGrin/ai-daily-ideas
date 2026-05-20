# ai-daily-ideas

Daily AI agent project ideas for one-person teams — monetizable or fun.

## Repository workflow

1. Add one idea as `ideas/YYYY-MM-DD-short-slug.md`.
2. Start the file with the metadata block described in `docs/idea-schema.md`.
3. Write the body in regular Markdown using sections like Concept, Monetization, and Execution Steps.
4. Regenerate the catalog:

   ```bash
   python3 scripts/generate_index.py
   ```

5. Verify the catalog before committing:

   ```bash
   python3 scripts/generate_index.py --check
   ```

## Metadata convention

Every idea must include frontmatter fields for title, date, status, category, tags, monetization, effort, slug, and summary. This keeps the ideas easy to scan and lets the catalog be generated without hand-editing tables.

See `docs/idea-schema.md` for the full schema and a copy-paste template.

## Catalog

The generated catalog lives in `INDEX.md` and lists every idea by date, status, category, effort, monetization model, and tags.

## Current repeatable check

```bash
python3 scripts/generate_index.py --check
```
