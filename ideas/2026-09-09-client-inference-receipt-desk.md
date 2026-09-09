---
title: Client Inference Receipt Desk for Solo Agent Shops
date: 2026-09-09
status: ready
category: agency billing operations
tags: [agents, billing, inference, receipts, freelance, services, b2b]
monetization: per-pack fees and monthly retainers
effort: small
slug: 2026-09-09-client-inference-receipt-desk
summary: A one-person operator plus agents turns a week's model invoices and agent traces into cited per-client inference receipts so the solo can pass through AI spend instead of eating the bill.
---

# Client Inference Receipt Desk for Solo Agent Shops

**Date:** September 9, 2026

## X signal (today)

X and GitHub on 1-9 September 2026 keep repeating the same cost problem: **personal and client agents are cheap to demo and expensive to run for real**.

- signüll (@signulll, 1 Sep): personal agents will need consumer pricing and endless inference; labs want enterprise margins. The gap shows up as a solo's OpenAI / Anthropic / gateway invoice with no client split.
- GitHub trending 8-9 Sep: agent harnesses, skills catalogs (mattpocock/skills, openai/skills, DeepSeek Harness), and model gateways (experiential, OmniRoute). More runs, more traces, still one lump invoice.
- Coin Bureau / Virtuals threads: agents with wallets and payment cards. Buyers will ask what the agent spent. Sellers have a CSV, not a receipt.
- Adjacent catalog items: agent work receipt (2026-09-04) proves *what the agent did*. Late-invoice chase (2026-09-07) collects *human invoices*. Agent hire listing (2026-09-06) packages the agent for sale. None of them emit a cited *per-client token and tool-cost receipt* the buyer can attach to a job.

Cheap multi-model routing + a weekly lump bill = a productized cost-clerk, not another usage dashboard SaaS.

## Concept

Sell a **weekly client inference receipt pack** for one shop that already runs agents on client work.

The customer uploads:

- last 7 days of provider invoices or usage CSVs (OpenAI, Anthropic, a gateway, local GPU notes)
- a job map: client name or code, job id, date range, which agent/skill ran
- optional: trace folders or run logs (computer-use traces, Codex/Claude Code session ids)
- a pass-through policy: markup %, what is billed vs eaten, currency, VAT note

Agents plus one human operator return within 24 hours:

1. A per-client table: tokens in/out, tool calls, estimated $ , markup, billable $ , confidence.
2. Unallocated spend bucket (personal experiments, failed retries the policy says to eat).
3. Three exception notes: runaway loop, duplicate run, provider refund pending.
4. One paste-ready line item block per client for the human invoice.
5. A source appendix. Every dollar cites invoice row id + run id or `not-in-record`.

This is **not** a live cost dashboard, **not** an auto-charger, and **not** a crypto wallet. It is a clerk that turns a lump AI bill into attachable receipts.

## Target user

- Primary buyer: EU/UK/US solo or 1-3 person shops selling agent work, reports, or coding-agent hours who already invoice humans and now eat model spend.
- Urgent pain: Friday invoice to Client A hides Tuesday's 40-dollar retry storm that belonged to Client B.
- Existing workaround: spreadsheet guesses, or "AI fee" as a vague 10% line nobody can defend.

## Why this works

- Market signal: builders are shipping more harnesses and skills; invoices are still one line. The first loop is allocation, not another router.
- Agent advantage: parse CSVs, join traces to jobs, refuse to invent a client when the run has no job tag.
- Solo-operator advantage: the human already knows which jobs were internal R&D. Judgment is the product; the model is the clerk.

## Monetization

- Primary model: per-pack service on a weekly cadence.
- First price test: 89 EUR / 89 USD for up to 8 clients + 3 providers; 149 if they add raw traces. 24-hour SLA after files land.
- Upsell: 39 standing policy card (markup, eat-vs-bill rules); 279/month retainer for four weekly packs; 49 "dispute pack" if a client rejects a line.
- Fun / public variant: publish one synthetic week (fake clients + real public pricing tables) as X marketing. No real invoices.

## Validation plan

1. Riskiest assumption: a solo will pay ~89 to split a bill they could guess in a spreadsheet.
2. Demand test: post one anonymized sample pack on X. DM 25 people who posted agent invoices, "token bill," gateway costs, or "how do I charge for agents." Offer the first 5 packs at 49 / 24h.
3. Success bar: 5 serious replies and 2 paid packs in 14 days. Kill if 25 outbound touches produce zero deposits.

## Execution plan (one person + agents)

**Agent 1 — Intake.** Normalize invoices and the job map. Extract provider, date, model, tokens, $ . Refuse to invent a fourth provider.

**Agent 2 — Joiner.** Match runs to jobs by id, folder name, or time window. Mark unmatched as unallocated.

**Agent 3 — Policy.** Apply markup and eat-vs-bill rules. Flag runaway loops.

**Agent 4 — Pack drafter.** Fill tables and invoice line blocks. Every cell cites a source id or `not-in-record`. Refuse to charge any card.

**Human operator.** Kill double-counts, drop personal R&D into unallocated, export PDF + markdown. The model does not send the client invoice.

Stack to start: coding agents, CSV parsers, one LLM, Stripe Payment Link, a mailbox. No product UI until the fifth paid job. No auto-billing clients.

## First 7-day action plan

1. Write an allocation standard (job tag required vs time-window guess vs unallocated).
2. Build one public sample pack from synthetic jobs + public price tables.
3. Publish sample + prices on a one-page site and X.
4. Send 25 outbound notes to recent token-bill / agent-pricing posts.
5. Run two paid pilots.
6. Time human review. Target under 30 minutes after job two.
7. Keep or kill.

## Risks and mitigations

- Privacy: treat invoices as confidential. No training on client names. Redact in public samples.
- False allocation: if a run has no job tag, it stays unallocated. Do not invent Client A.
- Overlap with work receipt desk: if they want *what the agent clicked*, send them to 2026-09-04. This pack is *what it cost*.
- Provider gaps: local GPU hours need a simple hourly note from the owner; do not invent a cloud rate.
- Tax: pack is an attachment, not tax advice. Owner keeps their accountant.

## Open questions

- [ ] Is the first buyer an agent-services freelancer or a small studio with a gateway invoice?
- [ ] Should week one skip traces and only split provider CSVs?
- [ ] Is a standing policy card required before the first paid pack?

## Success metrics

- 1 public sample pack this week.
- 25 outbound touches.
- 2 paid packs.
- Human review under 30 minutes on an 8-client week.

**Status:** Execution-ready brief for a productized inference-receipt desk.
