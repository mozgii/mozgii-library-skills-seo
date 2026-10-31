---
name: search-console
description: 'Works Google Search Console end to end: choosing a domain or URL-prefix property, the Page indexing report and what each reason means, URL Inspection, the Indexing API and its limits, reading clicks, impressions, CTR and position correctly, the Branded queries filter, reports added in 2025 and 2026, exporting past the 25,000-row limit with a script, the Search Analytics and URL Inspection APIs, and reconciling an export with the report. Use when Search Console shows Crawled or Discovered - currently not indexed, a report needs explaining, data must be exported, someone asks about the Indexing API, or GSC totals do not match.'
metadata:
  tags:
  - seo
  - google
  - search-console
  - gsc
  - page-indexing
  - indexing-api
  - search-analytics-api
---

# Google Search Console

Search Console is Google's own record of a site: which URLs it knows, which it left out and why, and which queries bring
clicks. Its numbers have definitions that change how they read, so this skill names each report, what it can prove, and
how to get the data out without losing rows. KPIs and traffic drop diagnosis belong to `seo-measurement`.

## Step 0: read which properties the account can see

Read the property list first, because a URL-prefix property shows part of the site and every later number inherits
that. Authenticate once with Google Cloud's CLI, using a scope that reads Search Console:

```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform
export GSC_TOKEN="$(gcloud auth application-default print-access-token)"
curl -s -H "Authorization: Bearer $GSC_TOKEN" https://www.googleapis.com/webmasters/v3/sites
```

Prefer a domain property (`sc-domain:`) when one is listed. Then note whether a BigQuery bulk export already runs, and
who holds which permission level.

## Choose the report or API for each question

Each question has one place that answers it, and the others lose for a stated reason.

| Question | Use | Why the others lose here |
|---|---|---|
| Why is this group of URLs out of the index? | Page indexing report | URL Inspection answers for one URL at a time |
| What does Google hold for this one URL? | URL Inspection | Page indexing shows a sample by reason, and it lags |
| The same answer for hundreds of URLs | URL Inspection API | about 2,000 calls per property per day; the interface is by hand |
| Which queries and pages bring clicks? | Performance report, or `gsc_export.py` past the interface's rows | analytics alone has no search queries |
| How did a total move day by day? | Performance grouped by date, with no query | a query breakdown omits anonymised queries |
| What happened more than 16 months ago? | BigQuery bulk export, or your own exports | Search Console keeps 16 months |
| Is the host slow or failing for Googlebot? | Crawl stats | Page indexing shows the result, not the host's health |
| A job posting or a livestream changed | Indexing API | it is limited to those pages, so never use it for anything else |
| A page must leave results fast | Removals (`crawling-and-indexing`) | the Indexing API and Request indexing do not hide a page |

## Page indexing report reasons and what to do

The Page indexing report in Search Console groups non-indexed URLs by reason. Many reasons are correct behaviour, so the
question is always whether the URL should be indexed. The full table with causes and fixes is in
[references/indexing-reasons.md](references/indexing-reasons.md). The ones that matter most:

| Reason | Usual meaning | First action |
|---|---|---|
| Crawled - currently not indexed | fetched, judged not worth indexing now | improve or merge the page; ignore for low-value URLs |
| Discovered - currently not indexed | known but not fetched yet; often crawl capacity or low priority | internal links, sitemap, server speed |
| Excluded by 'noindex' tag | a `noindex` was served | remove it if the page should rank |
| Blocked by robots.txt | disallowed | allow it if it should rank |
| Soft 404 | 200 status with "not found" or empty content | return 404, or add real content |
| Duplicate without user-selected canonical | Google picked another URL | add a canonical, merge duplicates |
| Server error (5xx) | the server failed when Googlebot asked | fix capacity or errors; check Crawl stats |

## Indexing API: jobs and livestreams only

Google's Indexing API may be used only for pages with `JobPosting` or `BroadcastEvent` embedded in a `VideoObject`.
Every submission passes spam detection, and working around the quota with several accounts can cost the project its
access. Default quotas in October 2026, per project: 200 publish requests a day (`URL_UPDATED` and `URL_DELETED`
together, reset at midnight Pacific), 180 `getMetadata` requests a minute, 380 requests a minute across all endpoints.

Every other page gets found through a sitemap with honest `lastmod`, internal links, and Request indexing for a single
URL. The UGC Fresh Data Program (October 2026) is a separate pipeline for large moderated platforms and needs an
approved application, with no promise that content appears.

## Read Search Console metrics correctly

Search Console metrics have definitions that change how to read them.

- **Impression**: a link to your site appeared in a result the user saw (or could scroll to); one per page per query
  view, with different rules for some features.
- **Click**: a click that leads to your site from search.
- **Position**: the average topmost position of your site across impressions; it falls when you start ranking for
  new, deeper queries even if nothing got worse.
- **CTR**: clicks divided by impressions; compare only within one query type and position range.
- **Property type**: domain property (`sc-domain:`) covers all protocols and subdomains; URL-prefix properties cover
  one prefix only.
- Data by page groups by canonical URL; data by query omits anonymised queries, so query totals are lower than page
  totals.

## Export Search Console data past 25,000 rows

The export script calls the Search Analytics API and pages past the 25,000-row limit per request. It needs the login
from Step 0:

```bash
python3 scripts/gsc_export.py sc-domain:example.com 2026-07-01 2026-09-30 --dims query,page --out q3.tsv
python3 scripts/gsc_export.py sc-domain:example.com 2026-07-01 2026-09-30 --dims date --country usa --device MOBILE
python3 scripts/gsc_export.py sc-domain:example.com 2026-07-01 2026-09-30 --dims query --query-regex "(?i)price|cost"
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

If the API answers 403 with a quota-project message, add `--quota-project <your-gcp-project>` (the Search Console
API must be enabled in that project). The same call with `curl`:

```bash
curl -s -X POST "https://searchconsole.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query" \
  -H "Authorization: Bearer $GSC_TOKEN" -H "Content-Type: application/json" \
  -d '{"startDate":"2026-09-01","endDate":"2026-09-30","dimensions":["page"],"rowLimit":100}'
```

Other APIs: URL Inspection (`POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect` with
`inspectionUrl` and `siteUrl`; about 2,000 calls per property per day) and Sitemaps. For long-term storage, use
Search Console's bulk data export to BigQuery instead of the API.

## Brand and non-brand with the Branded queries filter

The default split is Search Console's built-in Branded queries filter in the Performance report (announced November
2025, on all eligible properties since March 2026). It classifies queries with AI, including misspellings and brand
products, and appears only on properties with enough query volume, typically domain-level ones; it can misclassify, so
spot-check it. Where it is missing or for the API, filter queries with a regex:

```text
(?i)(example ?outdoor|exampleoutdoor|exmaple outdoor)
```

Use it in the Performance report's query filter (Custom (regex)), or with `--query-regex` in the script, and its
negation for non-brand.

## Search Console features added in 2025 and 2026

Search Console gained several reporting features since 2025 that change how reports are built:

| Feature | Since | Use |
|---|---|---|
| Hourly data in the Search Analytics API | April 2025 | watch a launch or an outage within the day |
| Query groups in Search Console Insights | October 2025 | queries grouped by topic, for a quick view of what grows |
| Custom annotations on Performance charts | November 2025 | mark releases, migrations and updates where the whole team sees them |
| Branded queries filter | November 2025, all eligible properties March 2026 | brand and non-brand split without a regex |
| Weekly and monthly views | December 2025 | smooth weekday noise; compare months directly |
| Search generative AI report | June 2026, all sites by 31 August 2026 | AI feature impressions by page (no queries); see `google-ai-features` |
| Platform properties for social and video accounts | July 2026 | Google traffic to Instagram, TikTok, X and YouTube content; one property per account or channel; global since July 2026 |
| Multimodal filter under Web | September 2026 | visits from Google Lens, Circle to Search and image uploads; pages, no queries |

## Working through the Page indexing report

The report is read top-down by URL count, against the list of pages that should rank. Group the example URLs by template
before deciding anything: one template fix usually clears a whole reason. The steps, with the export limits, are in
[references/indexing-reasons.md](references/indexing-reasons.md).

## Worked example: 4,000 URLs "Crawled - currently not indexed"

Situation: a store's Page indexing report shows 4,000 URLs as Crawled - currently not indexed, and the owner wants them
all requested.

The export of example URLs groups into three path patterns: 3,600 are `?sort=` and `?color=` filter URLs, 300 are empty
tag pages, and 100 are real category pages with one line of text. The first two groups should not rank, so they stop being
linked and the tag pages get `noindex`. The hundred categories get real descriptions and links from the hub pages. Nobody
requests indexing, because a request does not change a quality decision.

Check: URL Inspection on five of the categories shows them indexed within weeks; the reason's count falls as the
filter URLs drop out; `gsc_export.py` with `--page-contains /category/` shows impressions rising on those pages.

## Verify an export against the Search Console report

Reconcile every export with the report before it feeds a decision, because a wrong property or search type gives a
believable but wrong file. Export a finished period grouped by date, and add up clicks and impressions:

```bash
python3 scripts/gsc_export.py sc-domain:example.com 2026-09-01 2026-09-30 --dims date --out daily.tsv
awk -F'\t' 'NR>1 {clicks+=$2; impressions+=$3} END {print clicks, impressions}' daily.tsv
```

Open Performance › Search results for the same property, with the same dates, type Web and no filters. The two totals
should match. If they differ, check the property, the search type and the dates, then use a period that ended at least
three days ago, since Google says data normally arrives in two to three days and the newest figures can change.

Some gaps are expected and need no fix:

| Export grouped by | Against the report's total | Why |
|---|---|---|
| date | matches | dates are aggregated by property, like the chart |
| query | lower | anonymised queries are left out, and Search Console stores top rows only |
| page | can differ | page data is aggregated by page, not by property |
| any, against analytics | never matches | days follow California time, and clicks are not sessions |

For an indexing fix, read Google's record of the URL with the URL Inspection API; an old `lastCrawlTime` means Google has
not seen the fix yet:

```bash
curl -s -X POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect \
  -H "Authorization: Bearer $GSC_TOKEN" -H 'Content-Type: application/json' \
  -d '{"inspectionUrl":"https://www.example.com/shoes/","siteUrl":"sc-domain:example.com"}' \
| python3 -c "import json,sys; r=json.load(sys.stdin)['inspectionResult']['indexStatusResult']; print(r.get('verdict'), r.get('coverageState'), r.get('lastCrawlTime'))"
```

## Checklist for Search Console work

The checklist confirms the numbers come from the right place and are read the right way.

1. Domain property in use, or the reason for a URL-prefix one is written down.
2. Top Page indexing reasons explained, none hitting money pages.
3. Every export reconciled with the report by date totals.
4. Reports state the period, the search type and the property.
5. Releases annotated on the Performance chart.
6. Monthly export or BigQuery bulk export running, beyond the 16-month window.
7. Indexing API used only for `JobPosting` and `BroadcastEvent` pages.
8. No token in the repository, logs or tickets.

## Gotchas in Search Console

The gotchas below produce wrong conclusions or wasted requests.

1. **Query totals lower than page totals.** Symptom: the two tables disagree. Cause: anonymised queries are left out
   of query tables; this is not lost data. Fix: use page totals for size and query tables for patterns.
2. **URL-prefix property misses traffic.** Symptom: totals look low for the whole business. Cause: the property covers
   one prefix, not another subdomain or protocol. Fix: use a domain property.
3. **Average position "dropped".** Symptom: clicks rise while average position falls. Cause: the site started ranking
   for many new deeper queries. Fix: look at clicks.
4. **Reading CTR without position.** Symptom: CTR falls in a month of growth. Cause: CTR falls when impressions grow
   on lower positions. Fix: compare CTR within one position range.
5. **An empty generative AI report.** Symptom: the report shows nothing. Cause: the property may be set to Exclude
   under Settings › Search generative AI, or it may have no AI impressions yet. Fix: check the setting before
   reporting zero visibility.
6. **Requesting indexing again and again.** Symptom: the page stays out and the quota runs out. Cause: the request
   does not change a quality decision, and it has a daily quota. Fix: improve or merge the page.
7. **Pushing blog posts through the Indexing API.** Symptom: a plugin promises instant indexing and the project risks
   its access. Cause: the API is limited to jobs and livestream pages, so such a plugin uses it outside its terms.
   Fix: use a sitemap, internal links and Request indexing for single URLs.
8. **403 from the API with a working token.** Symptom: an answer about a quota project. Cause: the call has no project
   with the Search Console API enabled. Fix: add `--quota-project <your-gcp-project>`.

## Anti-patterns in Search Console

Anti-patterns here treat a report as a to-do list, or a total as a fact without its definition.

| Do not | Do this instead |
|---|---|
| Fixing every non-indexed URL | decide per group whether it should rank |
| Quoting a total from an unreconciled export | add up a date export and match the report first |
| Reading the newest days as final | use a period that ended at least three days ago |
| Spreading the Indexing API across several accounts | keep to the quota; it can cost the project its access |
| Keeping only the 16-month window | export monthly, or use the BigQuery bulk export |

## References for Search Console

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/indexing-reasons.md](references/indexing-reasons.md): every Page indexing report reason with cause and
  fix, and how to work through the report.
- `scripts/gsc_export.py`: Search Analytics export with filters and paging.

## See also for Search Console

- `crawling-and-indexing`: robots.txt, `noindex`, status codes, removals and the diagnosis of one URL
- `seo-measurement`: KPIs, GA4 and traffic drops
- `google-ai-features`: the Search generative AI setting and report
- `google-rich-results`: enhancement reports for rich results
- `canonical-urls`: the canonical reasons in Page indexing
- `algorithm-updates-and-penalties`: Security and manual actions
