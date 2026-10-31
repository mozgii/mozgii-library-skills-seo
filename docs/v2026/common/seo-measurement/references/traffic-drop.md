---
title: Diagnosing an organic traffic drop
author: MOZGII, Inc.
lang: en
description: Step-by-step diagnosis of a drop in organic search traffic, with the check for each possible cause and what to do about it.
---

# Diagnosing an organic traffic drop

An organic traffic drop has a small number of possible causes, and each leaves a different pattern in the data. Work
through the steps in order and write down what each check showed; the pattern usually names the cause before the
end.

## Contents

1. Confirm the drop
2. Locate the drop
3. Date the drop
4. Patterns and their causes
5. Technical checks on affected pages
6. Algorithm updates
7. Demand and SERP changes
8. Writing up the diagnosis

## Confirm the drop

The first check confirms the drop exists in search data, not only in analytics.

- Compare Search Console clicks with analytics organic sessions for the same days. Search Console flat and analytics
  down means a tracking problem: a removed or broken tag, a consent banner change, a new domain in referral exclusions,
  a channel grouping edit.
- Compare with the same period last year, not only with the previous weeks; seasonality explains many "drops".
- Check Search Console for a data anomaly note on the chart.

## Locate the drop

Locating the drop narrows the cause. Segment Search Console clicks and impressions, before against after:

| Segment | If the drop is concentrated here | Suspect |
|---|---|---|
| one page group or template | one section or page type | a release on that template; content changes; that section's rankings |
| one country or language | one market | hreflang, a local competitor, a country-specific update |
| mobile only | mobile | mobile rendering, Core Web Vitals, intrusive interstitials |
| non-brand only | rankings | algorithm update, competition, content quality |
| brand only | demand | awareness, PR, a product change |
| one search appearance (rich results, video) | a feature | structured data errors; a retired feature |
| all of the above equally | whole site | technical problem, manual action, sitewide update |

## Date the drop

Dating the drop links it to an event. Find the first day the line breaks (daily data, not weekly), then list what
happened within a few days before: deployments, CMS or plugin updates, migrations, robots.txt or CDN changes, content
removals, and Google updates on the Search Status Dashboard (status.search.google.com) or Bing and Yandex
announcements.

## Patterns and their causes

Each drop pattern points to a group of causes.

| Pattern | Likely cause |
|---|---|
| sudden, sitewide, to near zero | `noindex` or robots.txt block, DNS or server failure, manual action, domain problem |
| sudden, one section | a release on that template (canonical, noindex, rendering, removed content) |
| gradual over weeks | content decay, competitors improving, crawl or index problems growing |
| starts on an announced update date, rolls over two weeks | a core or spam update |
| impressions stable, clicks down | CTR loss: AI Overviews or new SERP features, a rewritten title, rich results lost |
| impressions down, positions stable | demand fell (seasonality, trend) |

## Technical checks on affected pages

The technical checks on a sample of affected pages run before any content theory.

1. Fetch five affected URLs as Googlebot (`curl -sIL -A '<Googlebot smartphone user agent>' <url>` for the status
   chain and `X-Robots-Tag`, then the HTML for meta robots and canonical): status 200, no `noindex`, self canonical.
2. URL Inspection: indexed? Google-selected canonical? Last crawl date? Rendered HTML complete?
3. Page indexing report: did "Excluded by noindex", "Blocked by robots.txt", "Soft 404" or "Duplicate" counts jump on
   the drop date?
4. Security and manual actions report: anything new?
5. Crawl stats: response time or server errors rising?
6. Compare the current HTML of a page with an archived copy from before (a crawl export, the Wayback Machine): what
   content, links or markup changed?

## Algorithm updates

Algorithm updates re-rank pages and are not penalties; Google's core updates have no single fix. When a drop matches
an update:

- Compare which pages lost and which gained, and read the pages that now outrank yours for the main queries.
- Review the losers honestly against Google's helpful content questions: original value, first-hand expertise,
  clear authorship, satisfying the query better than the alternatives.
- Improve or merge the weakest pages; remove content that exists only to attract search traffic.
- Expect recovery, if any, mostly at later updates, not within days.

Spam updates are different: if the site used link schemes or scaled content, clean up first; a manual action shows in
Search Console and needs a reconsideration request.

## Demand and SERP changes

Demand and SERP changes reduce clicks without anything changing on the site.

- Google Trends for the main queries: did interest fall?
- Look at the current results page: an AI Overview, more ads, a video or shopping block, a forum result above you.
- If impressions hold but CTR falls, improve the title and the lead for the new SERP, and check whether the page is
  cited in the AI answer (`google-ai-features`).

## Writing up the diagnosis

The diagnosis write-up states the cause with evidence and a confidence level.

```text
Drop: non-brand clicks -38% from 2026-09-12 (Search Console, 28 days vs previous 28 and vs last year)
Where: /guides/ section only, all countries, mobile and desktop alike
When: 2026-09-12, the day of release 4.18 (new article template)
Cause (high confidence): the new template renders the article body client-side; URL Inspection shows the rendered
  HTML without body text on 5 of 5 sampled guides
Fix: server-render the body; then Validate fix in Page indexing; expected recovery within 2–4 weeks of recrawl
```
