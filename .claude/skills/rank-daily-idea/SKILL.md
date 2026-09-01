---
name: rank-daily-idea
description: Assess and rank the oldest unassessed idea in ideas/. Use when running the daily idea-ranking routine, when asked to assess or score an idea in this repo, or when RANKING.md needs refreshing after new ideas land.
---

# Rank the next daily idea

Work through the idea backlog one item per run, oldest first, producing a scored
assessment that slots into `RANKING.md`. The scoring model is
`docs/idea-assessment-rubric.md` — read it before scoring anything.

## Procedure

### 1. Find the target

```bash
python3 scripts/rank_ideas.py --next
```

If it prints `All ideas assessed.`, there is nothing to do. Refresh `RANKING.md`, confirm
`--check` passes, and stop **without** opening a PR or committing. An empty run is a
successful run; do not invent work to fill it.

Otherwise it prints the slug, title, date, file path, and whether the file is a raw drop.

### 2. Read the idea, and only the idea

Read the idea file in full. Also read one or two existing assessments in `assessments/`
to match depth and tone. Do not read the whole repo.

If the file is a **raw drop** (no frontmatter — this is how Grok's daily cron writes
them), add normalized frontmatter per `docs/idea-schema.md` before assessing. Keep the
original body byte-for-byte: it is the source record. Set `status: draft`, since a raw
drop has not been through the lifecycle.

If the idea is a **stub** — no target customer, no monetization, a placeholder body — still
assess it, but open the assessment with a blockquote saying the source is incomplete and
the scores are low-confidence, and make "rewrite the idea file" the first phase of the
development plan. Do not silently invent a business the author never described.

### 3. Score the ten axes

Copy `templates/idea-assessment.md` to `assessments/<slug>.md` and fill in the frontmatter.

Score honestly. The rubric's value is entirely in its calibration, so:

- **Anchor to the band descriptions** in the rubric, not to how you feel about the idea.
- **`differentiation` and `low_compliance_risk` are where optimism does the most damage.**
  Before scoring differentiation, name the actual incumbents out loud. If you cannot name
  three, you have not thought about it. Before scoring compliance, name the specific
  regulation, not a vague worry.
- **Never adjust a score to reach a ranking you prefer.** If a favourite idea lands in
  `park`, that is the system working. Argue with it in the prose instead.
- **`low_maintenance` and `low_compliance_risk` are phrased so higher is better.** A
  high-risk idea scores *low*. This inversion is easy to get backwards; check it.

Estimate the three costs concretely, with real 2026 prices for named services. Setup is
one-off dollars to the *first paying customer*, not to a finished product. `monthly_cost_usd`
is infra and API spend at roughly ten customers. `time_to_mvp_days` assumes this is the
only project.

### 4. Write the prose

Scores rank; prose is what gets executed. Required sections are listed in the rubric.
Two things separate a useful assessment from a generated one:

- **Justify each axis with a specific fact**, not a restatement of the score. "Buyers
  already pay $69/mo for Follow Up Boss" is useful; "buyers have good budget" is not.
- **The development plan's Phase 0 must not involve writing product code.** Every idea in
  this catalog can be tested with a landing page, a hand-made artifact, or twenty emails
  first. If you cannot design that test, say so explicitly — it is a finding about the idea.

Name what you are guessing. An assessment that hides its uncertainty is worse than no
assessment, because it gets trusted.

### 5. Regenerate and verify

```bash
python3 scripts/generate_index.py     # only if you touched an idea file
python3 scripts/rank_ideas.py
python3 tests/run_tests.py
python3 scripts/generate_index.py --check
python3 scripts/rank_ideas.py --check
```

All must pass before you commit. Never hand-edit `RANKING.md` or `INDEX.md`.

### 6. Open one PR

Branch `claude/assess-<slug>`, one commit, then push and open a PR.

The PR body must include: where the idea landed in the ranking and why, the scores that
drove it, the setup cost and days to MVP, and — the part worth reading — **what changed
about the top of the ranking**, if anything. If the new idea displaced the leader, say so
in the first line. If it did not, say that too.

Keep the PR to one assessment. Assessing two ideas in one run makes the rankings harder to
argue with, and arguing with them is the point.
