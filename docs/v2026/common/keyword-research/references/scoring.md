---
title: Keyword scoring, tiers and intent classes
author: MOZGII, Inc.
lang: en
description: A reproducible keyword rating with business value, market signal, suggest signal and page readiness, plus demand levels, intent classes, tiers and strategic bets.
---

# Keyword scoring, tiers and intent classes

A reproducible keyword rating lets two people, or two agents, rank the same list the same way. The weights below are
a tested default; a project may tune them, but it writes the weights next to the list so every score can be
recomputed.

## Contents

1. Demand levels
2. The rating formula
3. Business value
4. Market, suggest and readiness signals
5. Tiers
6. Intent classes
7. Strategic bets

## Demand levels

Demand levels turn a volume number into a decision. The thresholds suit a niche B2B site; a consumer site raises them
by an order of magnitude.

| Level | Rule | Use |
|---|---|---|
| strong | ≥ 20 searches a month in the target market, or ≥ 5 and a top-3 autocomplete suggestion | main phrase candidate |
| some | ≥ 5 a month, or ≥ 1 and suggested | main phrase of a narrow page, or an H2 or secondary phrase |
| weak | no measured volume of its own but longer phrases containing it have demand, or suggested with 0 | body text forms only |
| none | no volume, not suggested | never a main phrase; drop unless it is a strategic bet |

Measured volume decides. A suggestion proves the wording exists, not that it has volume. Without any volume data,
suggestions alone give at most `some` (top 3) or `weak` (suggested), and the plan says the numbers are missing.

## The rating formula

The rating combines four 0–100 components:

```text
rating = 0.55 × business value + 0.20 × market signal + 0.10 × suggest signal + 0.15 × page readiness
```

```js
const value = 0.375 * intent + 0.25 * fit + 0.1875 * chance + 0.1875 * size;
const market = [0, 25, 50, 75][Math.min(sites, 4)] ?? 100;
const rating = 0.55 * value + 0.2 * market + 0.1 * suggest + 0.15 * readiness;
```

After volumes arrive, phrases with `none` demand leave the list and the rest are recomputed. Measured demand can
replace part of the market signal once every phrase has it.

## Business value

Business value, 0–100, is the commercial worth of ranking for the phrase.

| Component | Weight | 100 means | 0 means |
|---|---|---|---|
| Intent | 37.5% | ready to buy or order ("price", "buy", "quote", "hire", "near me") | free, DIY, jobs, courses |
| Offer fit | 25% | exactly what the business sells | an adjacent topic |
| Chance to win | 18.75% | few strong competitors; the site has proof | big brands and aggregators own the top 10 |
| Deal size | 18.75% | the largest product | the cheapest entry product |

## Market, suggest and readiness signals

The three remaining components describe the market and the site.

**Market signal**: how many tracked competitors use all significant words of the phrase in a title, H1 or H2
(0 sites = 0, 1 = 25, 2 = 50, 3 = 75, 4 or more = 100). It confirms the market talks this way; it is not demand.

**Suggest signal**: 100 if the phrase appeared in autocomplete during collection, else 0; or the script's Signal
scaled to 0–100.

**Page readiness**: the phrase is already in the title of a published page = 100; the page exists but the phrase is
not in its title = 70; no page = 30.

## Tiers

Tiers decide where a phrase is placed on its owner page.

| Tier | Rating | Treatment |
|---|---|---|
| A | ≥ 70 | title, H1, first screen, links from hubs; checked first |
| B | 55–70 | H2s, body text, FAQ items on the owner page |
| C | < 55 | body text and articles only; not promoted separately |
| brand | — | home and about pages |

## Intent classes

Intent classes map a phrase to the page type that can rank for it. Confirm with the live top 10.

| Class | Signals in the query | Page type |
|---|---|---|
| transactional | buy, order, price, cost, quote, hire, book, coupon | product, service or booking page |
| commercial investigation | best, top, vs, review, alternative, compare | comparison page, buying guide, review |
| informational | how, what, why, guide, ideas, examples | article, guide, tool |
| navigational | a brand or product name | home, product or login page |
| local | near me, in a city, open now | location page, Business Profile |
| exclude | free, DIY, jobs, salary, course (unless sold), competitor brands | none |

## Strategic bets

A strategic bet is a category the business wants to own before demand exists. It may score above its data with a
fixed, labelled bonus (for example +20 for the strategic cluster, +10 for a new segment). Record it as an owner
decision with a review date and the metric that will confirm or kill it (monthly volume of the category term,
impressions in Search Console). A bet is not demand; never present its rating as market evidence.
