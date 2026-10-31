---
name: crawling-and-indexing
description: 'Diagnoses and fixes why pages are not crawled or not indexed, and keeps unwanted pages out of the index: robots.txt rules, meta robots and X-Robots-Tag, noindex, HTTP status codes, soft 404s, crawl budget, JavaScript rendering, removals, and diagnosing one URL from its status to its indexed record. Use when a page is missing from Google or Bing, a page must be removed from search, a crawler is blocked or wasted, or robots.txt needs writing or review.'
metadata:
  tags:
  - seo
  - crawling
  - indexing
  - robots-txt
  - noindex
  - javascript-seo
  - search-console
---

# Crawling and indexing

A page reaches search results in three stages: a crawler fetches it, the search engine renders and indexes it, and
ranking systems choose it for a query. This skill owns the first two stages: getting the right pages fetched and
indexed, and keeping the wrong ones out.

## Step 0: read what the site serves crawlers today

Read the live answers first, because a CDN, a plugin or a host can change them without anyone editing a file. The first
command saves robots.txt with its status, the second lists its rules, and the third reads the home page's redirect chain
and headers.

```bash
curl -s -o robots.txt -w 'robots.txt %{http_code}, %{size_download} bytes\n' https://www.example.com/robots.txt
grep -inE '^(user-agent|allow|disallow|sitemap):' robots.txt | head -40
curl -sIL https://www.example.com/ | grep -iE '^(HTTP/|server:|location:|x-robots-tag:)'
```

Then note how many pages the site has, which matters for crawl budget, whether a CDN or WAF sits in front of it, and
who can read Search Console and the server logs.

## Crawl, index and serve: the three controls

Crawling, indexing and serving each have their own control, and mixing them up causes most indexing bugs.

| Goal | Control | Not this |
|---|---|---|
| Stop crawling a path | `Disallow` in robots.txt | `noindex` (needs a crawl to be seen) |
| Keep a page out of the index | `<meta name="robots" content="noindex">` or `X-Robots-Tag: noindex`, crawling allowed | robots.txt (a blocked URL can still be indexed from links, without a snippet) |
| Remove a page for good | 404 or 410 | a redirect to the home page (Google treats it as a soft 404) |
| Hide it fast from Google results | Search Console › Removals (about six months), then one of the above | removals alone (it expires) |
| Choose between duplicates | `rel="canonical"` or a 301 | `noindex` on the duplicate (`canonical-urls` skill) |
| Limit the snippet | `nosnippet`, `max-snippet:[n]`, `data-nosnippet` | robots.txt |
| Keep link-shared or utility pages out (shared carts, lists, pastes, documents) | `noindex` by default, set when the page is created | waiting for spam to appear on them |

## Diagnose one URL that is not indexed

The single-URL diagnosis runs from the cheapest check to the most expensive, and stops at the first failure.

1. **Status and robots**: fetch the URL as Googlebot and read the redirect chain, the headers and the robots and
   canonical tags. Status must be 200 in one hop; no `noindex` in `X-Robots-Tag` or meta robots; the canonical is
   the URL itself.

```bash
UA='Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
curl -sIL -A "$UA" https://example.com/page | grep -iE '^(HTTP/|location:|x-robots-tag:)'
curl -sL -A "$UA" https://example.com/page | grep -ioE '<meta[^>]+name="(robots|googlebot)"[^>]*>|<link[^>]+rel="canonical"[^>]*>'
```

2. **robots.txt**: is the path disallowed for `Googlebot` or `*`? Read the file; Search Console › Settings ›
   robots.txt shows the version Google fetched and when.
3. **URL Inspection** in Search Console: "URL is on Google" or the reason it is not; "Google-selected canonical";
   "Page fetch"; "Indexing allowed?". Then **Test live URL** and read the rendered HTML and screenshot.
4. **Discovery**: is the URL in a sitemap and linked from at least one indexed page with a normal `<a href>`?
5. **Quality and duplication**: does the page add something the index does not already have? A near-duplicate or
   thin page is often crawled and left out on purpose.
6. **Request indexing** in URL Inspection only after fixing the cause; it does not override a quality decision.

Bing: URL Inspection in Bing Webmaster Tools gives the same answers; submit with IndexNow (`xml-sitemaps` skill).

Search Console's Page indexing report names a reason for each URL it left out, such as Crawled - currently not indexed.
Every reason, what it means and its fix: the `search-console` skill.

## robots.txt rules that matter

robots.txt controls crawling only, per user agent, by path prefix. Google reads the first 500 KiB, matches the most
specific (longest) rule, and lets `Allow` win a tie with `Disallow`. A 4xx answer for robots.txt (except 429) means
"no restrictions". A 5xx answer stops crawling of the site for the first 12 hours while Google keeps retrying; for the
next 30 days it uses the last good copy of the file, still retrying. With no cached copy it assumes no restrictions,
and after the 30 days it behaves as if the site had no robots.txt, as long as the site is generally reachable. Google
normally caches the file for up to 24 hours. Syntax, wildcards, per-engine differences and tested examples are in
[references/robots-txt.md](references/robots-txt.md).

A minimal robots.txt for a typical site:

```text
User-agent: *
Disallow: /cart/
Disallow: /search
Disallow: /*?sessionid=

Sitemap: https://www.example.com/sitemap.xml
```

## Meta robots and X-Robots-Tag directives

Meta robots and the `X-Robots-Tag` header carry the same directives; the header also works for PDFs, images and
other non-HTML files.

```html
<meta name="robots" content="noindex, follow">
<meta name="googlebot" content="max-snippet:160, max-image-preview:large">
```

```text
X-Robots-Tag: noindex
X-Robots-Tag: googlebot: nosnippet
```

Directives Google supports: `noindex`, `nofollow`, `none` (= noindex, nofollow), `nosnippet`, `max-snippet:[n]`,
`max-image-preview:[none|standard|large]`, `max-video-preview:[n]`, `notranslate`, `noimageindex`,
`unavailable_after:[date]`, `indexifembedded`. `data-nosnippet` on an HTML element keeps that part out of snippets
and AI answers. When directives conflict, the most restrictive one wins.

Apache header for all PDFs:

```apache
<FilesMatch "\.pdf$">
  Header set X-Robots-Tag "noindex"
</FilesMatch>
```

nginx equivalent: `location ~* \.pdf$ { add_header X-Robots-Tag "noindex"; }`.

## HTTP status codes and what search engines do with them

Status codes tell crawlers what happened, and each one has a defined effect on indexing.

| Code | Effect |
|---|---|
| 200 | content may be indexed |
| 301, 308 | permanent: signals move to the target; the target is usually indexed |
| 302, 303, 307 | temporary: the source usually stays indexed; a long-lived 302 is treated like a 301 over time |
| 304 | not modified: the crawler reuses its copy (good for crawl efficiency) |
| 404, 410 | removed from the index after recrawl; 410 may be slightly faster; neither hurts the rest of the site |
| 429, 500, 503 | crawl rate drops; pages fall out if errors persist; use 503 with `Retry-After` for planned downtime |

## Crawl budget for large sites

Crawl budget is the number of URLs a search engine will fetch from a host in a period. It only matters for large
sites (Google's guide gives rough figures: 1 million or more unique pages changing about weekly, or 10,000 or more
changing daily) or for slow servers.
Raise it by answering fast, returning 304 for unchanged pages, removing duplicate and infinite URL spaces (filters,
calendars, session IDs), and keeping internal links and sitemaps to canonical URLs. Watch Search Console › Crawl
stats for response time and host status. Google ignores `Crawl-delay`; Bing honours it. Server logs show where the crawl
actually goes: [references/server-logs.md](references/server-logs.md).

## JavaScript, rendering and the 2 MB limit

JavaScript sites get indexed when the rendered HTML carries the content and the links. Google renders every page
that answers 200 in an evergreen Chromium after the first fetch; Bing renders too, but other crawlers, social
previews and many AI fetchers read the raw HTML only. The rules that matter most for indexing:

- Server-side rendering or static generation for indexable content; links as `<a href>` with real paths.
- No `noindex` in the first HTML of a page that should be indexed: JavaScript cannot reliably remove it.
- Scripts, styles and API routes the page needs are not disallowed in robots.txt; blocked resources are not
  rendered.
- Googlebot reads only the first 2 MB of an HTML file and of each CSS or JavaScript file, uncompressed (64 MB for a
  PDF); content after the cut is not indexed.

Framework detail, single-page app status codes and testing: the `javascript-seo` skill.

## Removing content from search

Removing a page from search results takes a permanent signal plus, when it is urgent, a temporary hide.

1. Serve 404 or 410 (content gone) or `noindex` (content stays for users), and leave crawling allowed.
2. For urgent cases use Search Console › Removals › New request (hides for about six months) and Bing Webmaster
   Tools › Block URLs.
3. For outdated content on someone else's site, use Google's Refresh Outdated Content tool.
4. Confirm with URL Inspection after recrawl.

## Worked example: new articles are "Discovered - currently not indexed"

Situation: a publisher's new articles stay "Discovered - currently not indexed" for weeks; older ones are indexed.

Checks in order: the article URLs answer 200, no `noindex`, self canonical, allowed in robots.txt. Crawl stats show
the average response time rose from 300 ms to 2.1 s after a hosting change, and 60% of Googlebot requests in the
server logs go to `/tag/` and `?replytocom=` URLs. Fix: restore server speed (cache HTML at the CDN), `noindex` and
stop linking thin tag pages, remove `replytocom` links, list new articles in a news or recent sitemap and link them
from the home page. Check: Crawl stats response time back under 500 ms; new articles indexed within days.

## Verify crawling and indexing fixes

Check the fix in the order Google meets it: robots.txt, the page, then Google's own record of the page. These two
commands read the live answers:

```bash
curl -s -o /dev/null -w 'robots.txt %{http_code}\n' https://www.example.com/robots.txt      # expect 200 or 404, never 5xx
curl -sIL https://www.example.com/shoes/ | grep -iE '^(HTTP/|x-robots-tag:)'                # expect one 200, no noindex
```

The URL Inspection API gives Google's indexed record for each changed URL, at about 2,000 calls per property a day. It
needs a token with a Search Console scope, in `GSC_TOKEN`:

```bash
curl -s -X POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect \
  -H "Authorization: Bearer $GSC_TOKEN" -H 'Content-Type: application/json' \
  -d '{"inspectionUrl":"https://www.example.com/shoes/","siteUrl":"sc-domain:example.com"}' \
| python3 -c "import json,sys; r=json.load(sys.stdin)['inspectionResult']['indexStatusResult'];
print({k: r.get(k) for k in ('verdict','coverageState','robotsTxtState','indexingState','pageFetchState','googleCanonical','userCanonical','lastCrawlTime')})"
```

| Goal | Expect |
|---|---|
| The page should rank | `verdict` PASS, `robotsTxtState` ALLOWED, `indexingState` INDEXING_ALLOWED, `pageFetchState` SUCCESSFUL, `googleCanonical` equal to `userCanonical` |
| The page should stay out | `indexingState` BLOCKED_BY_META_TAG or BLOCKED_BY_HTTP_HEADER, with `robotsTxtState` ALLOWED so the signal is seen |
| A fix has been seen | `lastCrawlTime` later than the release |

The record shows the last crawl, so an old `lastCrawlTime` means Google has not seen the fix yet. Then read the Page
indexing report for the reason you targeted, and Crawl stats for the host, over the following weeks.

## Checklist for crawling and indexing

The checklist confirms a site is crawlable and only the right pages are indexed.

1. robots.txt answers 200 or 404, never 5xx; important paths and CSS and JS are allowed.
2. Pages that should rank: 200, no `noindex`, self canonical, in the sitemap, linked internally.
3. Pages that should not rank: `noindex` or 404, crawlable so the signal is seen; or disallowed when crawl load is
   the problem and they are not indexed.
4. Page indexing report: top exclusion reasons explained, none hitting money pages.
5. Rendered HTML (URL Inspection) contains the main content and links.
6. Crawl stats: average response time stable, no host status problems.

## Gotchas in crawling and indexing

The gotchas below cause most "my page vanished" tickets.

1. **noindex plus Disallow.** Symptom: a page with `noindex` stays in the index for months. Cause: the crawler never
   sees the `noindex`, so the URL can stay indexed. Fix: remove the `Disallow` until the page drops out.
2. **noindex left from staging.** Symptom: a launch day traffic drop, with pages leaving the index. Cause: the launch
   ships the staging `noindex` or an `X-Robots-Tag` set at the CDN. Fix: check the headers on production after every
   release.
3. **Soft 404 from empty templates.** Symptom: Search Console reports Soft 404 on search or category pages. Cause:
   empty pages answer 200 with "0 results". Fix: return 404 or `noindex` for them.
4. **robots.txt 5xx.** Symptom: crawling of the whole host stops, and Crawl stats show host status problems. Cause: a
   broken robots.txt stops crawling for the first 12 hours; for the next 30 days Google uses the last good copy, so
   new rules are not read. Fix: fix the server error and monitor the file like the home page.
5. **Lazy content behind scroll or click.** Symptom: text visible in a browser is missing from the rendered HTML.
   Cause: Googlebot does not click or scroll, so content loaded on interaction is not indexed. Fix: load it in the
   HTML or on page load.
6. **Fragment URLs.** Symptom: many views are indexed as one page. Cause: Google ignores everything after `#`;
   `/#/products/1` is one URL. Fix: use the History API with real paths.
7. **Requesting indexing again and again.** Symptom: the page stays out and the quota runs out. Cause: the request
   does not change a quality decision, and it has a daily quota. Fix: improve or merge the page.

## Anti-patterns in crawling and indexing

Anti-patterns in crawl control mix up the controls in the table at the top of this skill.

| Do not | Do this instead |
|---|---|
| Using robots.txt to remove a page from search | serve `noindex` or 404 with crawling allowed |
| Redirecting deleted pages to the home page | return 404 or 410, or redirect to a real equivalent |
| Blocking CSS, JavaScript or API routes to save crawl | keep what rendering needs crawlable |
| Relying on Removals alone | pair the temporary hide with a permanent signal, because it expires |
| Treating `Crawl-delay` as a Google control | it is ignored by Google; fix server capacity and let Crawl stats show the effect |

## References for crawling and indexing

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/robots-txt.md](references/robots-txt.md): syntax, matching, wildcards, per-engine differences,
  examples, testing.
- [references/server-logs.md](references/server-logs.md): reading access logs for crawl analysis, verifying
  Googlebot, Bingbot and AI crawlers, and the log checks behind crawl budget decisions.

## See also for crawling and indexing

- `search-console`: Page indexing reasons, the Indexing API and URL Inspection at scale
- `canonical-urls`: choosing between duplicates
- `javascript-seo`: rendering, single-page apps and framework recipes
- `xml-sitemaps`: discovery through sitemaps and IndexNow
- `seo-audit`: where these checks sit in a full audit
- `ai-search-visibility`: AI crawler policy
- `bing-seo`, `naver-search-advisor`, `yandex-seo`: bingbot, Yeti and YandexBot, with each engine's crawl tools
