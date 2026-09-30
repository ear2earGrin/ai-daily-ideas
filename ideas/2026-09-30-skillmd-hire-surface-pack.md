---
title: Same-Week SKILL.md Hire-Surface Pack for Solo Shops
date: 2026-09-30
status: ready
category: agent marketplace operations
tags: [agents, freelance, indie-hackers, small-business, skill-md, marketplace, x402, near, bounties, services, b2b]
monetization: per-pack fees and monthly retainers
effort: small
slug: 2026-09-30-skillmd-hire-surface-pack
summary: A one-person operator plus agents turns one paid job a solo already does into a cited SKILL.md hire surface so other agents can discover, price, and call the work instead of DMing the owner.
---

# Same-Week SKILL.md Hire-Surface Pack for Solo Shops

**Date:** September 30, 2026

## X signal (today)

X on 24-30 September 2026 is arguing that **agents are already hunting paid work, and the missing artifact is a machine-readable job menu — not another landing page.**

- Suryansh Tiwari (@Suryanshti777, 26 Sep): every product blowing up is one boring job someone stopped doing by hand. The leftover market is the dentist front desk, the freight inbox, the 3-person firm that will never buy Harvey. Pick one job. Write down where the big tools break.
- Max Faingezicht (@maxcr, 27 Sep): basedagents.ai started as identity, became a task marketplace; agents are finding it organically and are "desperate for USDC bounties."
- Vadim (@zacodil, 30 Sep): Near Social 2.0 shipped with a SKILL.md so AI agents can read and post directly. The social graph is now an agent I/O surface.
- Adjacent this week: Mastercard Agent Pay / Visa agent protocol / x402 chatter; AITOPIA and ALNO pitching "publish an agent, take a cut"; one-person AI agencies documenting infra so the playbook itself becomes SaaS.
- The catalog already owns agent hire listings (2026-09-06), agent-payable tool listings (2026-09-16), buyer-agent visibility / llms.txt (2026-09-24), and skill harvest from existing work (2026-09-19). It does not own a *same-week SKILL.md hire surface*: one job the solo already sells, written so a stranger agent can call it this week without a sales call.

## Concept

Sell a **same-week SKILL.md hire-surface pack** when a solopreneur, freelancer, or 1-5 person shop already does one repeatable paid job (VAT packet, review reply, quote revival, clip farm, blast-radius map) and wants other agents — or bounty boards — to hire that job without a human pitch deck.

The customer uploads or points at:

- the one job they want hired this week (name, price they already charge humans, typical inputs, typical output file)
- 2-5 anonymized examples of a finished job
- how they take money today (Stripe link, invoice, USDC, "I DM a price")
- hard no's (what the agent must never invent, never publish, never spend)

Agents plus one human operator return within 48 hours:

1. A SKILL.md: job name, when to call it, required inputs, output contract, refusal cases, and a one-paragraph human summary.
2. An input schema card (JSON or Markdown table): fields, examples, max file size, PII rules.
3. A price and SLA card: human price, agent price if different, turnaround, revision cap, what "done" means.
4. A sample call + sample receipt from one anonymized past job.
5. A publish checklist: where the file can live this week (repo root, Near Social, bounty board bio, llms.txt pointer) without leaking client names.
6. A source appendix. No claim that agents will find them tomorrow.

This is **not** a new marketplace, **not** an MCP server build, and **not** a promise of inbound agent traffic. It is a productized desk for *one shop, one job, one week*, so "agents are hiring" becomes a file another agent can actually parse.

## Target user

- Primary buyer: US/EU/UK freelancers and tiny agencies who already sell a repeatable pack and keep explaining it in DMs.
- Urgent pain: bounty boards and agent social graphs want SKILL.md / machine menus; the owner's site is a vibe paragraph.
- Existing workaround: paste a Notion doc into ChatGPT and hope an agent reads the website.

## Why this works

- Market signal: this week's feed named one-job products, USDC-hungry agents, and a live SKILL.md on a public social network in the same week. Existing catalog packs list a tool, harvest skills from transcripts, or add llms.txt. They do not freeze *this week's one paid job* into a call contract.
- Agent advantage: turn finished examples into a strict input/output spec; refuse to invent capabilities the examples do not show.
- Solo-operator advantage: one person who has delivered the job five times can mark price and refusals in ten minutes. Judgment about what not to sell is the product; the model is the clerk.

## Monetization

- Primary model: per-pack service.
- First price test: 129 USD / 129 EUR for one job, one SKILL.md, one schema card, one sample receipt; 199 if they want a second job and a publish checklist for two surfaces.
- Upsell: 49 rush (24h); 79 rewrite after they change price or refusals; 299/month retainer (weekly diff if the job changes); 39 add-on plain-language landing blurb that matches the SKILL.md.
- Fun / public variant: publish one synthetic pack ("anonymized review-reply desk, 49 USD, 24h, no invented facts"). Never publish live client files or payment keys.

## Validation plan

1. Riskiest assumption: a solo will pay ~129 for a SKILL.md instead of writing a README themselves.
2. Demand test: post one anonymized sample pack on X and in 3 indie-hacker / agent-marketplace rooms on 30 Sep-2 Oct. DM 25 people who posted about basedagents bounties, Near Social SKILL.md, x402, or "agents will hire you." Offer the first 5 packs at 79 / 48h SLA.
3. Success bar: 5 serious replies and 2 paid packs in 14 days. Kill if 25 outbound touches produce zero deposits.

## Execution plan (one person + agents)

**Agent 1 — Intake.** Accept job name, price, examples. Detect one job only. Refuse live API keys and raw client inboxes.

**Agent 2 — Contract writer.** Draft SKILL.md from examples. Every capability must cite an example or be marked `draft-unverified`.

**Agent 3 — Schema + price card.** Inputs, outputs, SLA, refusals. Flag underspecified money or publish steps.

**Agent 4 — Pack writer.** SKILL.md, schema, price card, sample call/receipt, publish checklist, appendix.

**Human operator.** Kill invented capabilities, strip client names, export Markdown + PDF. The model does not post to Near Social or list a bounty unless the owner clicks publish.

Stack to start: one LLM, Stripe Payment Link, a mailbox. Examples only in week one. No custom marketplace.

## First 7-day action plan

1. Write a default SKILL.md standard (job, inputs, outputs, refusals, price).
2. Build one public sample pack from a synthetic review-reply or VAT-packet job.
3. Publish sample + prices + "we do not list you on a board" disclaimer on a one-pager and X.
4. Send 25 outbound notes to bounty / SKILL.md / one-job-agent posts.
5. Run two paid pilots.
6. Time human review. Target under 35 minutes after job two.
7. Keep or kill.

## Risks and mitigations

- Acting as their marketplace: never take a cut of agent-hired jobs in week one. Deliver the file. They publish.
- Overlap with hire listing (2026-09-06): that pack is identity + listing copy for a person/agent. This pack is the *callable job contract*.
- Overlap with payable tool listing (2026-09-16): that pack is an API/tool with metering. This pack is a human-fulfilled job wrapped for agents.
- Overlap with buyer-agent visibility (2026-09-24): that pack is llms.txt / MCP discoverability of a shop. This pack is one job's call surface.
- Overlap with skill harvest (2026-09-19): that pack extracts skills from past work. This pack publishes one skill as a hire menu.
- Client examples leaking: anonymize before processing. Halt if live secrets appear.
- Vapor capabilities: if examples do not show a step, it does not go in SKILL.md.

## Open questions

- [ ] Is the first buyer a pack-seller from this repo's own catalog, or a local shop that wants agents to book a single service?
- [ ] Should week one refuse jobs that move money or post in the customer's name?
- [ ] Do they want the SKILL.md more than the price/SLA card?

## Success metrics

- 1 public sample pack this week.
- 25 outbound touches.
- 2 paid packs.
- Human review under 35 minutes on a one-job week.

**Status:** Execution-ready brief for a productized SKILL.md hire-surface desk.
