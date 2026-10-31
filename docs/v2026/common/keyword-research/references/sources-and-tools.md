---
title: Keyword demand and position sources
author: MOZGII, Inc.
lang: en
description: Which keyword data source answers which question, what it costs, and how it misleads, for Google, Bing and Yandex.
---

# Keyword demand and position sources

Keyword data sources answer three different questions: how many people search a phrase (demand), how they phrase it
(wording), and where a site ranks (positions). Each source below says which it answers and how it fails. Prices and
quotas change; read the current pricing page before relying on a paid source.

## Contents

1. Demand sources
2. Wording sources
3. Your own site's queries and positions
4. Competitor positions and SERP data
5. What to ignore

## Demand sources

Demand sources estimate monthly searches; none is exact, and they disagree with each other.

| Source | Access | Gives | Limits |
|---|---|---|---|
| Google Keyword Planner | Google Ads account | monthly volume, trend, competition for ads | wide ranges (100–1K) unless the account spends; groups close variants |
| Bing Webmaster Tools › Keyword Research | free, verified site | Bing impressions per keyword, by country and device, with trends | Bing's share of the market only |
| Google Trends | free | relative interest over time and by region | no absolute numbers; compare 2–5 terms at once |
| Search Console › Performance | site owner | impressions for queries the site already shows for | only queries you already rank for; anonymised long tail |
| Yandex Wordstat (and its API) | Yandex ID; API on application | exact and broad monthly frequency by region and device | Yandex only; see the `yandex-wordstat` skill |
| Paid suites (Ahrefs, Semrush, Similarweb and others) | subscription | modelled volume, difficulty, SERP features, competitor keywords | modelled from clickstream and panels; errors of 2× are common on small terms |

Record the source and month with every number. Compare phrases with numbers from the same source only.

## Wording sources

Wording sources show how people phrase a need; they rank phrases against each other but do not give volume.

| Source | Access | Gives |
|---|---|---|
| Bing autocomplete | none (`scripts/autocomplete.py`, the default) | Bing completions |
| Google autocomplete | by hand in a private window; `--engine google` only for a few seeds, at your own risk, because automated queries to Google break its spam policy on machine-generated traffic | up to 10 completions per prefix, by popularity |
| People also ask, related searches | a search in a private window | sub-questions for H2s and FAQ content |
| Search Console queries | site owner | the exact words people used to find you |
| Reddit, forums, reviews, support tickets, sales calls | public or internal | customer vocabulary and objections |

Suggest Signal from the script: Σ 1/position over every list a phrase appears in. A phrase that tops several lists
is phrased the way people type it.

## Your own site's queries and positions

Your own queries and positions come only from the search engines' own tools, through the site owner's login.

- **Google Search Console** (web and API): clicks, impressions, CTR, average position by query, page, country,
  device, date; 16 months of history. The interface exports up to 1,000 rows; the Search Analytics API returns up to
  25,000 rows per request and pages beyond that.
- **Bing Webmaster Tools**: search performance by query and page; AI Performance for Copilot citations.
- **Yandex Webmaster**: search queries with shows, clicks and positions.

For research, export the queries you already get impressions for: they are proven demand your pages partly match.

## Competitor positions and SERP data

Competitor positions come from SERP data, which must be collected without scraping search engines directly.

- Do not scrape Google or Yandex results pages: it violates Google's spam policy on machine-generated traffic and
  triggers captchas and blocks.
- SERP APIs (DataForSEO, SerpApi and similar) return results per query, location and device for a fee.
- Paid suites estimate competitors' rankings across millions of keywords.
- Manual checks: a private window with the right country and language, a screenshot with the date.

## What to ignore in keyword data

Some keyword metrics look precise and mean little.

| Claim | Why |
|---|---|
| Keyword difficulty scores | vendors' own formulas, mostly backlink counts of the top 10 |
| Domain authority, domain rating, trust scores | vendors' own metrics; search engines do not use them |
| Keyword density targets | no engine publishes such a number; it produces text written for robots |
| Positions for zero-demand phrases | they rank because nobody competes, and bring nothing |
| Meta keywords | ignored by Google and Bing |
