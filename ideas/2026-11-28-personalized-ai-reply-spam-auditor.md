---
title: Personalized AI Reply Spam Auditor & Blocklist Pack
date: 2026-11-28
status: ready
category: social media hygiene
tags: [agents, x-twitter, spam, blocklist, creators, indie-hackers, moderation, b2c]
monetization: per-pack fees and monthly retainers
effort: small
slug: 2026-11-28-personalized-ai-reply-spam-auditor
summary: A one-person operator plus agents audits a creator's recent X replies, cross-checks public AI spam lists, flags false positives with cited evidence, and delivers a personalized blocklist plus a browser-agent script to apply it cleanly.
---

# Personalized AI Reply Spam Auditor & Blocklist Pack

**Date:** November 28, 2026

## X signal (today)

X on 25-28 November 2026 is dominated by Pieter Levels' public AI reply blocklist at blockedforaireply.com (formerly levels.io).

- Levels published a mass-block list of suspected AI reply spam accounts, using his own posts as honeypots. Accounts that reply with AI patterns get investigated by Grok 4.7 (high reasoning) looking at recent replies, then added if conclusive. He reports ~500 suspensions and very low false positives, but the list has ~2k current IDs with roughly half already removed via appeals.
- Controversies: people who claim to write every reply by hand report being listed; appeals require an oath never to use AI for replies again. Mass-block browser agents are provided as a prompt.
- Broader vibe: AI reply spam is eroding trust in the reply section. Creators want cleaner feeds without nuking human conversation. Existing public lists are powerful but one-size-fits-all and slow to correct false positives for an individual's specific audience.
- Adjacent: Anthropic/Claude Ship for PR reviews, vibe-coding debates, OpenWorks for small-business AI help. The pattern is agents handling repetitive judgment at scale while a human keeps the final call.

This catalog already has problem-intent human replies (2026-09-09) and ship-receipt packs. It does not own a *personalized* auditor that starts from a creator's own reply graph + public lists and returns a cited, appeal-ready blocklist.

## Concept

Sell a **same-week personalized AI reply spam auditor pack** to creators, indie hackers, and small accounts who want their X reply section human again without mass-blocking every possible AI user.

The customer provides:

- Their X handle (public data only) + optional export of recent notifications/replies or a list of suspected accounts
- Preference notes: "block pure promotional AI bots but keep thoughtful AI-assisted replies," tolerance for false positives, niches they care about
- Optional: existing personal block list or links to public lists they already use

Agents + one human operator return within 48 hours:

1. A spam scorecard for the last 50-100 replies: pure-AI-farm, AI-assisted-but-human-intent, likely-human, unclear.
2. Cross-check against blockedforaireply.com and any other public lists, with "on public list / not / recently removed" status.
3. False-positive review: for borderline accounts, an agent pulls 5-10 recent replies, cites patterns (or lack of them), and recommends keep/block/monitor.
4. Personalized blocklist (CSV + text) of recommended new blocks, with one-line evidence each.
5. A ready-to-paste browser-agent prompt (or simple script) that applies the blocks at a safe rate, plus a reverse prompt for unblocking if needed.
6. A short "what changed" note the creator can post if they want, and an optional appeal template for any accounts they later regret.

This is **not** a public blocklist competitor, **not** a real-time extension, and **not** a guarantee of zero spam. It is a productized desk that uses agents for the volume and a human for the judgment calls on edge cases that matter to *this* creator.

## Target user

- Primary buyer: mid-size creators, indie hackers, and solopreneurs on X (1k-50k followers) who get noticeable AI spam but don't want Levels-style nuclear options or weekly manual cleanup.
- Urgent pain: reply section filled with "great post! check my tool" AI farms; fear of blocking real people; public lists too aggressive or too slow.
- Existing workaround: ignore it, manually block 10-20 per day, or run the public mass-block and then un-block people who complain.

## Why this works

- Market signal: Levels' list is trending hard; false-positive complaints are visible; people are already asking "how do I get the list and mass-block?" A personalized, cited version is the natural next product.
- Agent advantage: pull public reply history, score patterns, cross-reference lists, draft evidence, generate the browser prompt. Volume is free; judgment on "this one is a human who uses AI sometimes" is the scarce part.
- Solo-operator advantage: one person who has watched both pure spam and thoughtful AI-assisted replies can set the policy and review the 5-10 edge cases. The model is the researcher; the human is the editor.

## Monetization

- Primary model: per-pack service.
- First price test: 79 EUR / 79 USD for one handle + last 7 days of replies + personalized list + browser prompt; 149 for 30-day lookback + monthly refresh option.
- Upsell: 29/month monitoring (agent re-scans new replies weekly and emails a delta list); 49 to include a public "I use a human-reviewed filter" badge/template; 199 for a small team of 3 handles.
- Fun / public variant: publish one anonymized sample audit of a synthetic high-spam account. Never publish a real customer's reply data.

## Validation plan

1. Riskiest assumption: creators will pay ~79 for a cited personal audit instead of just running the free public list.
2. Demand test: post a sample scorecard on X and in 2-3 indie/creator Discords on 28-30 Nov. DM 20 people who replied to Levels' posts or complained about AI spam / false positives. Offer first 5 packs at 49 / 48h.
3. Success bar: 4 serious replies and 2 paid packs in 10 days. Kill if zero deposits after 20 touches.

## Execution plan (one person + agents)

**Agent 1 — Intake & fetch.** Accept handle + notes. Use public X search or user-provided export to pull recent replies. Refuse private DMs.

**Agent 2 — Pattern scorer.** Score each replier on spam signals (repetitive phrasing, link farms, zero prior engagement, known list membership). Output ranked list with citations.

**Agent 3 — False-positive reviewer.** For the top 15 borderline cases, pull additional public replies and write a 2-sentence evidence note + recommendation.

**Agent 4 — Pack assembler.** Build the CSV, browser-agent prompt, and short summary. Timestamp everything.

**Human operator.** Review the edge cases, drop anything sensitive, export final Markdown + CSV. Does not log into the customer's account.

Stack to start: browser + coding agents, one strong LLM, Stripe Payment Link, email. Public data only in week one.

## First 7-day action plan

1. Write a default scoring rubric (pure farm / AI-assisted human / likely human / monitor).
2. Build one public sample pack from a synthetic or heavily anonymized high-spam thread.
3. Publish sample + prices + "public data only" disclaimer on a one-pager and X.
4. Send 20 outbound notes to people engaging with the Levels list or complaining about AI replies.
5. Run two paid pilots.
6. Time human review. Target under 25 minutes after the second pack.
7. Keep or kill.

## Risks and mitigations

- False positives that hurt real humans: every recommendation cites evidence; customer can veto; provide easy unblock prompt.
- Overlap with public lists: this pack *starts* from them and personalizes; it does not replace them. Explicitly recommend running Levels' list first if the user wants maximum coverage.
- Platform risk: X could change rate limits or block patterns. Stay on public data and browser-agent scripts the user runs themselves.
- Scope creep into real-time extension: deliver the one-time pack and the prompt. Stop.

## Open questions

- [ ] Do buyers want the browser-agent prompt more than the cited CSV?
- [ ] Should the first version refuse accounts under 500 followers (too little data)?
- [ ] Is the strongest signal "I got listed and I'm human" or "my replies are full of bots"?

## Success metrics

- 1 public sample pack this week.
- 20 outbound touches.
- 2 paid packs.
- Human review under 25 minutes on a single-handle pack.

**Status:** Execution-ready brief for a productized personalized AI reply spam auditor desk.
