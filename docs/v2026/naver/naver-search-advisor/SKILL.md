---
name: naver-search-advisor
description: 'Gets a site collected and indexed by Naver through Search Advisor (서치어드바이저): Webmaster Tools setup and the ownership check, the Yeti crawler and how to confirm it, robots rules by status code, sitemap and RSS submission, crawl requests, the partner crawl request API, IndexNow on Naver, the reports that find indexing problems, removal and site moves. Includes a no-login page check. Use for 서치어드바이저, 웹마스터도구, 소유확인, 수집요청, 사이트맵 제출, 수집 현황, 사이트 진단, Yeti, a site missing from Naver, an ownership check that fails, or an API error from Naver.'
metadata:
  tags:
  - seo
  - naver
  - search-advisor
  - korea
  - yeti
  - indexnow
---

# Naver Search Advisor

Search Advisor is Naver's site for webmasters, and its Webmaster Tools console is the only source of reports on how Naver
reads a site. Naver runs its own crawler, Yeti, with its own rules, so a site that ranks in Google can still be absent here.
This skill registers the site, gets it collected and indexed, and proves it. Titles, Blog and AI Briefing belong to
`naver-seo`.

Naver's official guides are in Korean, at `searchadvisor.naver.com/guide`. All 54 were read for this skill on 31 October
2026 and written here in English, keeping the Korean terms you will meet in the tools.

## Korean terms in Naver's tools

Search Advisor's menus and reports use the terms below, and most advice online quotes them.

| Korean | Reads | Meaning |
|---|---|---|
| 서치어드바이저 | Search Advisor | the whole site for webmasters |
| 웹마스터도구 | Webmaster Tools | the console inside it |
| 소유확인 | ownership check | proving the site is yours |
| 수집 | collection | crawling |
| 색인 | index | indexing |
| 수집요청 | crawl request | asking Yeti to fetch a URL |
| 웹 페이지 검색 제외 | exclude from search | a removal request |
| 사이트 진단 | site diagnosis | the indexing report |
| 수집 현황 | crawl status | crawl errors |
| 사이트 간단 체크 | simple site check | a live test of any site |
| 대표 URL, 선호 URL | representative URL | canonical |
| 스팸, 어뷰징 | spam, abusing | policy violations |
| 제휴 API | partner API | the crawl request API |

## Step 0: read what the site already has

Step 0 fits the advice to the site before anything changes.

1. Whether a Naver account already owns the site in Webmaster Tools.
2. Which host serves the canonical URLs, because scheme, `www` and port each make a separate site.
3. What the page returns today:

```bash
python3 scripts/naver_check.py https://www.example.co.kr/
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

Then run the same URL through the public simple site check at `searchadvisor.naver.com`, which needs no ownership.

## Choose how to tell Naver about a URL

Naver's collection works by priority, so each route is a hint and none is a command.

| Method | Use it when | Why the others lose | Limit |
|---|---|---|---|
| Sitemap (요청 › 사이트맵 제출) | always, as the full list | RSS holds few URLs; a request holds one | under 10 MB, 50,000 URLs each, index files allowed |
| RSS (요청 › RSS 제출) | a news or blog site with fresh posts | carries full text, so it stays short | under 10 MB, at least one item, full body in each item |
| IndexNow | any site that changes pages and wants Bing too | the only route shared with other engines | 10,000 URLs per POST |
| 수집요청 (crawl request) | one important page | limited per site; takes 1 day to weeks | no fixed number published |
| Partner crawl API | a large site Naver has accepted | needs a partnership and a token | 1,000 URLs per call, 2 MB, daily limit |

Every URL in a sitemap or RSS feed must be absolute and on the verified host. Relative links, or links on another host,
are not collected. Submitting a page again each day does nothing: a queued request stays queued, and `수집보류` (crawl on
hold) in the tool does not stop Yeti collecting it another way.

## Set up Webmaster Tools and ownership

Webmaster Tools is optional for appearing in Naver, because Naver has no submission step, but it is the only source of
reports. Sites register by host: `www.example.com` and `blog.example.com` work, `www.example.com/myid` does not, and
scheme, `www` and port each make a separate site.

1. Sign in at `searchadvisor.naver.com`, add the site, and choose an ownership check: the `naver-site-verification` meta
   tag or an uploaded HTML file. There is no DNS method.
2. Put the tag in `<head>`. It is refused in `<body>` or inside a `frame`, and the checker runs no JavaScript.
3. If the home page redirects, use a server 301 or 302. JavaScript, `meta refresh` and cookie-based redirects fail the
   check.
4. Submit the sitemap and RSS feed, then read Site Status (사이트 상태).
5. Add the mobile site too, if it has separate URLs.

A new site's report takes at least a week and needs at least one collected page. Naver says a visited site reflects in
search within a week at most.

## Let Yeti collect the site

Yeti is Naver's search crawler, and most Naver problems begin with a firewall that blocks it.

```text
Mozilla/5.0 (compatible; Yeti/1.1; +https://naver.me/spd)
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Yeti/1.1; +https://naver.me/spd) Chrome/W.X.Y.Z Safari/537.36
```

Confirm a real Yeti with a reverse DNS lookup that ends in `.naver.com` and a forward lookup that returns the same IP,
or against the JSON and CIDR lists linked from the crawler guide. IP ranges change without notice, so never hard-code
them or block by IP. Two other robots appear in logs: `Ads-Naver` for advertisers' pages and `Blueno` for link previews.
Those special robots may not follow robots.txt, so protect private pages with a login, not a rule.

Naver reads robots.txt by status code.

| robots.txt answers | Yeti reads it as |
|---|---|
| 2xx, plain text | your rules; an HTML body may count as no file, which means allow all |
| 3xx | follows up to 5 HTTP redirects, then allow all; HTML and JavaScript redirects are ignored |
| 4xx | allow all |
| 5xx | disallow all, though earlier rules may be used for a while |

```text
User-agent: Yeti
Allow: /
Disallow: /admin/

Sitemap: https://www.example.co.kr/sitemap.xml
```

Rules apply to one host, scheme and port. Keep JavaScript and CSS collectable, because Yeti needs them to render. It may
also fetch them and favicons despite a rule, since it treats them as part of the page. To pause Yeti for a while, lower
the traffic limit in Webmaster Tools: a robots.txt block can drop collected documents from search.

## Fix what stops indexing

Indexing runs in four steps, 수집 (collect), 정제 (refine), 색인 (index) and 랭킹 (rank), and each report covers one.

| Report | Shows | Limits |
|---|---|---|
| 사이트 간단 체크 | live check of any site's home page | no account needed |
| 사이트 진단 | 색인, 수집제한 (restricted), 색인제외 (excluded), SEO | last 90 days of collected pages; URL lists up to 2,000 |
| 수집 현황 | DNS, connection, server, page and content errors | a page taking over a minute, or HTML around 4 MB, can fail |
| 콘텐츠 노출 및 클릭 | clicks, impressions, CTR, top 30 queries and pages | web results only, data about a week old, 90 days kept, deleted with the site |
| 사이트 최적화 | an AI-graded quality report | an indirect signal; a good grade does not mean a top rank |
| 사이트 상태 | certificate, HTTPS redirect, sitemap | refreshed every 1 to 2 days |
| URL 검사 | one URL's status, collection, index state, meta and SEO | also shows the HTML Yeti got, which finds hacks |

Naver wants pages to work without JavaScript where possible. It renders SPAs, but renders on a later visit and indexes
static HTML first, so server-render the main content. Use real paths, because Yeti strips `#fragments` and hash-bangs;
keep links in `<a href>`; and avoid timestamps or hashes in JavaScript URLs, which Naver says can break its reading of
the page. Errors need real status codes: 404 for missing, 403 for login-only, 503 for maintenance, 301 for a move. A 200
on an error page is a soft 404 and wastes indexing.

Yeti prefers HTTPS, and running HTTP and HTTPS without a redirect can cost a site as duplicates. Duplicate hosts and
URLs take a 301 to one canonical; use `rel="canonical"` with an absolute URL where a 301 is not possible, and an
HTTP redirect for the home page.

## Use IndexNow on Naver

IndexNow reaches Naver at its own endpoint, and shares changes with other engines. Key rules are stricter here than at
indexnow.org: Naver lists only hex characters and hyphens, 8 to 128 long, and asks for a separate key per domain.

```bash
KEY=$(python3 -c "import secrets; print(secrets.token_hex(16))")
printf '%s' "$KEY" > "public/$KEY.txt"     # must answer at https://www.example.co.kr/$KEY.txt

curl -i -H 'Content-Type: application/json; charset=utf-8' https://searchadvisor.naver.com/indexnow -d @- <<JSON
{"host":"www.example.co.kr","key":"$KEY","urlList":["https://www.example.co.kr/menu"]}
JSON
```

The answers are 200 success, 202 key check pending, 400 bad request, 403 invalid key, 422 URL does not match the key,
429 too many requests, and 500 server error. Naver sets no total limit, only a limit on bursts. Report only changes made
since you started: old URLs do not need backfilling. A 200 confirms receipt, not indexing, and IndexNow replaces neither
the sitemap nor RSS.

The partner crawl request API is for accepted sites and is covered in
[references/crawl-api.md](references/crawl-api.md), with removal and site moves.

## Worked example: a Seoul bakery chain Yeti cannot reach

Situation: a bakery chain has a Next.js site on `.com`, ranks in Google for its brand, and is invisible in Naver.

`naver_check.py` reports a clean 200 and a canonical written as a relative path. The simple site check says Yeti cannot
reach the site: the CDN's bot rule is challenging it, and logs show `Yeti/1.1` getting 403. The `<head>` carries no
ownership tag.

The team allows verified Yeti on the CDN, confirming with `host` on a logged IP. It verifies the host with a meta tag and
makes canonicals absolute, then submits the sitemap and an RSS feed of news posts.

Check: `naver_check.py` passes; URL 검사 shows the home page indexed; 사이트 진단 shows 색인 rising over four to six weeks
and 수집제한 falling; Korean referrals from Naver rise in analytics.

## Verify the work

Verification reads the site from outside, then from Naver's reports.

```bash
python3 scripts/naver_check.py https://www.example.co.kr/menu --key "$KEY"
host 125.209.235.169                                # an address from your logs; expect a name ending .naver.com
host crawl.125-209-235-169.web.naver.com            # expect the same address back
```

1. `naver_check.py` prints `PASS` on one URL per template, and each `NOTE` has an owner's reason.
2. The simple site check passes on the live home page.
3. URL 검사 shows the page collected and indexed, and its HTML matches the browser.
4. `site:www.example.co.kr` in Naver shows the pages.
5. 사이트 상태 shows the certificate, HTTPS redirect and sitemap as 정상 (normal).

## Gotchas in Search Advisor

The gotchas below are the ones that cost a site months with Naver.

1. **The site is missing and nothing looks wrong.** Symptom: `site:` finds nothing, and pages open fine. Cause: a
   firewall or CDN rule stops Yeti. Fix: read `수집 현황`, then allow Yeti by verified DNS, not by a fixed IP list.
2. **Ownership check fails on a working tag.** Symptom: the tool cannot find the tag. Cause: it sits in `<body>` or a
   frame, or the page reaches it by a JavaScript or meta refresh redirect. Fix: put it in `<head>` of a page reached by
   an HTTP redirect, and read it in `view-source:`.
3. **Sitemap accepted, URLs ignored.** Symptom: few pages get collected. Cause: relative links, or links on a host other
   than the verified one. Fix: use absolute URLs on the exact host.
4. **`http` and `https` count as two sites.** Symptom: API calls fail with error 1003, or reports look empty. Cause:
   scheme, `www` and port make separate sites. Fix: register the host that serves the canonical URLs.
5. **The whole site vanished after a move.** Symptom: a redesign drops exposure. Cause: robots.txt or a network block on
   the old site went up first, so Yeti never saw the redirects. Fix: redirect 1:1 with 301, wait until the main pages have
   moved, and only then block.
6. **`noindex` on a redirecting page does nothing.** Symptom: the URL stays in results. Cause: a page that only redirects
   may not have its tag read. Fix: set it on the target too, or remove the page.
7. **A key that works on Bing fails on Naver.** Symptom: 403 from `searchadvisor.naver.com/indexnow`. Cause: indexnow.org
   allows any letter, Naver's guide lists only hex. Fix: use a hex key everywhere.
8. **The crawl request says 보류.** Symptom: a requested URL shows crawl on hold. Cause: requests run by priority, and a
   spam-suspected site is limited. Fix: improve the page, keep it linked, and do not resubmit daily.

## Anti-patterns in Search Advisor

Anti-patterns here treat Naver's tools as commands, or copy Google's setup.

| Do not | Do this instead |
|---|---|
| Blocking Yeti by IP | use robots.txt, because IP ranges change |
| Resubmitting a page every day | fix the page; a queued request stays queued |
| Pausing Yeti with robots.txt | lower the traffic limit in Webmaster Tools |
| Expecting a DNS ownership check | use the meta tag or the HTML file |
| Blocking the old site before a move finishes | keep every hop collectable until the main pages have moved |

## Pre-merge checklist for Search Advisor

The checklist covers any change to routing, hosting or publishing for a site with Korean traffic.

1. `naver_check.py` passes on one URL per changed template.
2. Canonicals, favicons, `og:image` and sitemap URLs are absolute and on the verified host.
3. Main content and links are in server-rendered HTML; no `#` routes for separate pages.
4. Errors keep real status codes; moves use a server 301.
5. robots.txt allows Yeti, JavaScript, CSS and the favicon, and answers as text/plain.
6. The CDN and WAF let verified Yeti through.
7. Sitemap under 10 MB and 50,000 URLs; RSS holds full text; IndexNow key file live.
8. No API token in the repository, logs or tickets.

## References for Search Advisor

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/crawl-api.md](references/crawl-api.md): the partner crawl request API, removal and site moves.
- `scripts/naver_check.py`: one page as Yeti reads it: robots rules, tags, title lengths, sitemap, IndexNow key.

## See also for Search Advisor

- `naver-seo`: titles, structured data, C-Rank, Blog and AI Briefing
- `xml-sitemaps`: sitemap formats and limits
- `crawling-and-indexing`: robots.txt, status codes and server logs
- `bing-webmaster-tools`, `yandex-seo`: the other engines' consoles
- `site-migrations`: moves in general
