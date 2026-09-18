---
title: Same-Week Golden-Set Eval Pack for Solo Agent Shops
date: 2026-09-18
status: ready
category: agent evaluation
tags: [agents, evals, qa, freelance, indie-hackers, developer-tools, services, b2b]
monetization: per-pack fees and weekly regression retainers
effort: small
slug: 2026-09-18-golden-set-eval-pack
summary: A one-person operator plus agents turns a week's traces and product spec into a 30-item cited golden set plus a one-pass regression so the solo can score the agent instead of trusting a demo.
---

# Same-Week Golden-Set Eval Pack for Solo Agent Shops

**Date:** September 18, 2026

## X signal (today)

X on 16-18 September 2026 is saying the leftover paid job is not another agent — it is scoring the one you already have.

- Suraj Sharma (@suraj_sharma14, 18 Sep): the money is a narrow job with a meter and a buyer who already pays. Item 3 on his list is an eval / QA contractor: most teams have traces, half have evals. Sell a 30-question golden set plus a weekly regression pass for one product. That is the side hustle that turns into a hire.
- AI automation (@aiautobusiness, 18 Sep): everyone wants to build an agent; nobody wants to learn what happens when it retrieves the wrong data, calls the wrong tool, burns budget, or ships garbage. Evaluation is the leftover job.
- Miles Deutscher (@milesdeutscher, 16 Sep): validate with real buyers before you name the company; proof of work beats another wrapper.
- Adjacent: TermiX / A2A posts (14 Sep) want agents bidding on jobs with stake slashed on failure — that only works if someone wrote the acceptance tests.
- Grok / Aman Maqsood tier lists this week put automation agencies and digital products above generic chatbots. A golden set is the productized version of "does this workflow still work."

This catalog already owns work receipts for one computer-use run (2026-09-04), exception + cost control (2026-09-15), session handoff (2026-09-17), and close-the-loop last-mile audits (2026-09-18). It does not own a *same-week golden-set eval pack* that turns traces into a reusable 30-item test the owner can re-run.

## Concept

Sell a **same-week golden-set eval pack** when a solo builder, tiny agency, or 1-5 person product team has an agent or RAG workflow in production and no written test of "good."

The customer uploads or exports:

- 20-80 traces (success + failure) from one product or one workflow
- the current spec, SOP, or prompt file
- optional: support tickets, known-bad answers, one 8-minute voice note on "what a pass looks like"

Agents plus one human operator return within 48 hours:

1. A 30-item golden set: input, expected behavior, pass/fail rubric, and source trace id.
2. A first-pass score of the current agent against that set (cited, not vibes).
3. A slice report: the five failures that matter (wrong retrieve, wrong tool, invented cite, scope leak, cost blowup).
4. Three fixes only: one rubric tweak, one retrieval/chunk rule, or one human gate. Each with a 7-day re-run.
5. A "do not add another agent" list.
6. A source appendix. No invented accuracy percentages.

This is **not** an eval SaaS platform, **not** a red-team firm, and **not** a rebuild of their harness. It is a productized QA pack they can re-run next week.

## Target user

- Primary buyer: EU/UK/US indie hackers, solo agent shops, and tiny product teams shipping one workflow to paying users, spending $50-800/month on models.
- Urgent pain: the demo looks great, a client just got a wrong answer, and there is no file that says what "correct" means.
- Existing workaround: scroll traces, ask ChatGPT if the answer "seems fine," or hire a labeling platform they will abandon.

## Why this works

- Market signal: today's X feed named eval as the paid leftover. Platforms exist for raw labeling. Almost nobody sells a 48-hour, one-product golden set with a first score attached.
- Agent advantage: cluster traces, draft rubrics, refuse to treat a confident answer as a pass, keep the set to 30 items a human can read.
- Solo-operator advantage: one person who has shipped client work can write a pass condition. Judgment about "this would get us fired" is the product; the model is the clerk.

## Monetization

- Primary model: per-pack service.
- First price test: 179 EUR / 179 USD for one workflow, 30 items, and one scored pass; 249 if they include tool-call traces + retrieval dumps.
- Upsell: 99 for a weekly 30-item regression pass; 399/month retainer (one new slice + four regressions); 59 add-on to turn three failures into paste-ready eval cases in their harness format (JSONL / LangSmith / Braintrust / plain markdown).
- Fun / public variant: publish one synthetic bakery-booking golden set (30 items, 11 fails on a naive RAG) as X marketing. Never publish a real client trace.

## Validation plan

1. Riskiest assumption: a solo will pay ~179 for 30 cited tests instead of writing five examples themselves.
2. Demand test: post the synthetic bakery set on X and in 3 builder rooms on 18-20 Sep. DM 25 people who posted "agent shipped garbage," "no evals," "traces but no tests," or Suraj's thread. Offer the first 5 packs at 129 / 48h SLA.
3. Success bar: 5 serious replies and 2 paid packs in 14 days. Kill if 25 outbound touches produce zero deposits.

## Execution plan (one person + agents)

**Agent 1 — Intake.** Accept zip/JSONL/CSV/PDF/PNG/voice. Detect one product only. Refuse to merge two agents in one pack.

**Agent 2 — Trace miner.** Cluster traces into failure modes. Pull candidate items. Flag PII.

**Agent 3 — Rubric writer.** For each of 30 items: input, expected, pass/fail, source id. No item without a source.

**Agent 4 — First-pass scorer.** Run or simulate the current spec against the set. Tag fail reasons. Never invent a percentage from three examples.

**Human operator.** Kill cute architecture advice, drop client names from the public sample path, export PDF + Markdown + JSONL. The model does not change production prompts and does not press deploy.

Stack to start: coding agents, one LLM, Stripe Payment Link, a mailbox. Exports only in week one; no live prod access.

## First 7-day action plan

1. Write a default rubric standard (retrieve, tool, cite, scope, cost).
2. Build one public sample pack from a synthetic bakery-booking agent.
3. Publish sample + prices + "we do not deploy your prompt" disclaimer on a one-pager and X.
4. Send 25 outbound notes to recent eval / garbage-agent / traces-no-tests posts.
5. Run two paid pilots.
6. Time human review. Target under 50 minutes after job two.
7. Keep or kill.

## Risks and mitigations

- Fake accuracy: if traces do not cover a mode, mark `not-in-record`. Do not invent 94%.
- Confidential traces: isolated processing, redaction pass, delete after 30 days unless they opt into the retainer.
- Overlap with work receipts: that pack explains one computer-use run. This pack is a reusable test set. Route single-run buyers to 2026-09-04.
- Overlap with exception-control: that pack reads failures and model bills this week. This pack writes the test they re-run next week. Sell both; do not merge the files.
- Overlap with close-the-loop: that pack asks whether the last mile fired. This pack asks whether the answer was correct when it fired. Different question.
- Scope creep into building their eval platform: 30 items, three fixes, one export format. Stop.

## Open questions

- [ ] Is the first buyer a RAG support bot or a computer-use booking agent?
- [ ] Should week one refuse packs with fewer than 15 real traces?
- [ ] Is JSONL + Markdown enough, or do they want a LangSmith upload?

## Success metrics

- 1 public sample pack this week.
- 25 outbound touches.
- 2 paid packs.
- Human review under 50 minutes on a 30-item set.

**Status:** Execution-ready brief for a productized golden-set eval desk.
