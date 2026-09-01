# Idea assessment rubric

Every idea in `ideas/` eventually gets exactly one assessment in `assessments/<slug>.md`.
An assessment answers four questions in a machine-comparable way:

1. **Is it viable?** Will anyone pay for it?
2. **Can a solo builder ship it?** Is the MVP actually reachable?
3. **What does it cost to stand up?** Money and days, not vibes.
4. **What is the plan?** Tools, and a concrete first build sequence.

The scoring is deliberately deterministic: a human (or agent) supplies ten 0-5 judgements
plus three cost estimates, and `scripts/rank_ideas.py` computes every derived number.
Nobody hand-writes a priority score. If two people disagree, they disagree about a single
0-5 axis, which is a conversation you can actually have.

## Axis A: viability (0-25)

How much money is realistically on the other side of this idea.

| Field | 0 | 3 | 5 |
| --- | --- | --- | --- |
| `pain_intensity` | mild curiosity | recurring friction people complain about | mission-critical, costs them money today |
| `buyer_quality` | hobbyists with no budget | freelancers / solo operators | SMBs or teams with a real software line item |
| `reachability` | buyers are scattered and anonymous | findable in niche communities | concentrated in channels a solo dev can work for free |
| `monetization_clarity` | no obvious way to charge | plausible price, unproven | comparable products already charge this, openly |
| `differentiation` | saturated, incumbents are good | a few players, gaps exist | no credible solution for this exact buyer |

`viability_score = sum(axes) * 4` → 0-100.

## Axis B: buildability (0-25)

How likely a one-person team is to actually get this in front of a paying user.

| Field | 0 | 3 | 5 |
| --- | --- | --- | --- |
| `mvp_simplicity` | needs novel research or heavy infra | standard CRUD plus one integration | scriptable in a weekend, no-code viable |
| `data_access` | data is gated behind partnerships or ToS-hostile scraping | public APIs with rate limits | open APIs or user-supplied data |
| `ai_fit` | current models fail the core task | models help but need heavy guardrails | the core task is exactly what current models are good at |
| `low_maintenance` | brittle scrapers and per-customer babysitting | some upkeep per integration | set-and-forget once shipped |
| `low_compliance_risk` | regulated: health, legal advice, money movement, minors | PII handling, standard contracts | no sensitive data, no regulated advice |

`buildability_score = sum(axes) * 4` → 0-100.

Note the last two axes are phrased so that **higher is always better**. Do not invert them.

## Axis C: cost to stand up

Three raw estimates, not scores:

| Field | Meaning |
| --- | --- |
| `setup_cost_usd` | one-off out-of-pocket dollars to reach the first paying customer: paid APIs, seat licences, data, design, ads for the first test |
| `monthly_cost_usd` | recurring infra and API spend at roughly ten customers |
| `time_to_mvp_days` | solo builder-days of focused work to a demoable MVP — calendar days, assuming this is the only project |

These collapse into a single index and a multiplier:

```
cost_index = setup_cost_usd / 1000 + monthly_cost_usd / 100 + time_to_mvp_days / 7
```

Read it as "thousands of dollars up front, plus hundreds per month, plus weeks of work."

| `cost_index` | band | multiplier |
| --- | --- | --- |
| ≤ 3 | `lean` | 1.00 |
| ≤ 6 | `moderate` | 0.85 |
| ≤ 12 | `heavy` | 0.65 |
| > 12 | `capital-intensive` | 0.45 |

## Priority

```
priority_score = round(viability_score * buildability_score / 100 * cost_multiplier)
```

The multiplication is the whole point, and it is inherited from the repo's existing
scanner ranking model (`src/scanner/scoring.py`): an idea that is lucrative but unbuildable
and an idea that is trivial but worthless both collapse toward zero. Only ideas that are
good on **both** axes survive, and the cost multiplier then discounts the ones that need
real capital to start.

| `priority_score` | band | meaning |
| --- | --- | --- |
| ≥ 60 | `build-next` | start this now |
| 45-59 | `queued` | good, but something else is better |
| 30-44 | `revisit` | needs a sharper wedge or cheaper path before it competes |
| < 30 | `park` | do not spend days here |

Ties break on `viability_score`, then on the older idea date — the queue stays FIFO
so nothing rots at the bottom forever.

## Narrative sections

Scores rank ideas. The prose is what you actually execute from, so every assessment must carry:

- **Verdict** — two or three sentences: build it, or don't, and why.
- **Tools needed** — concrete named services and libraries, split into *build* and *run*, each with its real price. "An LLM" is not a tool; "Anthropic API, ~$0.02/report" is.
- **Development plan** — numbered phases with a day budget per phase, ending at a demoable MVP. The first phase must be something that can be done without writing product code.
- **Kill criteria** — the observation that would make you stop. If you cannot name one, the idea is not concrete enough to score.

## Fields

Frontmatter for `assessments/<slug>.md`. `slug` must match both the filename stem and an
existing `ideas/<slug>.md`.

```yaml
---
slug: 2026-05-14-real-estate-digital-plumber
idea_title: AI Automation Digital Plumber Service for Small Real Estate Agents
assessed_on: 2026-09-01
assessed_by: claude
pain_intensity: 4
buyer_quality: 4
reachability: 4
monetization_clarity: 4
differentiation: 3
mvp_simplicity: 4
data_access: 3
ai_fit: 4
low_maintenance: 2
low_compliance_risk: 4
setup_cost_usd: 300
monthly_cost_usd: 120
time_to_mvp_days: 10
---
```

Everything else — `viability_score`, `buildability_score`, `cost_index`, `cost_band`,
`cost_multiplier`, `priority_score`, `priority_band`, rank — is computed and written into
`RANKING.md` by the ranker. Never hand-edit `RANKING.md`.

## Commands

```bash
python3 scripts/rank_ideas.py            # regenerate RANKING.md
python3 scripts/rank_ideas.py --check    # CI: assessments valid and RANKING.md current
python3 scripts/rank_ideas.py --next     # print the oldest idea with no assessment
python3 scripts/rank_ideas.py --json     # machine-readable ranking
```
