---
title: X awareness and engagement run design
date: 2026-07-27
status: drafted
platform: X
owner: TRAE
---

# X awareness and engagement run design

## Goal

Run a full 7-day X scheduling pass for `@beehivestrategy` that increases awareness and engagement while preserving a strong B2B operator voice, driving profile visits, and supporting eventual website and contact conversion.

## Context

- The account is being relaunched with a `3 posts/day` cadence.
- The user wants stronger awareness and engagement, not just quiet thought leadership.
- The audience is still business decision-makers first.
- X native scheduling is now proven to work, but the composer is inconsistent under automation.
- One production post has already been successfully scheduled and verified in X `Scheduled posts`.
- The live scheduling source has been reduced into a character-safe pack so that all posts fit within X limits.

## Chosen strategy

The approved strategy is a `reach-first hybrid` approach:

- stronger hooks than the original thought-leadership draft
- more aggressive hashtag use to widen discovery
- CTA on roughly half the posts
- direct links on only a minority of posts
- profile-first routing on the rest

This keeps the account discoverable without collapsing into generic “growth bait” copy.

## Alternatives considered

### Option 1: trust-first B2B

Use low-hashtag, low-CTA, authority-led posts with minimal direct promotion.

Trade-off:
- strongest fit for executive trust
- weakest for rapid awareness growth

### Option 2: reach-first hybrid

Use stronger hooks, active hashtag usage, selective CTA pressure, and limited direct-link posts.

Trade-off:
- best balance of awareness, engagement, and business relevance
- requires disciplined editing so the account does not drift into generic startup content

### Option 3: aggressive awareness

Optimize heavily for surface reach with broader hooks, dense hashtag usage, and stronger promotion.

Trade-off:
- may increase raw impressions
- increases the risk of weaker decision-maker fit and lower perceived quality

## Content design

### Voice

The posts should sound like:

- an operator with a clear point of view
- commercially aware, not academic
- direct and native to X
- useful enough to earn a follow even without a link click

The posts should avoid:

- fluffy inspiration language
- long corporate phrasing
- repeated buzzword stacking
- hashtag stuffing that looks spammy

### Post shape

Each post should follow this pattern where appropriate:

1. sharp first-line hook
2. one clear business tension or insight
3. compact supporting bullets or contrast
4. short ending that either reframes the problem or nudges the CTA

Posts should remain short enough to:

- read quickly in-feed
- support replies and reposts
- keep room for hashtags and occasional links

## Hashtag design

The approved setting is the most aggressive of the discussed options, but it still needs control.

Rule:

- aim for `2-3` hashtags on most posts
- only use tags that clearly fit the post topic
- do not mechanically repeat the same tag block on every post

Preferred hashtag pool:

- `#AI`
- `#Analytics`
- `#BusinessIntelligence`
- `#AIAgents`
- `#B2BMarketing`
- `#SEO`
- `#GEO`

Usage constraint:

- keep hashtags at the end of the post where possible
- skip a third hashtag if the copy becomes crowded or unnatural

## CTA and link design

### CTA intensity

Approved setting:

- use CTA in roughly half the posts

CTA types:

- soft: “worth rethinking if this is live in your business”
- medium: “DM if this is a live bottleneck”
- direct: “contact us” or “see the site” on selected posts

### Link usage

Approved setting:

- direct links on a minority of posts
- profile-first routing on the rest

Why:

- protects distribution on X
- still supports the user’s lead-generation KPI
- keeps some posts optimized for engagement and others for conversion

## Scheduling design

### Cadence

The active 7-day cadence remains:

- `12:30 PM HKT`
- `2:00 PM HKT`
- `4:30 PM HKT`

### Source files

Live scheduling should use:

- `obsidian/Beehive Strategy/07 - Marketing/X (Twitter) - 7 Day High-Cadence Pack (X-Safe).md`

Tracking should use:

- `obsidian/Beehive Strategy/07 - Marketing/X Manual Posting Schedule (7 Days).md`

### Verified workflow

The working flow is:

1. open dedicated compose page
2. type the post into the primary compose modal
3. open schedule modal
4. set the date and time
5. confirm the schedule values
6. submit the final schedule action
7. verify the result in `Scheduled posts`

## Automation constraints

The design must account for the real browser behavior already observed:

- X home composer is less reliable than dedicated compose for automation
- the final schedule action can appear disabled even with valid copy and time
- X sometimes fails to acknowledge a programmatically edited draft
- verification must never rely on button state alone
- the authoritative success check is the appearance of the item in `Scheduled posts`

Implication:

- schedule one post at a time
- verify after each successful queue action
- update the tracker only after verification
- do not claim batch success unless the scheduled list proves it

## Error handling

If a post fails to queue:

1. re-check character length and visible time state
2. re-open dedicated compose
3. re-enter the draft cleanly
4. retry scheduling once
5. verify whether the scheduled item appears anyway
6. if not verified, leave the tracker pending and stop on that item for review

This avoids silent failures and false positives.

## Testing and validation

Success criteria for this run:

- all scheduled copy remains within X limits
- hashtags fit the post topic and do not feel forced
- CTA distribution matches the approved mixed model
- only a minority of posts carry direct links
- each queued post is verified in `Scheduled posts`
- the schedule tracker reflects only verified outcomes

## Scope

This spec covers the X rewrite-and-schedule run only.

It does not yet cover:

- LinkedIn adaptation
- cross-platform repurposing
- analytics reporting loop after posts go live

## Immediate next step

After user review of this spec, the next step is to produce the execution plan for:

- rewriting the remaining pack into the approved hybrid style
- scheduling posts sequentially through dedicated compose
- verifying each scheduled item
- updating the tracker after each confirmed queue
