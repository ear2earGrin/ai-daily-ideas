---
title: Same-Week Niche Directory + Ad-Slot Pack for Solo Sellers
date: 2026-09-14
status: ready
category: distribution operations
tags: [agents, directory, seo, leads, x, services, b2b]
monetization: per-pack fees and monthly refresh retainers
effort: small
slug: 2026-09-14-niche-directory-adslot-pack
summary: A one-person operator plus agents turns a niche definition and a scrape brief into a cited 80-firm directory page plus three ad-slot drafts so a solo seller can own a list instead of renting ads on someone else's feed.
---

# Same-Week Niche Directory + Ad-Slot Pack for Solo Sellers

**Date:** September 14, 2026

## X signal (today)

X this week is arguing that **the one-person media company is an agent workflow, not a content calendar.**

- Cody Schneider (@codyschneider, 2 Sep, still circulating): a Hermes-style agent scrapes every company you sell to, Claude Code one-shots a directory site, you index it, refresh monthly from Search Console gaps, and run ads *on the directory* to your product. One site they shipped 90 days ago is doing ~100 organic clicks/day.
- Riley Brown (@rileybrown, 6 Sep): stop building agents that invent games; build the thin platform the other agents can plug into. Same shape: own the list and the host, not the generator.
- HybridClaw / Agency threads (12-13 Sep): businesses will pay for a locked workflow, not another chat window. A directory with a monthly refresh job is a clerk system.
- Anik Singal-style DESK-test chatter this week: "bring them the customers" still ranks above another UGC farm. A cited list is the smallest version of that.
- Catalog already owns a cited *signal pack* (2026-09-05) and a *proof-clip farm* (2026-09-12). It does not own the *directory asset* the seller can keep, refresh, and put an ad slot on.

## Concept

Sell a **same-week niche directory + ad-slot pack** when a solo seller can name a buyer list and does not want to rent reach from a marketplace or a creator.

The customer provides:

- niche sentence (who they sell to, geography, exclude list)
- their offer one-pager or landing URL
- optional seed list of 10 names they already know
- optional Search Console export if a thin site already exists

Agents plus one human operator return within 5 days:

1. A research log: sources scraped, date, include/exclude rules, duplicates dropped.
2. An 60-120 row firm table: name, site, city/region, one-line what-they-do, public contact if found, source URL, confidence (`listed` / `inferred` / `not-found`).
3. A single static directory page (Markdown + simple HTML) with filters by city or sub-niche.
4. Three ad-slot drafts: one in-directory native unit, one email footer, one X/LinkedIn line that points at a row, not a slogan.
5. A monthly refresh checklist: which rows look stale, which Search Console queries to chase, what not to invent.
6. A send pack: zip of CSV + page + source log + a 8-line email the seller can use to pitch a sponsor or themselves.

This is **not** a full SEO agency, **not** a guaranteed ranking product, and **not** a scraped email dump for spam. It is a productized clerk that turns "I should build a list" into a page a human can publish on Vercel in an afternoon.

## Target user

- Primary buyer: solo consultants, tool makers, and agency-of-one operators who sell into a countable niche (HVAC software, Bulgarian law boutiques, EU VAT agents, local clinic SaaS).
- Urgent pain: they know the 80 firms; the list lives in a Notes app; paid social is expensive; they have no owned URL that Google already understands.
- Existing workaround: buy a stale CSV, scrape once and never refresh, or post into a Facebook group and hope.

## Why this works

- Market signal: this week's X feed treats directories as the durable layer under agent media (podcasts, clip farms, newsletters). The catalog already writes posts; it does not ship the *list page*.
- Agent advantage: scrape public sites, normalize names, refuse emails that are not on a public page, keep a citation per row.
- Solo-operator advantage: one operator who has sold into the niche can kill tourist-trap rows and keep the 80 that actually buy. Judgment is the product; the model is the clerk.

## Monetization

- Primary model: per-pack service.
- First price test: 249 EUR / 249 USD for a first 80-row pack + page; 149 for a monthly refresh of an existing pack; 79 add-on to wire a Stripe or Lemon Squeezy sponsor slot on the page.
- Upsell: 399 setup + 149/mo retainer (refresh + 3 new rows + one Search Console note); 49 rush if they already have a clean seed CSV.
- Fun / public variant: publish one synthetic 25-row directory (fake HVAC shops in one EU city) as X marketing. Never publish a client's live buyer list.

## Validation plan

1. Riskiest assumption: a solo will pay ~249 for a cited list + page instead of asking ChatGPT for "top 50 companies in X" and pasting it into Notion.
2. Demand test: post one anonymized 25-row sample on X and in 2 indie-hacker rooms on 14-16 Sep. DM 20 people who posted "I need a list of [niche]" or who run a thin resource site. Offer the first 3 packs at 149 / 5-day SLA.
3. Success bar: 5 serious replies and 2 paid packs in 14 days. Kill if 20 outbound touches produce zero deposits.

## Execution plan (one person + agents)

**Agent 1 — Scope.** Lock niche, geography, exclude rules, max rows. Refuse "the whole internet."

**Agent 2 — Collector.** Public pages only (directories, association lists, official sites). Log source URL and fetch date. No login walls in week one.

**Agent 3 — Normalizer.** Dedup names, flag chains vs independents, mark contact as public-page-only. Never invent a phone number.

**Agent 4 — Page + ad drafter.** Build Markdown/HTML directory, CSV, three ad units that point at rows. Every cell has a source id or `not-found`.

**Human operator.** Kill junk rows, check three sample sites by hand, strip any personal emails that were not on a public page, export zip. The model does not blast the list.

Stack to start: coding + browser agents, one LLM, a static host (Vercel/GitHub Pages), Stripe Payment Link, a mailbox. No paid data vendors in week one.

## First 7-day action plan

1. Write a default evidence standard (what counts as a firm, a public contact, a stale row).
2. Build one public sample pack: 25 synthetic firms + page + three ad drafts.
3. Publish sample + prices + "no cold-email dump" disclaimer on a one-pager and X.
4. Send 20 outbound notes to recent "need a list" / "built a directory" posts.
5. Run two paid pilots in niches you already understand.
6. Time human review. Target under 50 minutes after job two on an 80-row pack.
7. Keep or kill.

## Risks and mitigations

- Scraped PII / spam lists: public-page contacts only; no enrichment APIs that sell emails; pack license forbids unsolicited bulk email.
- Hallucinated firms: every row needs a live source URL or it is dropped, not marked `inferred` without a reason.
- Overlap with cited signal pack: that product writes *posts*. This product ships a *list page*. If they only want drafts, send them to 2026-09-05.
- Overlap with proof-clip farm: clips are distribution for a local shop. A directory is a list asset for a B2B seller.
- SEO theater: do not promise rankings. Promise a page they can publish and a refresh checklist.
- Stale data: monthly retainer exists because a one-shot scrape dies in 90 days.

## Open questions

- [ ] Is the first buyer a tool maker who wants inbound, or a consultant who wants an outbound list they are allowed to keep?
- [ ] Should week one refuse niches larger than one country + one vertical?
- [ ] Is 249 too close to a cheap VA scrape, or still cheaper than a content site that never ships?

## Success metrics

- 1 public sample pack this week.
- 20 outbound touches.
- 2 paid packs.
- Human review under 50 minutes on a standard 80-row pack.

**Status:** Execution-ready brief for a productized niche-directory desk.
