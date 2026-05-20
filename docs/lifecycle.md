# Daily idea lifecycle

This repository keeps a lightweight trail from raw idea to validated project. The goal is not heavy process; it is to make each daily idea easy for a fresh contributor or future agent to understand, validate, and execute.

## 1. Capture

Create `ideas/YYYY-MM-DD-short-slug.md` from `templates/daily-idea.md`.

Required outputs:

- Normalized frontmatter using `templates/idea-metadata.yaml`.
- A concise concept, target user, monetization hypothesis, validation plan, and first execution step.
- Status set to `draft` or `ready`.

Verification:

```bash
python3 scripts/generate_index.py
python3 scripts/generate_index.py --check
```

## 2. Normalize

Before an idea is considered ready, make sure the metadata is complete and the body is scannable.

Checklist:

- Filename and `slug` match exactly.
- `date` uses `YYYY-MM-DD`.
- `status` and `effort` use allowed values from `docs/idea-schema.md`.
- `summary` names the user, value, and output.
- Existing ideas stay in `ideas/`; do not overwrite or delete them when adding new structure.

## 3. Validate

When an idea moves to `validating`, copy `templates/validation-plan.md` into the relevant issue, planning doc, or future `validation/` folder and fill it out before running tests.

Recommended validation tasks:

- Define the riskiest assumption.
- Identify a small target audience sample.
- Run outreach, a landing-page test, a demo, or a concierge offer.
- Record exact positive signals, objections, and disqualifying evidence.
- Decide whether to build, revise, or archive.

## 4. Execute

When validation justifies building, copy `templates/execution-log.md` into the relevant issue, planning doc, or future `execution/` folder.

Execution logs should capture:

- The smallest useful deliverable.
- Manual operator steps versus automation candidates.
- Milestones and verification commands.
- Risks, blockers, and launch notes.

## 5. Maintain the catalog

`INDEX.md` is generated, not hand-edited. After changing any file under `ideas/`, run:

```bash
python3 scripts/generate_index.py
```

Before opening a PR, run:

```bash
python3 scripts/generate_index.py --check
```

A passing check means every idea file has valid metadata and the catalog reflects the current ideas.
