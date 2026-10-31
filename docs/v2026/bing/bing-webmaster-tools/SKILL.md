---
name: bing-webmaster-tools
description: 'Sets up and works Bing Webmaster Tools (BWT): importing from Search Console or adding a site by hand, verification by Domain Connect, BingSiteAuth.xml, meta tag or CNAME, what each report shows, URL Inspection, Site Scan, Crawl control, Block URLs, submission quotas, the Webmaster REST API with its JSON endpoints, keys and OAuth 2.0, the retirement of SOAP and POX, and a script that reads quota, queries, pages and crawl stats and submits URLs. Use for Bing Webmaster Tools setup, verifying a site with Bing, a Bing API key, InvalidApiKey, URL Submission or Content Submission limits, exporting Bing queries, or an integration that stopped working in September 2026.'
metadata:
  tags:
  - seo
  - bing
  - bing-webmaster-tools
  - bwt
  - webmaster-api
  - url-submission
  - oauth
---

# Bing Webmaster Tools

Bing Webmaster Tools (`bing.com/webmasters`) is the Bing counterpart of Search Console, and the only first-party view of
how Bing sees a site. Its data is also open through a REST API that a script can read and write. This skill adds the site,
says what each tool answers, and gets the data out. What Bing asks of pages belongs to `bing-seo`; AI Performance and the
AI preferences belong to `bing-ai-and-copilot`.

Facts here were read on Microsoft's own pages on 31 October 2026. Bing's help pages render only with JavaScript, so a
plain fetch of them returns a title and no text: open them in a browser.

## Step 0: read what the account already has

Read the account's state first, because a site may already be verified by someone else, and a quota can be lower than
the documented one. Without a key, ask who owns the site in Webmaster Tools. With one:

```bash
export BING_WEBMASTER_KEY=...     # Settings › API Access; one key per user, valid for all that user's sites
python3 scripts/bing_api.py sites
python3 scripts/bing_api.py quota https://www.example.com/
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

Then note whether Search Console already covers the site, because that decides the fastest way in.

## Choose how to add the site

Bing offers two paths, and the import wins whenever Search Console is already verified.

| Path | Details |
|---|---|
| Import from Search Console | verified automatically; brings sitemaps and user roles; 100 sites at a time; Bing checks ownership again from time to time and imports new sitemaps |
| Add manually | a whole domain or one branch (`example.com/clothing/`); then verify by Domain Connect DNS, `BingSiteAuth.xml` in the root, a `<meta>` tag in `<head>`, or a CNAME record |

Sign in with a Microsoft, Google or Facebook account. An account holds at most 1,000 sites. Expect about 48 hours before
data appears, and no history from before the site was added. Then submit the sitemap (XML, RSS 2.0, Atom 0.3 or 1.0, or a
text file) and add a `Sitemap:` line to robots.txt.

## What each Bing Webmaster tool answers

Each tool below answers one question, and most have a limit worth knowing before reading it.

| Tool | Answers | Worth knowing |
|---|---|---|
| Search Performance | clicks, impressions, CTR, position by keyword and page | up to six months; sources are Web and Chat, News, Images, Videos, Knowledge Panel; figures rose from 24 March 2023 when those sources joined |
| AI Performance | where Copilot and Bing AI summaries cite the site | `bing-ai-and-copilot` |
| URL Inspection | index status, SEO and markup of one URL | Live URL does not follow redirects, because Bingbot fetches each redirect separately |
| Site Explorer | which URLs Bing knows | |
| Site Scan | an on-demand crawl with errors, warnings and notices | a monthly quota that support will not raise; "Ignore Robots.txt" exists, so keep it off in production |
| Recommendations | prioritised issues with severity | lists 50 URLs, the rest by CSV |
| IndexNow | submissions, their source, crawl and index status | "Important URLs Missed" lists URLs indexed in the last 7 days that did not arrive through IndexNow |
| Crawl control | Bingbot speed for each hour of the day | a `crawl-delay` in robots.txt always wins over this setting |
| Block URLs | hides a URL or folder at once | temporary: 90 days, most processed in under 12 hours |
| Keyword Research | Bing demand by country, language and device | up to six months |

## Submission limits for URLs and content

The submission APIs reach Bing alone, and Microsoft says URL and Content Submission may be deprecated, so use them only
where IndexNow cannot do the job (`bing-seo` compares the methods).

| Method | Limit |
|---|---|
| Manual Submit URLs | 10,000 a day per domain |
| URL Submission API | 10,000 a day per domain, 500 per batch |
| Content Submission API | 10 MB per submission, uncompressed |

Quotas reset at midnight UTC and apply to the domain, not each subdomain. A site's real quota can be lower than 10,000, so
read it with `bing_api.py quota` before a large batch. Request indexing in URL Inspection spends the same quota. No
method guarantees indexing.

## Use the Webmaster REST API

The Webmaster API exposes the same data as the tools. Use the JSON endpoints only: SOAP and POX were retired on 31 August
2026, and the migration changes the URL segment, the content type and how you parse the answer. Answers come wrapped in
`{"d": ...}`, and dates arrive as `/Date(1316156400000-0700)/`.

```bash
python3 scripts/bing_api.py quota https://www.example.com/
python3 scripts/bing_api.py queries https://www.example.com/ --top 100 --out bing-queries.tsv
python3 scripts/bing_api.py crawl https://www.example.com/ --out bing-crawl.tsv
python3 scripts/bing_api.py submit https://www.example.com/ --file changed-urls.txt
```

Choose the login by who runs the code.

| Login | Use it when | Why the other loses here |
|---|---|---|
| OAuth 2.0 | an application acts for other people's sites, or any new work | Microsoft recommends it, with the scopes `webmaster.read` and `webmaster.manage` |
| API key | a script of your own, on your own verified sites | it needs no client, but it travels in the query string and works for all that user's sites |

Methods, OAuth steps and error shapes: [references/webmaster-api.md](references/webmaster-api.md).

## Worked example: a SaaS adds Bing reporting to its weekly report

Situation: a software company has Search Console on its domain, no Bing setup, and wants Bing queries in a weekly report.

The team imports from Search Console, which verifies the site and brings the sitemaps, and waits about 48 hours. The
history starts there, so the report's first weeks say so. A developer creates a key under Settings › API Access, and stores
it in the job's secret store as `BING_WEBMASTER_KEY`. The weekly job runs:

```bash
python3 scripts/bing_api.py queries https://www.example.com/ --top 100 --out bing-queries.tsv
python3 scripts/bing_api.py crawl https://www.example.com/ --out bing-crawl.tsv
```

Microsoft refreshes queries and pages weekly and crawl daily, so a daily job would add nothing. The report shows clicks and
impressions from the first file and the `Code5xx` trend from the second.

Check: the top rows of `bing-queries.tsv` match Search Performance for the same period, and a deleted test key produces
exit 1 with no key printed.

## Verify the setup and the API

Verification proves the site is connected, that the data is real, and that nothing leaks.

```bash
python3 scripts/bing_api.py quota https://www.example.com/        # expect DailyQuota and MonthlyQuota, exit 0
python3 scripts/bing_api.py crawl https://www.example.com/ --out crawl.tsv
grep -rIl "$BING_WEBMASTER_KEY" . --exclude-dir=.git              # expect no output; -l prints file names, never the key
```

1. The site shows as verified, and the sitemap as processed.
2. URL Inspection (Live URL) shows the rendered HTML, and the Index card shows the URL indexed.
3. In `crawl.tsv`, `BlockedByRobotsTxt`, `Code4xx` and `Code5xx` stay flat or fall after a release.
4. An export's top rows match the same report in the tools.

## Checklist for Bing Webmaster Tools

The checklist covers a new site and any integration.

1. Site added by import or verified by hand, with a sitemap submitted and a `Sitemap:` line in robots.txt.
2. More than one person can read the data.
3. No stray `crawl-delay` when Crawl control is in use.
4. "Ignore Robots.txt" stays off in production Site Scans.
5. Integrations call `/json/`, and parse the `{"d": ...}` wrapper.
6. The quota is read before any large batch.
7. API keys stay out of the repository, logs and tickets.
8. Submissions leave out URLs that must stay private.

## Gotchas in Bing Webmaster Tools

The gotchas below are what most often waste time in the tools and the API.

1. **API calls return 400 with `InvalidApiKey`.** Symptom: `{"ErrorCode":3,"Message":"InvalidApiKey"}`. Cause: a deleted
   key, or a key from another user. Fix: generate a new key in Settings; deleting one breaks every application using it.
2. **Old integrations went dark in September 2026.** Symptom: calls to `/pox/` or `/soap/` fail. Cause: both were
   retired on 31 August 2026. Fix: move to `/json/` and parse the `{"d": ...}` wrapper.
3. **Crawl control seems to do nothing.** Symptom: the hourly pattern is saved and the crawl rate stays the same. Cause:
   a `crawl-delay` line in robots.txt takes precedence. Fix: remove it.
4. **Content Submission leaks a blocked page.** Symptom: a URL disallowed in robots.txt appears in Bing. Cause: Bing
   does not honour a robots.txt disallow for content you submit, though it honours `noindex`. Fix: exclude those URLs
   from the feed.
5. **A blocked URL forgotten.** Symptom: a page stays out of Bing though nothing on the site blocks it. Cause: a Block URLs
   entry left in the tools; it lasts 90 days. Fix: read Block URLs before calling it a crawl problem.
6. **No data in the first days.** Symptom: reports stay empty after verifying. Cause: data takes about 48 hours and has no
   history from before the site was added. Fix: wait, and say so in the first report.
7. **Live URL stops at a redirect.** Symptom: URL Inspection shows the redirect, not the target. Cause: Bingbot fetches
   each redirect separately. Fix: inspect the final URL.

## Anti-patterns in Bing Webmaster Tools

Anti-patterns here spend quota or leak access.

| Do not | Do this instead |
|---|---|
| Pasting a key in a URL into logs or tickets | keep it in the environment and rotate it if it leaks |
| Building on URL or Content Submission for new work | use IndexNow, because both may be deprecated |
| Running a daily job on weekly data | match the job to the refresh: queries and pages weekly, crawl daily |
| Running Site Scan with "Ignore Robots.txt" in production | keep it off |
| Reading a site's quota from the documentation | read it with `bing_api.py quota`, because it can be lower |

## References for Bing Webmaster Tools

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/webmaster-api.md](references/webmaster-api.md): API methods, OAuth 2.0, errors, the retirement of SOAP
  and POX, and what stayed unconfirmed.
- `scripts/bing_api.py`: quota, queries, pages, crawl stats and URL submission through the JSON API.

## See also for Bing Webmaster Tools

- `bing-seo`: the guidelines, IndexNow, bingbot and what differs from Google
- `bing-ai-and-copilot`: AI Performance and the AI Training and AI Grounding preferences
- `search-console`: the Google counterpart
- `xml-sitemaps`: sitemap formats and limits
- `seo-measurement`: reporting Bing beside Search Console
