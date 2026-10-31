---
title: Bing Webmaster API reference
author: MOZGII, Inc.
lang: en
tags: [bing, webmaster-api, oauth, url-submission, rest]
description: JSON endpoints, authentication, errors and method groups of the Bing Webmaster API, with what could not be confirmed.
---

# Bing Webmaster API reference

The Bing Webmaster API gives programmatic access to a verified site's traffic, crawl, link and keyword data, and accepts
URL, sitemap and site changes. The official documentation is at <https://learn.microsoft.com/en-us/bingwebmaster/>.

## JSON endpoints and the SOAP retirement

JSON over HTTP is the only supported protocol: SOAP and POX were retired on 31 August 2026 with no change to methods,
parameters, keys or quotas. WSDL is gone too.

```text
GET  https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl=https://www.example.com/&apikey=KEY
POST https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=KEY
Content-Type: application/json; charset=utf-8
```

| Part | Shape |
|---|---|
| POST body | a flat JSON object, one property per parameter |
| Success | `{"d": ...}`, with `d` null on writes such as `SubmitUrlBatch` |
| Failure | HTTP 400 and `{"ErrorCode": 3, "Message": "InvalidApiKey"}`, with no `d` |
| Dates | `/Date(1316156400000-0700)/`, milliseconds since 1970 |
| Enums | integers |
| `__type` | informational, ignore it |

## Authentication with a key or OAuth 2.0

Microsoft recommends OAuth 2.0 and also supports an API key.

**API key:** Settings › API Access in Webmaster Tools. One key per user, valid for all of that user's verified sites.
Deleting it breaks every application that uses it. It travels in the query string, so keep request URLs out of logs.

**OAuth 2.0:** register a client under API Access (name and redirect URI), then run the authorization code flow.

| Step | Value |
|---|---|
| Authorize | `GET https://www.bing.com/webmasters/oauth/authorize` with `response_type=code`, `client_id`, `redirect_uri`, `scope` |
| Exchange | `POST https://www.bing.com/webmasters/oauth/token` (form encoded) with `client_id`, `client_secret`, `code`, `grant_type=authorization_code`, `redirect_uri` |
| Refresh | the same URL with `grant_type=refresh_token` and `refresh_token` |
| Call | `Authorization: Bearer ACCESS_TOKEN` |
| Scopes | `webmaster.read`, `webmaster.manage` |

The authorization code lasts 5 minutes. The sample token lifetime is 3,599 seconds, and refresh tokens last until the
user revokes access. The redirect URI must match exactly, including case and trailing slash. The sample call there uses
the host `www.bing.com` rather than `ssl.bing.com`.

## Method groups worth knowing

The interface holds about 60 methods; these are the ones an SEO workflow uses.

| Goal | Methods |
|---|---|
| Sites | `GetUserSites`, `AddSite`, `VerifySite`, `RemoveSite`, `GetSiteRoles`, `AddSiteRoles`, `RemoveSiteRole` |
| Traffic | `GetRankAndTrafficStats`, `GetQueryStats`, `GetPageStats`, `GetQueryPageStats`, `GetPageQueryStats`, `GetQueryTrafficStats` |
| Crawl and index | `GetCrawlStats`, `GetCrawlIssues`, `GetUrlInfo`, `GetChildrenUrlInfo`, `GetCrawlSettings`, `SaveCrawlSettings` |
| Submission | `SubmitUrl`, `SubmitUrlBatch`, `GetUrlSubmissionQuota`, `SubmitContent`, `GetContentSubmissionQuota` |
| Sitemaps | `SubmitFeed`, `GetFeeds`, `GetFeedDetails`, `RemoveFeed` |
| Links | `GetLinkCounts`, `GetUrlLinks`, `AddConnectedPage`, `GetConnectedPages` |
| Keywords | `GetKeyword`, `GetKeywordStats`, `GetRelatedKeywords` |
| Blocks | `AddBlockedUrl`, `GetBlockedUrls`, `RemoveBlockedUrl` |
| URL parameters | `GetQueryParameters`, `AddQueryParameter`, `RemoveQueryParameter`, `EnableDisableQueryParameter` |
| Site moves | `SubmitSiteMove`, `GetSiteMoves` |

`GetQueryStats` and `GetPageStats` return `Query`, `Date`, `Clicks`, `Impressions`, `AvgClickPosition` and
`AvgImpressionPosition`, refreshed weekly (for pages, `Query` holds the URL). `GetCrawlStats` covers the last six
months, refreshed daily, with `CrawledPages`, `CrawlErrors`, `InIndex`, `InLinks`, `BlockedByRobotsTxt`, status code
counts and `ContainsMalware`. `GetUrlSubmissionQuota` returns `DailyQuota` and `MonthlyQuota`.

## URL and Content Submission limits

Both APIs reach Bing alone, and Microsoft strongly recommends IndexNow and says they may be deprecated.

| Limit | Value |
|---|---|
| URL Submission | up to 10,000 URLs per domain per day, up to 500 per batch |
| Reset | midnight UTC |
| Scope | domain, not subdomain |
| Content Submission | up to 10 MB uncompressed per submission, gzip accepted; base64 of the whole HTTP message |
| Availability | Microsoft states 99.9% for URL Submission |

Submitting 404s and redirects is allowed and helps Bing retire dead links. Throttle large changes. Bing does not
honour a robots.txt disallow for submitted content, but it honours `noindex`. A quota can be raised through a support
ticket.

## What could not be confirmed

These gaps were open on 31 October 2026, so test before relying on them.

- The URL Submission help page says OAuth 2.0 is required, yet its own samples, the method pages and the retirement
  guide all use `apikey`. Treat both as working until Microsoft says otherwise, and prefer OAuth for new work.
- `bing_api.py` was tested against a local stub built from the documented samples, not against the live API, because
  that needs a verified site's key.
- The Learn pages for methods date from 2023 and still show POX samples beside the JSON ones.
