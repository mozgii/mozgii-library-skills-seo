---
name: naver-seo
description: 'Ranks sites in Naver search in South Korea: where content should live, titles, descriptions, favicons and sublinks, Naver structured data, content and spam guidelines, C-Rank and blogs, AI Briefing, and what share figures to trust. Use for Naver SEO, 네이버 SEO, 네이버 블로그, C-Rank, AI 브리핑, 서브링크, Naver titles, or any site that needs to rank with Korean searchers.'
metadata:
  tags:
  - seo
  - naver
  - korea
  - c-rank
  - naver-blog
  - ai-briefing
  - structured-data
---

# Naver SEO

Naver is South Korea's home search engine, and it shows a website as one source among its own Blog, Cafe, Knowledge iN
and shopping results. A site that ranks in Google can still be absent here, because Naver has its own
crawler, its own console and strict rules on titles. This skill covers what ranks once a site is collected, and where a
Naver Blog earns more than the website does. Registering a site and getting it collected belongs to
`naver-search-advisor`.

Naver's official guides are in Korean, at `searchadvisor.naver.com/guide`. All 54 were read for this skill on 31 October
2026 and written here in English, keeping the Korean terms you will meet in the tools.

## Step 0: read what the site already has

Step 0 fits the advice to the site before anything changes.

1. Korean traffic by source in analytics, for 90 days: `naver.com`, `m.search.naver.com`, `blog.naver.com`.
2. Which Naver surfaces already exist: a Blog, a SmartStore, a Place listing.
3. What the page's title and description are today, read the way Yeti fetches them:

```bash
curl -sL -A 'Mozilla/5.0 (compatible; Yeti/1.1; +https://naver.me/spd)' https://www.example.co.kr/ | python3 -c '
import re, sys
html = sys.stdin.read()
title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
desc = re.search(r"<meta[^>]+name=[\x22\x27]description[\x22\x27][^>]+content=[\x22\x27]([^\x22\x27]*)", html, re.I)
for name, found in (("title", title), ("description", desc)):
    text = found.group(1).strip() if found else ""
    print(name, len(text), text)'
```

Then run the same URL through the public simple site check (사이트 간단 체크) at `searchadvisor.naver.com`, which needs no
ownership. If it says Yeti cannot reach the site, stop here and start with `naver-search-advisor`.

## How much of Korea Naver holds

Naver's share depends heavily on who measures it, so quote the source and date every time. Neither figure comes from
Naver.

| Source | Period | Naver | Google | Measures |
|---|---|---|---|---|
| StatCounter | September 2026 | 43.05% | 47.97% | page views on sites running its tracker, worldwide sample; Bing 4.84%, Daum 0.73% |
| InternetTrend (BizSpring) | 30 September to 29 October 2026 | 68.6% | 25.7% | visits logged on Korean sites that install its logger; Bing 2.8%, Daum 2.3% |

Both are third-party estimates. The gap comes from the samples, so use your own referral data. A Korean consumer brand
usually needs both engines; a developer tool may find Google is enough.

## Choose where the content lives

Naver searches its own services beside the open web, so the first decision is where a piece of content should live.

| Surface | Wins when | Why the others lose | Search Advisor reports it? |
|---|---|---|---|
| Own website | products, services, documentation, anything you must own | a Blog cannot hold the checkout or the brand's URLs | yes |
| Naver Blog (네이버 블로그) | reviews, experience, how-to posts for Korean readers | a site starts with no history; C-Rank rewards a blog's topical record | no: Blog and VIEW results are outside the report |
| Naver Cafe, Knowledge iN (지식iN) | community questions | a brand's post reads as an ad, so answer as a named expert | no |
| SmartStore, Place | selling or a physical location | a website alone has no store or map card | through their own consoles |

Name the Blog, SmartStore and social accounts in the site's channel markup, so Naver can connect them
([references/structured-data.md](references/structured-data.md)).

## Write titles and descriptions for Naver

Naver's guides are unusually specific about titles and descriptions. The site check recommends a title of 40 characters
or fewer and a description of 80 or fewer.

| Field | Do | Costs exposure |
|---|---|---|
| Home `<title>` | the brand: a company, service or product name | changing it often to chase search; excessive length |
| Page `<title>` | a unique phrase naming the page's topic | a word repeated twice or more, promo text, unrelated keywords, one title across the site |
| `meta description` | one or two sentences | a pasted body, a copy of the title, one description across the site, a keyword list |
| `og:title`, `og:description` | set them too; Naver may choose them at indexing | |
| `og:image` | a unique image over 150x150, at least 5,000 bytes, ratio up to 3:1 | a logo or banner repeated across pages, which Naver may skip |

The engine picks the title and snippet it shows from these tags, the page and anchors, and Naver will not edit them by
hand. A distinctive brand name helps: one that is an ordinary noun is harder for Naver to read as a navigation query.

Favicons show in results when collectable, square, at least 16px (32px or larger is advised) and in ICO, PNG, GIF, APNG,
JPEG or SVG. Keep one tag per `rel`; if several exist, Naver takes `shortcut icon`, `icon`, the default `/favicon.ico`,
`apple-touch-icon`, then `apple-touch-icon-precomposed`.

Sublinks (서브링크) are automatic and cannot be requested. Exclude one with `rel="nosublink"` on its `<a>`, or all with
`<meta name="naver" content="nosublinks">`. Changes take about 7 days after a recrawl, and the takedown form can remove a
link permanently, so try the markup first. The brand line under a result (사이트 브랜드) is automatic too.

## Add structured data for Naver

Naver reads Schema.org in JSON-LD or Microdata, its two recommended formats, and supports fewer types than Google. Valid
markup guarantees nothing, and a page's content can override it.

| Type | Use for |
|---|---|
| `Person`, `Organization` with `sameAs` | linked channels, on the root page |
| `PostalAddress`, `BreadcrumbList` | address and path in results |
| `ItemList` of `ListItem` | carousels |
| `AggregateRating`, `Review` | scores; one reviewed thing per page |
| `Recipe`, `Restaurant`, `SoftwareApplication`, `Movie`, `TVSeries`, `VideoObject` | their own result types |

Required properties, limits and templates: [references/structured-data.md](references/structured-data.md).

## Write content that Naver trusts

Naver's content guide asks for five things: expertise and first-hand experience, one consistent subject (most of the
site, and at least half of its content, on the core topic), honesty and original work with sources linked, readable
structure with key facts as text, and steady upkeep. It says Yeti checks whether a site is kept up, and that an abandoned
site which fills with spam can lose exposure.

AI tools are allowed, as long as the operator adds experience and a point of view: a generated or summarised text
published as is falls short. Scale matters more than the tool. Mass pages from one template are spam whether or not
AI wrote them.

The spam list: cloaking, deceptive redirects (timed or on Back), link spam, backlink abuse, expired-domain abuse, macro
manipulation of visits or comments, hacked content, malware, hidden text, keyword stuffing, clickbait, mass low-quality
content, scraping, harmful content, confusing or falsified details, fake public sites, phishing, and attacks on service
stability. Exposure can be limited or removed, and an owner who has fixed the cause can ask to have it restored.

## Work Naver Blog and C-Rank

C-Rank is the name Naver gave in 2016 to the part of its blog ranking that scores a source. Its post describes four
words: Context (how focused the blog is on a topic), Content (quality), Chain (how readers react and pass it on), and
Creator (the trust and popularity those add up to). The value feeds blog ranking in part, and it is not the whole
ranking. In the same post Naver rejects the folk terms "최적화 블로그" (optimised blog) and "저품질 블로그" (low-quality
blog) as a way of thinking, and warns there is no quick trick.

D.I.A. is reported by Korean SEO writers as Naver's document-level model. We could not reach a Naver post that defines it
in this round, so treat any detail about it as a third-party claim.

In practice: keep a blog on one subject, publish first-hand posts with original photos, answer the question a searcher
typed, and never buy visits, comments or accounts. Those are macro manipulation under the spam policy.

## Work with AI Briefing

AI Briefing (AI 브리핑) is Naver's generated answer in search, and Naver's own search blog mentions it across results in
2026. A launch date of 27 March 2025 comes from press reports. No official guide says how a page qualifies, and the guides
describe no AI report, so the same work applies: indexable pages, sources and clear facts.

`<meta name="robots" content="nosourceinfo">` is the one AI control in the guides. It stops Naver giving an AI-written
description of the site as a source. The guide does not say it removes a page from AI Briefing, so never promise that.

## Worked example: a Seoul bakery chain whose titles Naver dislikes

Situation: a bakery chain's site is collected by Naver and ranks in Google for its brand, yet it shows weakly on Naver.

The home title runs to 62 characters and repeats "베이커리" three times, and the home page sets its title in the client. The
team renders titles on the server, shortens the home title to the brand, and brings the main page titles to under 40
characters, each naming a product or branch. The root page gains `Organization` markup with `sameAs` to the Naver Blog and
Instagram. A Naver Blog starts a weekly series of real baking notes, while store pages keep prices, hours and addresses
as text.

Check: the Step 0 command shows the new title and its length on each template; `site:` shows unique titles; Korean
referrals from Naver rise in analytics. Blog results stay outside Search Advisor's click report, so measure them from
`blog.naver.com` stats.

## Verify the work

Verification reads the served page, then Naver's own results. This command prints each template's title and flags what
Naver's guides warn about:

```bash
for u in https://www.example.co.kr/ https://www.example.co.kr/menu https://www.example.co.kr/stores/gangnam; do
  curl -sL -A 'Mozilla/5.0 (compatible; Yeti/1.1; +https://naver.me/spd)' "$u" | python3 -c '
import collections, re, sys
html = sys.stdin.read()
found = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
title = found.group(1).strip() if found else ""
repeats = [w for w, n in collections.Counter(re.findall(r"[\w가-힣]{2,}", title)).items() if n > 1]
print(len(title), "OVER 40" if len(title) > 40 else "ok", "REPEATS " + ",".join(repeats) if repeats else "", title)'
done
```

1. Every title is unique, within 40 characters, with no repeated word.
2. `site:www.example.co.kr` in Naver shows the pages with distinct titles.
3. `<meta name="robots" content="nosourceinfo">` appears only where the owner chose it.
4. Structured data matches the visible page.
5. Korean referrals from `naver.com` and `blog.naver.com` move in analytics.

## Gotchas in Naver SEO

The gotchas below are the ones that cost a site months with Naver.

1. **The site is missing and nothing looks wrong.** Symptom: `site:` finds nothing, and pages open fine. Cause: usually a
   firewall or CDN rule that stops Yeti. Fix: start with `naver-search-advisor`, because no title work counts until then.
2. **A title that repeats its keyword.** Symptom: a long title catches no more queries. Cause: Naver names a word repeated
   twice or more as a cost to exposure. Fix: write a short phrase naming the page's topic.
3. **A logo as every `og:image`.** Symptom: results show no image. Cause: Naver may skip a logo or banner repeated across
   pages. Fix: use a unique image over 150x150, at least 5,000 bytes, ratio up to 3:1.
4. **A brand that is an ordinary noun.** Symptom: searches for the brand show unrelated results. Cause: such a name is
   harder for Naver to read as a navigation query. Fix: use the distinctive form of the name in the home title.
5. **Blog posts missing from the click report.** Symptom: Search Advisor shows little, though Naver brings visits. Cause:
   the report counts web results only and leaves out VIEW, blog, content panels and ads. Fix: read each surface in its own
   stats, and analytics for the total.
6. **The AI opt-out that is not one.** Symptom: `nosourceinfo` is set and answers still draw on the site. Cause: it covers
   the source description. Fix: use `noindex` to leave search, and tell the owner what that costs.

## Anti-patterns in Naver SEO

Anti-patterns on Naver usually come from treating it as a Korean Google.

| Do not | Do this instead |
|---|---|
| Stuffing keywords into a title to catch more queries | write a short, unique title; repetition is named as a penalty |
| Changing the home title each season | keep the brand there; only page titles change |
| Machine-translating an English site | research Korean queries and write for them |
| Buying blog posts, visits or comments | earn them; macro manipulation is a listed spam type |
| Running several sites with the same content to take more results | keep one; duplicate sites lose exposure |
| Using a free hosting subdomain | use your own domain; Naver's URL guide recommends it |
| Quoting one market share number | name the source and date, and read your own referrals |

## Pre-merge checklist for Naver SEO

The checklist covers any change to templates or content for a site with Korean traffic.

1. The site is collected by Yeti (`naver-search-advisor`).
2. Titles stay unique and within 40 characters, with no repeated words; descriptions stay within 80.
3. The home title stays the brand; only page titles change.
4. `og:title`, `og:description` and a unique `og:image` are set.
5. Favicon collectable, square, with one tag per `rel`.
6. Main content is in server-rendered HTML.
7. Structured data matches the visible page, with one reviewed thing per page.
8. Blog, SmartStore and social accounts are named in the site's channel markup.

## References for Naver SEO

The reference file below holds the detail for this skill; open it only when the task needs it.

- [references/structured-data.md](references/structured-data.md): the types Naver supports, required properties, and
  JSON-LD templates.

## See also for Naver SEO

- `naver-search-advisor`: Webmaster Tools, Yeti, indexing fixes, IndexNow and the crawl API
- `international-seo`: URL structure and hreflang for Korea
- `structured-data`: Schema.org and Google's rich results
- `bing-seo`, `yandex-seo`: the other engines' rules
- `content-briefs`: planning content around real questions
- `ai-search-visibility`: AI answers across engines
