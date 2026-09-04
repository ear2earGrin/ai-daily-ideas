---
title: Agent Work Receipt Desk for Computer-Use Runs
date: 2026-09-04
status: ready
category: agent operations
tags: [agents, computer-use, audit, receipts, services, b2b]
monetization: per-run fees and monthly retainers
effort: small
slug: 2026-09-04-agent-work-receipt-desk
summary: A one-person operator plus agents turns a task brief and a computer-use trace into a cited work receipt so the buyer can see what the agent actually did, what was out of scope, and how to roll back.
---

# Agent Work Receipt Desk for Computer-Use Runs

**Date:** September 4, 2026

## X signal (today)

X on 4 September 2026 is arguing that **computer-use agents just became a headline product, and nobody is selling the paper that proves what they did.**

- OpenAI posted GPT-6 Astra: "Anything you can do on a computer, Astra can do for you. Fast." The clip is circulating next to claims that this is a defining AGI-threshold moment. The missing product is not another demo. It is a file a human will accept after the agent touched mail, CRM, files, or ads.
- Ahmed W. shipped an anti-gold-plating skill because his agents keep adding unrequested features and only report after they have already broken scope.
- Connor Jewiss (late Aug, still circulating): first personal agent that runs locally with no server-side data wins. That only works if the owner can later reconstruct the session.
- Cyril Lutterodt / Agents in the Wild: research + GTM agents that find VCs and first customers. The demo is cheap. The audit of "what did it email, scrape, or invent" is not.
- Adjacent: NewsCatcher launched a news product explicitly for agents; GenLayer / auto-research threads still treat *judgment of agent work* as unsolved.

This catalog already has human-job paper (playbook redline 09-02, deliverable verdict 09-03, live change-order 09-04). It does not have a receipt for *agent* computer use.

## Concept

Sell a **24-hour agent work receipt pack** after a computer-use or multi-tool agent run.

The customer uploads:

- the original task brief ("clean my inbox of newsletters", "update these 12 Shopify products", "find 50 leads and draft outreach")
- the agent trace: screenshots, HAR, browser-agent log, tool-call JSON, screen recording, or Astra/session export
- optional: before/after file dump, sent-mail folder, CRM changelog, git diff

Agents plus one human operator return:

1. A reconstructed intent: numbered allowed actions vs forbidden actions (send, delete, pay, publish).
2. A step ledger: each observed action tagged `in-scope / gold-plate / out-of-scope / unverified / harmful`.
3. A cited excerpt table: brief line next to log line, screenshot, or `not-in-record`.
4. A blast-radius page: accounts touched, messages sent, files changed, money moved.
5. A rollback checklist the owner can execute in 15 minutes.
6. A one-paragraph client note in plain language (not a SOC2 novel).

This is **not** a security audit firm and **not** an Astra competitor. It is a productized clerk that turns "the agent handled it" into evidence.

## Target user

- Primary buyer: solo founders, agencies, and 2-10 person shops who just let a computer-use agent touch a real account and now cannot explain the session to a client, a cofounder, or themselves.
- Urgent pain: the run "worked" in the demo sense, but three extra pages were published, two emails went out, or gold-plating burned tokens and reputation.
- Existing workaround: re-watch a 40-minute screen recording, trust the agent's self-report, or never use computer-use on a production account.

## Why this works

- Market signal: today's X feed made computer-use mainstream in one post. Gold-plating and unverifiable agent work are already the complaint underneath the hype.
- Agent advantage: parse long traces, screenshots, and tool JSON; refuse to invent clicks that are not in the record.
- Solo-operator advantage: one maker who has shipped agents can tell the difference between a useful extra and a scope break, and write a receipt a non-engineer will read.

## Monetization

- Primary model: per-run service.
- First price test: 89 EUR for traces under 30 minutes / one account; 169 EUR for multi-tool or multi-account runs; 249 EUR if money or outbound email is in the blast radius. 24-hour SLA.
- Upsell: 39 EUR rush (8h); 59 EUR "reply to the agent's self-report"; 29 EUR standing brief (allowed/forbidden action list); 279 EUR/month retainer for a studio running daily agent jobs.
- Fun / public variant: one synthetic Astra-style session + receipt published weekly on X. High shareability while the Astra clip is still circulating.

## Validation plan

1. Riskiest assumption: someone will pay 89-169 EUR after an agent run instead of skimming the log themselves or asking the same model to summarize.
2. Demand test: publish one anonymized sample receipt next to the Astra clip. DM 20 people who posted "I let the agent loose on my inbox/CRM/store." Offer the first 5 packs at 69 EUR / 24h.
3. Success bar: 5 serious replies and 2 paid packs in 14 days. Kill if 25 outbound touches produce zero deposits.

## Execution plan (one person + agents)

**Agent 1 — Intake.** Accept zip, JSONL tool logs, video, PDF screenshots. Detect run type (browser, desktop, email, store, code).

**Agent 2 — Brief parser.** Extract allowed actions, success criteria, and hard stops ("do not send", "do not delete", "do not pay").

**Agent 3 — Trace miner.** Turn logs and frames into a dated step list. Drop small talk and thinking tokens that are not actions.

**Agent 4 — Classifier.** Tag gold-plating vs required work. Never invent a click.

**Agent 5 — Pack drafter.** Fill ledger, blast-radius page, rollback checklist, owner note. Every cell cites a source id or `not-in-record`.

**Human operator.** Delete invented steps, mark real risk, keep tone sendable. The model does not log into the customer's accounts.

Stack to start: coding + vision agents, ffmpeg for recordings, one LLM, Stripe Payment Link, a mailbox. No product UI until the fifth paid job.

## First 7-day action plan

1. Write a default action standard (what counts as send, publish, delete, pay, gold-plate).
2. Build one public sample pack from a synthetic 12-minute browser-agent run.
3. Publish sample + prices on a one-page site and X while Astra is still trending.
4. Send 25 outbound notes to people posting computer-use wins and disasters.
5. Run two paid pilots.
6. Time human review. Target under 35 minutes after job two.
7. Keep or kill.

## Risks and mitigations

- Seeing secrets in traces: isolated processing, no training, delete after 14 days unless they opt in. Refuse password-bearing recordings if they cannot redact.
- Pretending to be a pentest or SOC2 audit: sell a *work receipt*, not an attestation.
- Incomplete traces: label packs "based on materials provided only." Offer a recapture script as an upsell, not as a claim of completeness.
- Overlap with the 09-03 verdict desk: if the fight is human freelancer vs client, send them there. This SKU is only for agent-operated sessions.

## Open questions

- [ ] Is the first buyer the founder who ran the agent, or the client who received mystery outbound from it?
- [ ] Should v1 require structured tool logs, or accept only screen recordings?
- [ ] Is email/CRM the first niche, or Shopify/admin busywork?

## Success metrics

- 1 public sample pack this week.
- 25 outbound touches.
- 2 paid receipts.
- Human review under 35 minutes on a standard browser-agent log.

**Status:** Execution-ready brief for a productized agent-run receipt desk.
