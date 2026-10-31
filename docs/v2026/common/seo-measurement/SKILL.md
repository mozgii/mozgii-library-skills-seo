---
name: seo-measurement
description: 'Measures SEO results and diagnoses traffic changes: which source answers which question, organic traffic and conversions in analytics and the GA4 Data API, KPIs and reporting, segmenting brand and non-brand, comparing changed pages with a control group, and a step-by-step diagnosis of traffic drops (tracking, technical, algorithm updates, seasonality, SERP changes). Use when asked to report on SEO, explain a traffic drop or spike, set SEO KPIs, pull organic landing pages from GA4, or check whether a change worked.'
metadata:
  tags:
  - seo
  - search-console
  - analytics
  - reporting
  - traffic-drop
  - kpi
  - bing-webmaster
---

# SEO measurement and traffic diagnosis

SEO measurement answers two questions: is organic search bringing more of the visits and revenue that matter, and
why did a number change. Search engines' own consoles give the search side (impressions, clicks, positions);
analytics gives the site side (sessions, conversions, revenue).

## Step 0: read which properties and tags the site has

Read which properties and analytics tags exist first, because a URL-prefix property or a tag missing from one template
changes every number downstream. Log in once with a scope that reads Search Console.

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform
export GSC_TOKEN="$(gcloud auth application-default print-access-token)"
curl -s -H "Authorization: Bearer $GSC_TOKEN" https://www.googleapis.com/webmasters/v3/sites
curl -s https://www.example.com/ | grep -oE 'G-[A-Z0-9]{6,}|GTM-[A-Z0-9]+' | sort -u
```

Prefer a domain property (`sc-domain:`) when one is listed. An empty second result can mean a tag loaded by a consent
tool, so check the rendered page. Then note the analytics key events, the brand regex if one exists, and whether Bing
Webmaster Tools, Yandex Webmaster or a BigQuery export already run.

## Choose the data source for each question

Each question has one source that answers it, and the others lose for a stated reason.

| Question | Source | Why the others lose here |
|---|---|---|
| Which queries and pages bring clicks from Google? | Search Console | analytics alone has no search queries |
| Did revenue or leads from search change? | analytics, by landing page | Search Console stops at the click |
| How did a total move day by day? | Search Console grouped by date, with no query | a query breakdown omits anonymised queries |
| What did Googlebot fetch, and with what status? | server logs | analytics does not see bots; Search Console shows a summary |
| How visible is the site in AI answers? | Search Console generative AI report, Bing AI Performance, then referrals | Web totals mix AI features with classic results |
| What about Bing or Yandex? | Bing Webmaster Tools, Yandex Webmaster | Search Console covers Google only |
| What happened more than 16 months ago? | your own exports, or the BigQuery bulk export | Search Console keeps 16 months |

## Sources of SEO data

Each SEO data source measures something different, and their numbers never match exactly.

| Source | Measures | Notes |
|---|---|---|
| Google Search Console | impressions, clicks, CTR, average position by query, page, country, device, date, search appearance; 16 months | anonymised queries omitted from query tables; AI Overviews and AI Mode included in Web totals |
| Search Console generative AI report | impressions of your URLs in Google's AI features (Search and Discover) | pages, countries, devices, dates; no queries |
| Search Console platform properties | how your Instagram, TikTok, X and YouTube accounts perform in Google Search and Discover | one property per account or channel; global since July 2026 |
| Bing Webmaster Tools | Bing clicks, impressions, queries; backlinks; AI Performance (Copilot citations) | also covers traffic from partners that use Bing |
| Yandex Webmaster | Yandex queries, shows, clicks, positions; indexing; Alice AI visibility | `yandex-seo` |
| Analytics (GA4 or other) | organic sessions, engagement, conversions, revenue by landing page | consent banners and blockers hide part of the traffic |
| Server logs | crawler activity, real status codes | the only view of what bots actually fetched |

## Pull organic landing pages from GA4

The Google Analytics Data API (v1beta) gives the site side of the report: sessions, key events and revenue per landing
page for organic search. Enable it once, and authenticate with an Analytics scope:

```bash
gcloud services enable analyticsdata.googleapis.com
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform

curl -s -X POST "https://analyticsdata.googleapis.com/v1beta/properties/$GA4_PROPERTY:runReport" \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "x-goog-user-project: $GCP_PROJECT" -H "Content-Type: application/json" \
  -d '{"dateRanges":[{"startDate":"28daysAgo","endDate":"yesterday"}],
       "dimensions":[{"name":"landingPagePlusQueryString"}],
       "metrics":[{"name":"sessions"},{"name":"keyEvents"},{"name":"totalRevenue"}],
       "dimensionFilter":{"filter":{"fieldName":"sessionDefaultChannelGroup","stringFilter":{"value":"Organic Search"}}},
       "orderBys":[{"metric":{"metricName":"sessions"},"desc":true}],"limit":100}'
```

`$GA4_PROPERTY` is the numeric property ID, not the `G-` measurement ID. The API's `getMetadata` method lists the
dimension and metric names a property accepts.

## Brand and non-brand segments

Brand and non-brand traffic behave differently, so report them separately. Brand queries (the company or product
names, with typos) depend on awareness; non-brand queries show SEO progress. Use Search Console's Branded queries filter
where a property has it (`search-console`), and a query regex anywhere else:

```text
(?i)(example ?outdoor|exampleoutdoor|exmaple outdoor)
```

## SEO KPIs

SEO KPIs connect search visibility to business results; pick a few per audience.

| Level | KPI |
|---|---|
| Business | organic revenue or leads; organic share of new customers |
| Search | non-brand clicks; clicks to money pages; impressions for target clusters; AI feature impressions |
| Health | indexed share of canonical pages; Core Web Vitals pass rate; crawl errors |
| Work | pages published or improved; fixes shipped from the audit |

Average position of the whole site and "number of keywords in the top 10" are poor KPIs: both move when the site
starts showing for new queries, without any change in traffic.

## Diagnose a traffic drop

A traffic drop is diagnosed from the outside in: first confirm it is real, then find where it is, then why. Full
steps with checks are in [references/traffic-drop.md](references/traffic-drop.md). The short order:

1. **Is it real?** Analytics only, or Search Console too? A drop only in analytics points to tracking (a lost tag,
   a consent change), not to search.
2. **Where is it?** Segment by page group, device, country, query type (brand or non-brand) and search appearance.
3. **When did it start?** Match the date against releases, migrations and the Google Search Status Dashboard
   (status.search.google.com) for core and spam updates. A date that matches an update, or a manual action, is diagnosed with
   the `algorithm-updates-and-penalties` skill.
4. **What kind?** Impressions fell (lost rankings or demand) or only CTR fell (SERP changes such as AI Overviews,
   new features, a rewritten title).
5. **Technical first**: indexing, robots, canonicals, status codes and rendering on the affected pages.
6. **Then demand and competition**: Google Trends for seasonality; who now ranks above you and why.

The Google Trends API (alpha since July 2025) gives scaled search interest over time for demand and seasonality
checks, for accounts admitted to the alpha.

## Check whether a change worked

A change is measured against a comparison, not against last week alone. Annotate the release date, compare the
changed pages with a similar unchanged group over the same period (28 days before and after, same weekdays), and
wait for recrawl (URL Inspection shows the crawl date). Seasonality and updates move all pages; only the difference
between the groups belongs to the change.

## Worked example: a monthly SEO report for an online store

Request: a one-page monthly report for the owner of a store with 1,200 products.

Built from: Search Console (domain property, Branded queries filter), GA4 organic conversions by landing page, and
the generative AI report. Content: non-brand clicks 18,400 (+9% month on month, +31% year on year); clicks to
category and product pages 14,100; organic revenue €61,000 (24% of total); AI feature impressions 52,000 on 140
pages; indexed share of canonical pages 96%; Core Web Vitals pass rate 88% of mobile URLs. Then three lines: what
changed (the filter fix shipped on the 4th, annotated), what moved because of it (category clicks +14% against +3% for
untouched categories), and the next two actions. Average position and keyword counts are left out.

## Verify a report before it goes out

Check each number at its source before it reaches the owner, because a wrong property or a missing tag gives a believable
but wrong report. Add up a finished month by date with the login from Step 0, and match the two totals against
Performance › Search results for the same property, with the same dates, type Web and no filters:

```bash
curl -s -X POST "https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer $GSC_TOKEN" -H "Content-Type: application/json" \
  -d '{"startDate":"2026-09-01","endDate":"2026-09-30","dimensions":["date"],"rowLimit":31}' \
| python3 -c "import json,sys; r=json.load(sys.stdin)['rows']; print(sum(x['clicks'] for x in r), sum(x['impressions'] for x in r))"
```

Then confirm the analytics tag answers on one URL per template, since a template without it reads as a traffic drop:

```bash
for u in https://www.example.com/ https://www.example.com/shoes/ https://www.example.com/p/runner-x; do
  printf '%s: ' "$u"; curl -s "$u" | grep -oE 'G-[A-Z0-9]{6,}|GTM-[A-Z0-9]+' | sort -u | tr '\n' ' '; echo
done
```

Search Console and analytics never match, because days follow California time and clicks are not sessions: report them
side by side, and do not reconcile them. Read a period that ended at least three days ago. Exports and the gaps to expect
between tables: the `search-console` skill.

## Checklist for SEO measurement

The measurement checklist confirms the numbers can be trusted and are read the right way.

1. Search Console domain property, Bing Webmaster Tools and analytics verified; analytics tag on every template.
2. Brand regex defined; reports split brand and non-brand.
3. Organic conversions tracked per landing page.
4. Monthly export of Search Console data (API or BigQuery) beyond the 16-month window.
5. Releases annotated (Search Console custom annotations on the Performance chart); changes measured against a
   control group.
6. AI visibility reports (Search Console generative AI, Bing AI Performance) included.

## Gotchas in SEO measurement

The gotchas below produce wrong conclusions.

1. **Average position "dropped".** Symptom: clicks rise while average position falls. Cause: the site
   started ranking for many new deeper queries. Fix: look at clicks.
2. **Comparing a period with a holiday to one without.** Symptom: a sudden "drop" or "win" around a holiday. Cause:
   the two periods are not alike. Fix: compare year over year or same weekdays.
3. **A tracking change looks like an SEO drop.** Symptom: analytics falls while Search Console stays flat. Cause: a
   tag or consent change, not search, moved the number. Fix: check Search Console clicks before blaming search.
4. **Reading CTR without position.** Symptom: CTR falls in a month of growth. Cause: CTR falls when impressions grow
   on lower positions. Fix: compare CTR within one position range.
5. **A citation counted as a visit.** Symptom: a report treats citations as traffic. Cause: Bing's AI Performance
   shows a sample of citations, and a citation is neither a click nor traffic. Fix: report citations and visits apart.

## Anti-patterns in SEO measurement

Anti-patterns in reporting pick the number that moved and call it the result.

| Do not | Do this instead |
|---|---|
| Reporting whole-site average position | report non-brand clicks and clicks to money pages |
| Reporting keyword counts in the top 10 | use impressions for target clusters |
| Judging a change by last week alone | compare changed pages with a similar unchanged group |
| Mixing brand and non-brand in one line | split them |
| Keeping only the 16-month window | export monthly, or use the BigQuery bulk export |

## References for SEO measurement

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/traffic-drop.md](references/traffic-drop.md): the traffic drop diagnosis with checks and causes.

## See also for SEO measurement

- `search-console`: metric definitions, exports, new reports and reconciling totals
- `algorithm-updates-and-penalties`: a drop that matches an update or a manual action
- `core-web-vitals`: the page experience numbers in a report
- `ai-search-visibility`: AI search reports and referral channels
- `google-ai-features`, `bing-ai-and-copilot`: each engine's AI report
- `keyword-research`: query exports for cannibalisation
- `seo-audit`: technical causes behind a drop
- `bing-webmaster-tools`, `naver-search-advisor`, `yandex-seo`: each engine's own reports
