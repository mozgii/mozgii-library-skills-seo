---
title: Naver crawl request API, removal and site moves
author: MOZGII, Inc.
lang: en
tags: [naver, crawl-api, indexing, migration, removal]
description: The partner crawl request API, how to remove content from Naver, and the moves guide, written from Search Advisor's official pages.
---

# Naver crawl request API, removal and site moves

Naver's partner API and its removal and move procedures are the operations with real consequences, so this page keeps
the exact rules. Everything here comes from Search Advisor's guides, read on 31 October 2026.

## Who can use the partner crawl request API

The 수집요청 API is a partnership: a site that meets Naver's content volume criteria applies through Naver's partnership
proposal form (제휴 희망 사이트: 네이버, 제휴 구분: 웹사이트-수집요청 API). Once accepted, Webmaster Tools shows the API
status and an access token. A submitted URL gets a higher crawl priority than ordinary discovery.

Before calling it, check three things. The site must pass the ownership check with the exact scheme, `www` and port
used in calls. Yeti must be allowed to fetch each URL under robots.txt. And each URL must be the final landing page that
a browser shows, in canonical form: a redirecting URL counts as an update failure.

## Submit and verify URLs through the API

The API has two endpoints and accepts only HTTPS with TLS 1.2 or later.

| Endpoint | Purpose |
|---|---|
| `POST https://apis.naver.com/searchadvisor/crawl-request/submit.json` | send URLs to update or delete; counts against the daily limit |
| `POST https://apis.naver.com/searchadvisor/crawl-request/verify.json` | check the syntax of the same payload |

```bash
curl -sS -X POST https://apis.naver.com/searchadvisor/crawl-request/verify.json \
  -H "Authorization: Bearer $NAVER_CRAWL_TOKEN" -H 'Content-Type: application/json' \
  -d '{"urls":[{"url":"https://www.example.co.kr/menu/spring","type":"update"},
               {"url":"https://www.example.co.kr/menu/winter","type":"delete"}]}'
```

| Rule | Value |
|---|---|
| URLs per call | 1,000 at most |
| Payload | 2 MB at most |
| `type` | `update` sends Yeti to the URL; `delete` removes it from Naver's store with no visit |
| Same URL in both | delete wins |
| Daily limit | set per partner, counted by URLs; past it, further URLs are dropped |
| Spread | send in small batches over the day, because a burst sends Yeti to the site in a spike |

A success looks like `{"errorCode":0,"message":"Success","result":{"totalUpdateCount":1,...}}`, and verify answers
`"result":"valid"`. The report at 리포트 › 제휴 API 현황 refreshes every 24 hours: a rising 업데이트실패 count means bad
URLs or a site fault.

| HTTP | Code | Meaning |
|---|---|---|
| 200 | 000 | success |
| 401 | 024, 028, 029 | authentication failed, header missing or unreadable |
| 401 | 1003 | site ownership not confirmed |
| 401 | 1004 | not a partner site |
| 402 | 1005 | daily request limit used up; later URLs are not collected |
| 403 | 030, 071 | HTTPS required, return format unsupported |
| 404 | 051, 052 | no such API, no such partner |
| 400 | 061, 063, 1001, 1002 | bad URL, encoding, header parameter or payload |
| 406 | 1000 | no requestable URL in the payload |
| 413 | 064 | payload over 2 MB |
| 500 | 1030, 1031 | server errors; retry later |

The token is a bearer secret. Keep it in the environment, and never print it or commit it.

## Remove content from Naver

Naver removes results only for legal or policy breaches, so removal starts on your own site. Removal is not instant
because it needs a re-index.

1. Delete the page and confirm it returns 404 (or 403) to Yeti.
2. In Webmaster Tools, go to 요청 › 웹 페이지 검색 제외, and enter the URL.
3. Wait for the index to update.

To keep a page live but out of search, use `noindex`. Do not add a robots.txt block first: Yeti must revisit to see the
404 or the tag. Add a block only after the pages have left results. A page with its original still online can return.
For someone else's site, ask its owner or its host, found through WHOIS. With a court order, contact Naver's customer
centre.

## Move a site to a new domain

Moves take time because a quality score has to carry over from the old host, and frequent moves damage it. Naver advises
moving small and mid-sized sites all at once, and moving only for a real reason such as a rebrand.

1. Copy the content, images and files to the new site, and point the domain at it. DNS recognition can take 2 to 3 days.
2. Run the simple site check on the new address.
3. Allow everything in the new robots.txt, and 301 each old URL to its exact new URL.
4. Set a canonical on every new page, so old URLs do not stay as the displayed ones.
5. Register the new site, and submit its sitemap.
6. Watch collection and indexing. Quality recovers over time.
7. Use 수집요청 on any old URLs still showing. Close the old server and remove it from the tools only when traffic to it
   has stopped.

Keep redirect chains under five hops, and keep every hop collectable: a robots-blocked step in the middle stops the
chain. Use 302 for a brief outage or temporary page. To close a site for good, announce it at least a month before, cut
off write access, and keep the domain: an expired domain can pass to spam or adult sites and shame the old brand.
