---
title: SEO audit checklist by area
author: MOZGII, Inc.
lang: en
description: The full SEO audit checklist per area, with the tool or command that answers each check.
---

# SEO audit checklist by area

This checklist lists every check of a full SEO audit, grouped by area, with the tool that answers it. Run the areas
in order; skip an area only when it does not apply and say so in the report.

## Contents

1. Access and setup
2. Crawling
3. Indexing
4. Canonicals and duplicates
5. Redirects and status codes
6. Sitemaps
7. Rendering and JavaScript
8. Page metadata and content
9. Structured data
10. Page experience
11. Internal links and architecture
12. International
13. Off-site and reputation
14. AI search
15. Spam and security

## 1. Access and setup

The access and setup checks confirm the auditor sees what the search engines see.

- Search Console verified as a **domain property** (`sc-domain:example.com`), covering every protocol and subdomain.
- Bing Webmaster Tools verified (it can import from Search Console); Yandex Webmaster when Russian-speaking markets
  matter.
- Manual actions report and Security issues report in Search Console: empty, or each item listed as a finding.
- Analytics records organic sessions separately per search engine; the tracking tag is on every template.

## 2. Crawling

The crawling checks confirm that crawlers can fetch every page that should rank and do not waste requests on pages
that should not.

| Check | How |
|---|---|
| robots.txt answers 200 (or 404 for "no rules"), never 5xx | `curl -sI https://example.com/robots.txt` |
| No important path disallowed; CSS and JS allowed | read the file; test URLs in Search Console's robots.txt report |
| `Sitemap:` lines point to live sitemaps | `curl -s https://example.com/robots.txt \| grep -i sitemap` |
| Server answers fast and without errors to crawlers | Search Console › Settings › Crawl stats: response time, host status |
| No crawl traps (infinite calendars, session IDs, endless filters) | crawl report: URL patterns with thousands of near-identical URLs |
| Log files show Googlebot reaching money pages | `grep -i googlebot access.log \| awk '{print $7}' \| sort \| uniq -c \| sort -rn \| head` |

Verify that a "Googlebot" in logs is real: a reverse DNS lookup ends in `googlebot.com` or `google.com`, and the
forward lookup returns the same IP (`host 66.249.66.1`, then `host crawl-66-249-66-1.googlebot.com`). Or match the IP
against Google's published list, `https://developers.google.com/static/crawling/ipranges/common-crawlers.json`.

## 3. Indexing

The indexing checks confirm that pages that should rank are indexed and pages that should not are kept out.

- Page indexing report: count of indexed pages against the number of canonical pages the site has.
- Top exclusion reasons explained: "Crawled - currently not indexed", "Discovered - currently not indexed",
  "Duplicate without user-selected canonical", "Alternate page with proper canonical tag", "Excluded by noindex tag",
  "Soft 404", "Blocked by robots.txt".
- `noindex` only where intended: search the crawl for `noindex` in meta robots and `X-Robots-Tag`.
- No staging, test or internal search result pages indexed (`site:` searches on suspicious paths and hosts).

## 4. Canonicals and duplicates

The canonical checks confirm that each document has one URL and every signal points to it.

- Every indexable page has an absolute, self-referencing canonical to a URL that answers 200.
- http to https, bare domain to www (or back), trailing slash and upper case each resolve with one 301.
- Parameters for tracking, sorting and sessions canonicalise to the clean URL.
- Paginated pages canonicalise to themselves, not to page 1.
- Near-duplicate pages (same template, swapped word) are merged or made distinct.

## 5. Redirects and status codes

The redirect checks confirm that moved content passes its signals in one hop.

- No redirect chains longer than one hop on internal links; no loops.
- Permanent moves use 301 or 308; 302 and 307 only for temporary changes.
- Removed pages answer 404 or 410, not a redirect to the home page and not a 200 "not found" page.
- `python3 scripts/page_check.py <url>` shows `redirect_hops` 0 for every internal link target.

## 6. Sitemaps

The sitemap checks confirm the sitemaps list exactly the canonical, indexable URLs.

- `python3 scripts/sitemap_check.py https://example.com/` passes: parses, under the limits, same host, valid
  lastmod, sampled URLs indexable.
- Sitemap URL count is close to the indexable page count from the crawl.
- Search Console Sitemaps report: last read date recent, no errors.

## 7. Rendering and JavaScript

The rendering checks confirm the main content, links and metadata are in the HTML Google renders.

- URL Inspection › View crawled page › HTML: title, canonical, H1, main text and links present.
- Links are `<a href="...">` elements; no navigation that works only through `onclick`.
- No content that needs a click, scroll or login to load.
- Client-side routing returns real 404 status codes (or `noindex`) for missing pages.
- Raw HTML under 2 MB uncompressed (`page_check.py` field `html_bytes`); Googlebot ignores what comes after.

## 8. Page metadata and content

The page-level checks confirm each page states its topic once and well.

- Unique `<title>` and meta description per page; no template-wide duplicate.
- One H1 per page that matches the page's main topic.
- No thin pages (doorways, empty categories, tag pages with one post) indexed.
- Images that carry information have descriptive `alt` text; text inside images repeated in HTML.

## 9. Structured data

The structured data checks confirm markup is valid, eligible and true.

- Rich Results Test passes for each template; Search Console enhancement reports have no errors.
- Markup matches visible content (prices, ratings, dates, author).
- Markup for features Google has retired (FAQ and HowTo rich results, among others) wins nothing in Google. It is
  harmless, so never report it as an error; just do not add it for those results.

## 10. Page experience

The page experience checks read real-user data first and lab data second.

- Core Web Vitals report in Search Console: URLs grouped as Poor or Need improvement, per template.
- CrUX data for the origin (PageSpeed Insights): LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at the 75th percentile.
- HTTPS everywhere with a valid certificate; no mixed content.
- No interstitial that hides the main content on mobile on arrival from search.

## 11. Internal links and architecture

The architecture checks confirm that link equity reaches the pages that need it.

- Money pages within three clicks of the home page.
- No orphan pages (in the sitemap or analytics, but with no internal links).
- Descriptive anchor text; breadcrumbs on deep templates.

## 12. International

The international checks apply when a site serves more than one language or country.

- Each template's hreflang set is complete: every version lists itself and every other version, and each listed
  URL lists the page back (compare the `hreflang` field of `page_check.py` across the versions).
- Codes are valid (`en-GB`, not `en-UK`); each version's canonical is itself.
- No automatic redirect by IP or browser language that hides versions from crawlers.

## 13. Off-site and reputation

The off-site checks look at signals the site does not control directly.

- Backlink profile reviewed for paid or spam links that need `rel="sponsored"` or removal.
- Brand search results: the site, its profiles and reviews show what the owner expects.

## 14. AI search

The AI search checks confirm the site can appear in AI answers and that its controls are set on purpose.

- robots.txt rules for AI crawlers (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Google-Extended) match the
  owner's decision; Googlebot is never blocked to stop AI Overviews.
- Search Console generative AI performance report and Bing AI Performance read for the main pages.
- Details: the `ai-search-visibility` skill.

## 15. Spam and security

The spam and security checks confirm nothing on the site invites a demotion or a penalty.

- Search Console › Security and manual actions: Manual actions and Security issues both empty.
- No back button hijacking: from a Google result, open the page on a phone and press Back; you land on the results.
- No third-party sections (coupons, casino, loans) hosted mainly for the host's ranking strength.
- No sets of generated pages without unique data; no city-swap doorways.
- `site:example.com` with spam words (casino, viagra, loan) shows no injected pages.
