# Daily idea automation

This repository now includes a local scaffold for adding one AI agent idea at a time without committing provider credentials or generated secrets.

## Files

- `scripts/add_daily_idea.py` renders a markdown idea file from flags or JSON.
- `templates/daily_idea.md.tmpl` defines the markdown structure used by the script.
- `templates/example_idea_payload.json` shows the JSON shape an LLM step can emit later.
- `.github/workflows/daily-idea.yml` is a disabled-by-default workflow stub for future scheduled automation.

## Add an idea locally

From the repository root:

```bash
python3 scripts/add_daily_idea.py \
  --date 2026-05-19 \
  --title "AI Agent-Powered Inbox Opportunity Scout" \
  --concept "An assistant that scans inbound messages and turns repeated pain points into validated micro-product ideas." \
  --monetization "Subscription for founders" \
  --monetization "Premium workspace integrations" \
  --execution-step "Connect one message source" \
  --execution-step "Cluster repeated customer pain points" \
  --execution-step "Generate a weekly opportunity brief"
```

The script writes to `ideas/YYYY-MM-DD-slug.md`. It refuses to overwrite an existing file unless `--allow-overwrite` is passed.

## Use JSON input

The JSON route is the intended seam for a future LLM integration:

```bash
python3 scripts/add_daily_idea.py --from-json templates/example_idea_payload.json --dry-run
```

Expected JSON fields:

```json
{
  "date": "2026-05-19",
  "title": "Idea title",
  "slug": "optional-custom-slug",
  "concept": "Concept paragraph",
  "monetization": ["Bullet one", "Bullet two"],
  "execution_steps": ["Step one", "Step two"],
  "status": "Status line"
}
```

Required fields are `date`, `title`, and `concept`. `monetization`, `execution_steps`, `status`, and `slug` have safe defaults.

## Wiring an LLM later

Keep the LLM step outside this repository or in GitHub Actions secrets. The recommended contract is:

1. Prompt the model to return only JSON matching `templates/example_idea_payload.json`.
2. Save that JSON to a temporary file, for example `/tmp/daily-idea.json`.
3. Run `python3 scripts/add_daily_idea.py --from-json /tmp/daily-idea.json`.
4. Review the generated markdown before committing.

Do not commit API keys, raw provider responses with credentials, or generated `.env` files.

## GitHub Actions stub

`.github/workflows/daily-idea.yml` only validates the scaffold by default. The scheduled job is documented but commented out so the repository does not start opening automated changes before credentials, review policy, and branch permissions are decided.

To enable later:

1. Add provider credentials as repository or organization secrets.
2. Add an LLM generation step that writes `/tmp/daily-idea.json`.
3. Run `scripts/add_daily_idea.py --from-json /tmp/daily-idea.json`.
4. Create a branch/PR with a reviewed action such as `peter-evans/create-pull-request`.

## Verification

Run:

```bash
python3 -m py_compile scripts/add_daily_idea.py
python3 scripts/add_daily_idea.py --from-json templates/example_idea_payload.json --dry-run
```
