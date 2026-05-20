# Idea metadata schema

Each idea lives in `ideas/YYYY-MM-DD-short-slug.md` and starts with a YAML-style frontmatter block. The repository tooling intentionally supports a small, dependency-free subset of YAML: `key: value` scalars and inline lists like `[agent, saas]`.

## Required fields

| Field | Example | Notes |
| --- | --- | --- |
| `title` | `Niche Legacy Story Weaver` | Human-readable idea name. |
| `date` | `2026-05-17` | ISO date; should match the leading date in the filename. |
| `status` | `ready` | One of `draft`, `ready`, `validating`, `building`, `launched`, `archived`. |
| `category` | `consumer memory` | Short market or domain label. |
| `tags` | `[agents, content, b2c]` | Inline list used for filtering and discovery. |
| `monetization` | `project fees` | Primary business model. |
| `effort` | `medium` | One of `small`, `medium`, `large`. |
| `slug` | `2026-05-17-niche-legacy-story-weaver` | Must match the filename stem. |
| `summary` | `AI agents turn family artifacts into books...` | One-sentence catalog summary. |

## Template

```markdown
---
title: Example Idea
date: 2026-05-20
status: draft
category: example
tags: [agents, workflow]
monetization: subscription
effort: small
slug: 2026-05-20-example-idea
summary: One sentence describing the user, value, and output.
---

# Example Idea

## Concept
...
```

## Validation

Run the repeatable catalog check before committing:

```bash
python3 scripts/generate_index.py --check
```

If the check reports that `INDEX.md` is out of date, regenerate it:

```bash
python3 scripts/generate_index.py
```
