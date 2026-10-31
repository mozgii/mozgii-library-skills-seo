---
title: Page indexing report reasons
author: MOZGII, Inc.
lang: en
description: Every reason in Search Console's Page indexing report, what causes it and how to fix or accept it.
---

# Page indexing report reasons

The Page indexing report in Google Search Console lists why known URLs are not indexed. Each reason below gives the
usual cause and the fix. Many reasons are correct behaviour: the question is always whether the URL should be
indexed.

## Contents

1. Reasons that are usually intended
2. Reasons that need a technical fix
3. Reasons about quality or priority
4. Canonical reasons
5. Working through the report

## Reasons that are usually intended

These Page indexing reasons are fine when the URL should not rank; fix them only for pages that should.

| Reason | Cause | Fix when the page should rank |
|---|---|---|
| Excluded by 'noindex' tag | meta robots or `X-Robots-Tag` noindex | remove the directive (check the CDN and plugins too) |
| Blocked by robots.txt | a `Disallow` rule matches | change the rule; test in the robots.txt report |
| Page with redirect | the URL redirects | none: list and link the target instead |
| Not found (404) | the URL does not exist | none if gone; 301 to the replacement if it moved |
| Alternate page with proper canonical tag | the page names another URL as canonical | none: this is the canonical working |

## Reasons that need a technical fix

These Page indexing reasons point to a server or code problem.

| Reason | Cause | Fix |
|---|---|---|
| Server error (5xx) | the server failed or timed out for Googlebot | capacity, timeouts, firewall rules that block Googlebot; Crawl stats shows when |
| Redirect error | a loop, a chain too long, an empty or bad URL in `Location` | one hop to a 200 URL |
| Blocked due to unauthorized request (401) | login or HTTP auth | remove auth for public pages |
| Blocked due to access forbidden (403) | WAF, bot protection, geo-block | allow verified Googlebot IPs |
| Blocked due to other 4xx issue | another 4xx | find the code with URL Inspection |
| Soft 404 | 200 with empty or "not found" content | return 404, or give the page real content |
| Indexed, though blocked by robots.txt | indexed from links without a crawl | allow crawling and add `noindex`, or allow and keep it |

## Reasons about quality or priority

These Page indexing reasons mean Google chose not to index the URL, or not yet.

**Crawled - currently not indexed.** Google fetched the page and left it out. Usual causes: thin or near-duplicate
content, a page that adds nothing to what is indexed, or a new page waiting its turn. Fix by making the page clearly
useful and distinct, merging it into a stronger page, or linking it from relevant indexed pages. Do not request
indexing repeatedly.

**Discovered - currently not indexed.** Google knows the URL but has not fetched it. Usual causes: the host was slow
or overloaded so Google postponed, too many low-value URLs compete for crawl, or the page has few internal links. Fix
server speed, cut duplicate URL spaces, and link the page from crawled pages.

## Canonical reasons

These Page indexing reasons mean the URL is a duplicate and another URL is indexed in its place.

| Reason | Meaning | Fix |
|---|---|---|
| Duplicate without user-selected canonical | duplicates exist and no canonical is set | add self canonicals on the main URL, canonicals to it on the others |
| Duplicate, Google chose different canonical than user | your canonical was overruled | make all signals agree: redirects, internal links, sitemap, hreflang |
| Duplicate, submitted URL not selected as canonical | a sitemap URL lost to another | list the canonical URL in the sitemap instead |

## Working through the Page indexing report

The Page indexing report is read top-down by URL count, against the list of pages that should rank.

1. Export each reason's example URLs (up to 1,000 per reason in the interface; more through the URL Inspection API).
2. Group the URLs by template or path pattern.
3. For each group decide: should rank (fix) or should not (accept, or stop generating the URLs).
4. Fix the template, then use **Validate fix** in the report to track recrawl.
5. Expect days to weeks for the counts to move; large sites take longer.
