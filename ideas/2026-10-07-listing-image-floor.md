---
title: Same-Day Listing Image Floor for WooCommerce Shops
date: 2026-10-07
status: ready
category: catalog image operations
tags: [agents, woocommerce, ecommerce, photos, makers, local-business, indie-hackers, services, b2b]
monetization: per-batch fees and monthly refresh retainers
effort: small
slug: 2026-10-07-listing-image-floor
summary: A one-person operator plus agents turns a messy folder of product photos into WooCommerce-ready catalog, single, and thumbnail files plus a SKU map, so a small shop stops resizing images by hand before every drop.
---

# Same-Day Listing Image Floor for WooCommerce Shops

**Date:** October 7, 2026

## X signal (today)

X on 4–7 October 2026 has a boring, paid job sitting in plain sight, next to the louder agent-pricing argument.

- Kikuyu Pipes (@DrKanyuira, 4 Oct, 4.7k views): "I wish there was a tool for automatically resizing images on WooCommerce. Hio kazi hunibore kama gathia." The complaint is not model quality. It is the hand work of making product photos fit the store.
- Adjacent, 5–7 Oct: small-business automation posts keep pricing the tool plan at $15–50/month after the real setup is already done (see today's sibling card, `2026-10-07-automation-quote-gap-card.md`). Image prep is one of those unpriced setup jobs. It shows up on every new SKU, not once at install.
- Adjacent, 6 Oct: makers running Etsy, Shopify, and TikTok as a one-person stack still talk about the catalog as the bottleneck, not the ad. A WooCommerce shop has the same bottleneck with worse defaults: catalog, single, and thumbnail sizes that do not match the phone photo.
- Sports and TV dominated the worldwide trend list on 7 Oct (Dodgers, Messi, AEW, DWTS). That is a distribution day, not a catalog day. Shops that want a same-night offer still need the product image to exist at the right crop before the post goes out. This catalog already owns game-night local offers (`2026-09-21`). It does not own the image floor those offers sit on.

This is not a design subscription and not a generative product shoot. The seller already has the photos. The job is to make them listable.

## Concept

Sell a **same-day listing image floor** to a one-person WooCommerce shop, maker, or local brand that is sitting on a folder of phone photos and has not published the drop because every image is the wrong size.

The customer sends:

- a zip or Drive link of product photos they own (phone shots are fine).
- a SKU or product-name list, even a messy spreadsheet.
- the three target sizes they already use, or a note that they want WooCommerce defaults (catalog 300×300, single 600×600, thumbnail 150×150 — confirm against their theme, do not invent a theme spec).
- optional: background preference (white pad, blur pad, or leave as shot) and one "do not crop" rule (logo, label, face of the jar).

Agents plus one human operator return within one business day:

1. A renamed set: `{sku}-catalog.jpg`, `{sku}-single.jpg`, `{sku}-thumb.jpg`, sRGB, EXIF stripped, longest side matched to the target, subject not cut off.
2. A CSV: source file, SKU, product name, output paths, crop note (`padded` / `center-crop` / `needs-human`).
3. A reject list: blurry, duplicate, or no matching SKU. No silent deletes.
4. A one-page upload note: media library order, alt text drafted from the product name only (no invented claims), and which images still need a human crop.
5. A source appendix. No claim that the photo was shot in studio, that the background removal is perfect, or that the theme will accept the file without a cache flush.

This is **not** a new product photo shoot, **not** a generative model of the product, and **not** a WooCommerce plugin in week one. It is a productized desk that finishes the boring resize the seller already wished existed.

## Target user

- Primary buyer: solo WooCommerce shops, Etsy makers who also run a WP store, and local brands in the EU/UK/Africa who upload phone photos and lose an evening to the media library.
- Urgent pain: a drop is ready except the images. Resizing by hand is the work they called boring. Hiring a designer for 30 SKUs costs more than the drop.
- Existing workaround: Canva one image at a time, a half-broken bulk plugin, or shipping the phone photo and letting WooCommerce crop the label off.

## Why this works

- Market signal: the wish is explicit and recent. The user did not ask for a better model. They asked for the resize to be done.
- Agent advantage: match filenames to a SKU list, draft alt text from the product name, flag crops that cut a label, and refuse to invent a product claim the spreadsheet does not contain.
- Solo-operator advantage: one person with ImageMagick or Pillow plus a vision pass can review 30 SKUs in one sitting. The model proposes the crop. The operator rejects a cut label. Week one does not need a plugin, a theme license, or a store login.

## Monetization

- Primary model: per-batch service, then a monthly refresh for shops that add SKUs every week.
- First price test: 49 EUR for up to 30 SKUs, same day. 79 EUR if the operator also writes alt text and a media-library upload order.
- Upsell: 19 EUR per extra 15 SKUs; 99 EUR/month for up to four batches. A later product is a small WP upload folder that runs the same spec locally. Do not build the plugin until two shops pay for the batch.
- Fun / public variant: publish one synthetic before/after of a jam-jar phone photo becoming catalog, single, and thumb, with the label still readable. Never use a customer's product.

## Validation plan

1. Riskiest assumption: a shop owner will pay ~49 EUR to stop resizing by hand, instead of installing one more free plugin they will not configure.
2. Demand test: post the jam-jar sample on 7–9 Oct and reply under "I wish WooCommerce resized this" and maker-drop posts. Offer the first 5 batches at 29 EUR.
3. Success bar: 5 serious replies and 2 paid batches in 14 days. Kill if 20 touches produce zero files sent.

## Execution plan (one person + agents)

**Agent 1 — Intake.** Accept a zip and a SKU list. Refuse ID photos, medical images, and anything the sender does not claim to own.

**Agent 2 — Matcher.** Pair each photo to a SKU by filename or a one-line caption. Unmatched files go to the reject list, not to a guessed product.

**Agent 3 — Crop clerk.** Propose pad vs center-crop. Mark `needs-human` if the label, logo, or product edge would be cut. Do not generate a new product.

**Agent 4 — Pack writer.** CSV, alt text from the product name only, upload note, appendix.

**Human operator.** Open the `needs-human` set. Export zip + CSV. The model does not log into wp-admin.

Stack to start: Pillow or ImageMagick, one vision-capable model for the crop flag, a paste/zip inbox, a Stripe Payment Link. No WooCommerce login in week one.

## First 7-day action plan

1. Write the default size card (catalog, single, thumb) and the do-not-crop rules (label, logo, jar edge).
2. Build the jam-jar sample from a photo you own.
3. Publish sample + prices on a one-pager and X.
4. Send 20 notes to WooCommerce resize complaints and maker-drop posts.
5. Run two paid batches.
6. Time human review. Target under 40 minutes after batch two.
7. Keep or kill. Only then sketch the plugin.

## Risks and mitigations

- Theme sizes differ: ask for the three sizes. If the seller does not know them, ship the documented defaults and label them `confirm against theme`.
- Cut labels: anything flagged `needs-human` does not ship as final. Pad before crop.
- Invented alt text: product name and visible color only. No "organic", no medical claim, no price.
- Rights: only files the sender says they own. No stock scrape, no regenerating a competitor's packshot.
- Overlap with launch-week SKU diff (`2026-09-10`): that pack compares accessory listings across a launch. This pack resizes the seller's own photos.
- Overlap with proof-clip farm (`2026-09-12`): that pack cuts short-form video. This pack is still images for the media library.
- Store access: do not take wp-admin in week one. The seller uploads the zip.

## Open questions

- [ ] Is the first buyer a WooCommerce shop, or a maker who will pay once per drop and never install a plugin?
- [ ] Does 29 EUR for the first batch convert better than 49 EUR with alt text included?
- [ ] Should week one refuse folders with no SKU list at all?

## Success metrics

- 1 public before/after this week.
- 20 outbound touches.
- 2 paid batches.
- Human review under 40 minutes on 30 SKUs.

**Status:** Execution-ready brief for a productized WooCommerce listing-image floor.
