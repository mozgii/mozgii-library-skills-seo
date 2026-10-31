---
name: bing-seo
description: 'Optimises sites for Microsoft Bing: what differs from Google, the Webmaster Guidelines rewritten in 2026 for Copilot and grounding, how to tell Bing about a URL, IndexNow, bingbot verification, and where Bing''s market share justifies the work. A script checks a page without an account. Use for Bing SEO, bingbot, IndexNow, Bing not indexing a site, the Bing guidelines, writing content that can be grounded, or a site with traffic from the US, Japan or DuckDuckGo.'
metadata:
  tags:
  - seo
  - bing
  - indexnow
  - bingbot
  - webmaster-guidelines
  - grounding
---

# Bing SEO

Bing is the search index behind Microsoft Copilot and much of DuckDuckGo, so a page Bing cannot read is missing from all
three. The basics match Google's; what differs is how a site reports changes, what the guidelines ask, and how far the
market justifies the work. This skill covers those and proves each one. The console and its API belong to
`bing-webmaster-tools`, and Copilot's report and the AI preferences to `bing-ai-and-copilot`.

Facts here were read on Microsoft's own pages on 31 October 2026. Bing's help pages render only with JavaScript, so a
plain fetch of them returns a title and no text: open them in a browser.

## Step 0: read what the site already has

Step 0 fits the advice to the site before anything changes. Collect these first:

1. Traffic by engine from analytics, for 90 days: Bing, DuckDuckGo and `copilot.microsoft.com` referrals.
2. Whether Bing Webmaster Tools already has the site, and who can read its data.
3. Countries and languages served, set against the share table below.
4. What the page returns today:

```bash
python3 scripts/bing_check.py https://www.example.com/ --key YOUR_INDEXNOW_KEY
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

The check needs no account. Leave `--key` out when the site has no IndexNow key yet.

## Where Bing's market share justifies the work

Bing's share swings widely by country, from under 1% in Russia to about a third in Japan, so start from the site's own
markets. StatCounter's figures are third-party estimates from page views on sites that run its tracker, for all
devices. They are not Microsoft's numbers.

| Market (StatCounter, September 2026) | Bing | Google | What it means |
|---|---|---|---|
| Worldwide | 5.29% | 89.94% | worth the setup on any site |
| United States | 9.91% | 85.19% | a real second channel |
| Japan | 31.63% | 59.08% | treat Bing as a primary engine |
| China | 21.61% | 1.45% | second behind Baidu at 46.85% (`international-seo`) |
| South Korea | 4.84% | 47.97% | Naver comes first (`naver-seo`) |
| Czech Republic | 4.75% | 78.77% | Seznam holds 14.96% |
| Russian Federation | 0.75% | 28.1% | Yandex holds 70.35% (`yandex-seo`) |

DuckDuckGo says its traditional links and images come largely from Bing, so Bing work reaches its users too.

## Choose how to tell Bing about a URL

Bing offers five ways to report a change. IndexNow wins for almost every site: one request reaches every
participating engine, and Microsoft says URL and Content Submission may be deprecated.

| Method | Use it when | Why the others lose here | Limit |
|---|---|---|---|
| IndexNow | any site that publishes, edits or deletes pages | the rest reach Bing alone | 10,000 URLs per POST |
| XML sitemap | always, as the complete list | IndexNow reports changes, not the full set | read about once a day |
| Manual Submit URLs | a handful of urgent URLs | needs no code, but does not scale | 10,000 a day per domain |
| URL Submission API | a custom CMS that must not adopt IndexNow, or needs Bing alone | IndexNow is simpler and wider | 10,000 a day per domain, 500 per batch |
| Content Submission API | a real-time platform that wants to send page content and cut Bingbot load | much harder to build | 10 MB per submission, uncompressed |

Quotas reset at midnight UTC and apply to the domain, not each subdomain. A site's real quota can be lower than
10,000, so read it in Bing Webmaster Tools before a large batch (`bing-webmaster-tools`). Request indexing in URL
Inspection spends the same quota. No method guarantees indexing.

## What differs from Google

The work is the same as for Google in most places; these are the differences that change a decision.

| Topic | Google | Bing |
|---|---|---|
| Push a change | no general push; Indexing API for jobs and livestreams only | IndexNow, for any page |
| `crawl-delay` in robots.txt | ignored | honoured, and it overrides the hourly setting in Webmaster Tools |
| A permanent move | 301 or 308; a long-lived 302 is treated like a 301 over time | 301, and a redirect rather than a canonical tag; 302 only under two days |
| AI use of a page | Search Console setting, `Google-Extended` | AI Training and AI Grounding preferences (`bing-ai-and-copilot`) |
| Generated answers | a report with no queries | a report that names grounding queries |
| Console | Search Console | Bing Webmaster Tools, which can import a Search Console site (`bing-webmaster-tools`) |

## What the Webmaster Guidelines ask for grounding

The Webmaster Guidelines now describe how Bing treats a URL across search, Copilot and grounding APIs. The page shows no
date; trade press dated the rewrite to 26 and 27 February 2026 and reported no separate announcement. Its first
section is the point: normal SEO supports grounding, so nothing replaces crawlable, clear pages. Failing the guidelines can
cost visibility in search, eligibility for grounding, or the listing itself.

- **Discovery:** IndexNow, XML sitemaps, crawlable `<a href>` links with descriptive anchors, and external links from
  relevant sites. Avoid batches when you can send changes as they happen.
- **Freshness:** only canonical URLs in the sitemap; remove deleted or redirected ones promptly; accurate `lastmod` and
  HTTP validators such as ETag.
- **Moves:** 301 for a permanent move, 302 only under two days, and a redirect rather than a canonical tag. Keep URLs
  stable.
- **Removal:** return 404, tell IndexNow, use the removal tools when needed. `robots.txt` controls crawling, not
  indexing; `noindex` keeps a URL out of search, Copilot and grounding APIs.
- **Rendering:** do not hide critical content behind client-side rendering or block resources, and avoid piles of
  parameter URLs. Bing allocates crawl by site health and crawl value.
- **Content that can be grounded:** one topic per URL, the key fact near the top, statements that stand alone without
  implied context, consistent names for people, products and places, and text that images and video support but do not
  replace.
- **Structure:** a good `<title>`, a meta description, logical H1 to H6 and semantic HTML. Missing, duplicate or very
  short titles can reduce indexing and grounding eligibility.
- **Structured data:** it may help and it guarantees nothing; markup must match the visible page. Bing reads Schema.org
  in Microdata, JSON-LD and RDFa, plus microformats and Open Graph.
- **Measuring:** a fall in clicks is not always a loss of visibility, so watch impressions, indexing and citations too.

The guidelines name Generative Engine Optimization and say neither SEO nor GEO guarantees anything. The abuse list:
cloaking, link schemes, duplicate content, scraped or lightly rewritten content, keyword stuffing and engineered
language, unreviewed automatic content at scale, thin affiliate sites, malicious behaviour, misleading structured data,
and prompt injection, which covers any content written to manipulate the language models behind Bing or Copilot.
Actions range from lower rankings to removal; a site owner who believes one was a mistake contacts support through
Webmaster Tools.

## Verify and control Bingbot

Bingbot is the main crawler, and its user agent can be faked. Verify a claimed Bingbot with a reverse DNS lookup that
ends in `search.msn.com`, a forward lookup that returns the same IP, or the public Verify Bingbot tool. Automated
systems can match against `https://www.bing.com/toolbox/bingbot.json`.

```bash
host 157.55.39.1                                   # expect a name ending in search.msn.com
host NAME_FROM_THE_FIRST_LINE                      # expect 157.55.39.1 back
```

Other Microsoft crawlers appear in logs: AdIdxBot (ads), BingPreview and MicrosoftPreview (page snapshots), and
BingVideoPreview. Before calling a Bing crawl problem, check the WAF: a rule that challenges unknown bots stops Bingbot
long before robots.txt matters.

## Run IndexNow on Bing

IndexNow lets a site push changed URLs, and participating engines share them: Bing, Naver, Seznam.cz, Yandex, Amazon,
Yep and the Internet Archive, per indexnow.org in October 2026. Google does not take part. Use it for added, updated
and deleted URLs, and for pages that started returning a redirect, 404 or 410.

```bash
KEY=$(python3 -c "import secrets; print(secrets.token_hex(16))")     # hex keeps it valid on every engine
printf '%s' "$KEY" > "public/$KEY.txt"                               # must answer at https://www.example.com/$KEY.txt

curl -i -H 'Content-Type: application/json; charset=utf-8' https://api.indexnow.org/indexnow -d @- <<JSON
{"host":"www.example.com","key":"$KEY","urlList":["https://www.example.com/pricing","https://www.example.com/old-page"]}
JSON
```

| Answer | Means | Do |
|---|---|---|
| 200 | received; says nothing about indexing | watch the IndexNow report |
| 202 | received, key check pending | wait, confirm the key file answers |
| 400 | malformed request | check the JSON and URL escaping |
| 403 | key not valid | fix the file name or its content |
| 422 | URLs not on this host, or the key does not match | send one host per request |
| 429 | too many requests | slow down and spread submissions |

A key file in a subfolder validates only URLs under that folder. Each engine sets its own daily threshold and publishes
no number. Many platforms ship this already (Cloudflare, WordPress plugin, Shopify, Drupal and others), so check the
IndexNow report's Sources before writing code.

## Copilot and the old noarchive and nocache tags

Copilot draws on the Bing index, so everything above comes first. Today `noarchive` keeps a page out of Copilot and
`nocache` limits Copilot to URL, title and snippet. Microsoft is replacing both with AI Training and AI Grounding
preferences, with a deadline of 1 March 2027 for sites that use the old tags. Dates, syntax and the AI Performance report:
the `bing-ai-and-copilot` skill.

## Worked example: a Japanese retailer invisible in Copilot

Situation: a Tokyo appliance retailer gets 28% of its organic visits from Bing but no Copilot citations, and traffic
from Bing has fallen for two months.

`bing_check.py` on a product page shows a clean 200 and `noarchive` in the template, added in 2024 to stop cached copies.
That keeps the page out of Copilot today. Webmaster Tools' crawl report shows a rise in 403s, and the WAF log shows its
new bot rule challenging requests with the bingbot user agent; `host` on a sample IP confirms real Bingbot. Search
Performance shows clicks down on category pages, and Site Scan finds 12,000 parameter URLs from filters.

The team allows verified Bingbot in the WAF, removes `noarchive` from the template because the owner wants citations,
adds `Disallow` rules for filter parameters, and turns on the CDN's IndexNow integration. Product pages get price, stock
and warranty as text in the first screen.

Check: `bing_check.py` passes with no `noarchive` note; the crawl report's 403s fall to near zero within a week; the
IndexNow report shows submissions indexed; AI Performance shows grounding queries for product categories over the next
month. Nothing here promises citations, so the report to the owner states what changed and what the numbers then did.

## Verify the work

Verification proves each claim from the outside, and from Microsoft's own tools.

```bash
python3 scripts/bing_check.py https://www.example.com/pricing --key "$KEY"
host 157.55.39.1                                   # a logged IP: expect a name ending in search.msn.com
```

1. `bing_check.py` prints `PASS` on one URL per template; every `NOTE` is a decision somebody made.
2. URL Inspection (Live URL) shows the rendered HTML, and the Index card shows the URL indexed.
3. The IndexNow report shows a test URL arrive from the expected source, then its crawl status.
4. The crawl report's blocked, 4xx and 5xx counts stay flat or fall after a release.
5. For AI tags, read the served HTML and headers, because a preference counts only after Microsoft recrawls.

## Gotchas in Bing SEO

The gotchas below are what most often waste time on Bing.

1. **Site indexed in Google, missing from Bing.** Symptom: `url:` on the page finds nothing. Cause: usually a WAF
   block, no links pointing at a new site, or a blocked URL left in Webmaster Tools. Fix: read URL Inspection's Live URL
   first, then Block URLs, then the firewall.
2. **Copilot never cites the site.** Symptom: citations stay at zero and rankings look fine. Cause: `noarchive` or
   `nocache` on the template. Fix: remove them unless the owner chose them (`bing-ai-and-copilot`).
3. **IndexNow answers 200 and nothing happens.** Symptom: submitted URLs stay out of the index. Cause: 200 only confirms
   receipt. Fix: read the IndexNow report's Need Attention list (content quality, canonical, noindex, robots).
4. **A key that fails in a subfolder.** Symptom: IndexNow refuses URLs outside one folder. Cause: a key file in a
   subfolder validates only URLs under that folder. Fix: put the key file in the root.
5. **`data-snippet` from the guidelines.** Symptom: the attribute does nothing visible. Cause: the guidelines mention
   `data-snippet`, while the robots meta tag page documents only `data-nosnippet`, and we found no syntax for the former.
   Fix: rely on `data-nosnippet` and `max-snippet`, and test.
6. **An old 302 keeps the old URL.** Symptom: months after a move, Bing still treats the redirect as temporary. Cause:
   the guidelines ask for 302 only under two days. Fix: use 301 for a permanent move.

## Anti-patterns in Bing SEO

Anti-patterns on Bing copy Google habits or buy shortcuts that its guidelines name.

| Do not | Do this instead |
|---|---|
| Treating Bing as Google with less traffic | check the market table, and work Japan or a Microsoft-heavy B2B audience as a primary channel |
| Using `nosnippet` to manage AI use | use the AI preferences, because `nosnippet` also strips captions |
| Sending every URL through IndexNow nightly | send real changes, as they happen |
| Keeping a redirect as a 302 for months | use 301; Bing asks for 302 only under two days |
| Writing pages for grounding with engineered phrasing | write for readers; prompt injection and keyword stuffing are named abuses |

## Pre-merge checklist for Bing SEO

The checklist covers a change that touches templates, robots rules or publishing.

1. `bing_check.py` passes on one URL per changed template.
2. No new `noindex`, `noarchive`, `nocache`, `nosnippet` or `data-nosnippet` without an owner's decision.
3. robots.txt still allows bingbot, keeps the `Sitemap:` line, and has no stray `crawl-delay`.
4. The WAF and CDN let verified Bingbot through.
5. Publish, update and delete events reach IndexNow, with the key file live.
6. The sitemap lists only canonical URLs that answer 200.
7. Redirects are 301 unless the move lasts under two days.
8. AI preferences match the written policy, on pages and in robots.txt (`bing-ai-and-copilot`).

## References for Bing SEO

The script below holds the detail for this skill.

- `scripts/bing_check.py`: one page read as Bingbot reads it, with robots rules, directives and the IndexNow key file.

## See also for Bing SEO

- `bing-webmaster-tools`: setup, every report, the REST API and quotas
- `bing-ai-and-copilot`: AI Performance and the AI Training and AI Grounding preferences
- `ai-search-visibility`: AI crawlers and citations across every assistant
- `xml-sitemaps`: sitemap formats and limits
- `crawling-and-indexing`: robots.txt rules and server logs
- `naver-seo`, `yandex-seo`: other engines that take IndexNow
- `international-seo`: choosing engines by market
