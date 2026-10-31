---
name: yandex-seo
description: 'Optimises sites for Yandex search in Russian-speaking markets: Yandex Webmaster setup and reports, regional assignment, robots.txt differences (Clean-param, no Crawl-delay or Host), recrawl and IndexNow, the site quality index (ИКС), commercial and behavioural factors, filters for over-optimisation and bought links, Yandex Business listings, Metrica and Alice AI answer visibility. Use for Яндекс, Вебмастер, региональность, ИКС, Баден-Баден, Минусинск, Clean-param, or any site that needs traffic from Yandex.'
metadata:
  tags:
  - seo
  - yandex
  - yandex-webmaster
  - russian
  - regional-seo
---

# Yandex SEO

Yandex is the main search engine in Russia and is used across Russian-speaking markets. It follows the same basics as
Google (crawlable, useful, well-structured pages), with its own webmaster tools, stronger regional ranking, explicit
commercial factors, behavioural signals, and named filters for over-optimisation and link buying. Russian-language
text itself is covered by the `russian-language-seo` skill.

## Step 0: read what Yandex already sees

Read the site's Yandex state first, because region, mirror and robots.txt rules decide what the rest of this skill
changes. Collect whether Webmaster and Metrica are already connected and who can read them, the regions the business
sells in, and whether a Yandex Business card exists. Then read what the site serves today:

```bash
for u in http://example.ru/ http://www.example.ru/ https://example.ru/ https://www.example.ru/; do
  curl -sIL -o /dev/null -w "$u -> %{url_effective} %{http_code} (%{num_redirects} hops)\n" "$u"
done
curl -s https://www.example.ru/robots.txt | grep -iE '^(user-agent|clean-param|host|crawl-delay|sitemap):'
```

Every variant should end on the one main mirror. `Host` and `Crawl-delay` lines mean the site relies on rules Yandex no
longer reads.

## Yandex Webmaster setup

Yandex Webmaster (webmaster.yandex.ru) is the Yandex counterpart of Search Console; every site that wants Yandex
traffic needs it.

1. Add the site and verify (meta tag, HTML file or DNS record). Add every host variant; set the main mirror with
   301 redirects, since the `Host` directive was retired in 2018.
2. Submit sitemaps (Indexing › Sitemap files) and check robots.txt (Tools › robots.txt analysis).
3. Set the region (Site information › Regionality), or link the site to a Yandex Business listing.
4. Link Yandex Metrica to see behaviour data alongside search data.
5. Read Diagnostics (critical and possible problems), Indexing (pages in search, excluded pages with reasons),
   Search queries (shows, clicks, positions), and Security and violations.

## Indexing in Yandex

Yandex indexing follows robots.txt and meta robots like Google, with a few differences.

| Topic | Yandex behaviour |
|---|---|
| `Clean-param` | supported: `Clean-param: utm_source&utm_medium&utm_campaign /` tells Yandex to ignore those parameters |
| `Crawl-delay` | ignored since 2018; set crawl speed in Webmaster (Indexing › Crawl rate) |
| `Host` | retired; use 301 redirects to the main mirror |
| robots.txt size | over 500 KB is treated as allowing everything |
| `<noindex>` tag | Yandex-specific HTML tag that keeps part of the text out of its index (`<!--noindex-->...<!--/noindex-->` for valid HTML) |
| Recrawl | Indexing › Page recrawl: a daily quota of URLs to recrawl quickly |
| IndexNow | supported; one submission also reaches Bing and others (`xml-sitemaps`) |
| Turbo pages | discontinued in 2025; serve fast mobile pages instead |
| Important pages | Indexing › Monitoring important pages alerts on status or content changes |

## Parameter URLs in Yandex: Clean-param, canonical or Disallow

Parameter URLs in Yandex are handled by what the parameter does to the page, so pick from that.

| The URL | Use | Why the others lose here |
|---|---|---|
| Listed tracking parameters: `utm_*`, `ysclid`, `yrclid` | `Clean-param` is optional | Yandex may remove these itself when it finds them insignificant; `Disallow` is never needed for them |
| `?ref=`, `?sid=` and others that never change the content | `Clean-param: ref&sid /catalog/` | Yandex recommends it because it moves some accumulated metrics to the main URL; `Disallow` moves none, and `rel="canonical"` is a recommendation the robot can ignore |
| `?sort=price`, `?view=grid`: the same items in another order or layout | `rel="canonical"` to the clean URL | `Clean-param` is for parameters that leave the content unchanged; `Disallow` hides the tag from the robot |
| Internal search, cart and filter URLs with no place in search | `Disallow` | the content differs, so `Clean-param` does not fit and Yandex ignores a canonical to a much different page |

Do not put `Disallow` on URLs that only need `Clean-param`: `Disallow` takes priority, so the page stays out of the index.
A `Clean-param` rule is case sensitive, holds up to 500 characters, takes an optional path prefix and can sit anywhere in
robots.txt. It is a Yandex rule, so a site that also needs Google keeps `rel="canonical"` on those URLs.

## Regional ranking

Yandex ranks many queries by region: a "geo-dependent" query (plumbing, delivery, dentist) shows different results in
Moscow and Novosibirsk. A site gets a region from Webmaster's Regionality setting, its Yandex Business listing,
addresses and phone codes on the pages, and content. Region codes appear in search URLs as `lr` (213 Moscow, 2 Saint
Petersburg, 225 Russia). A business serving several cities needs a page per city with that city's address, phone
and specifics, and a Yandex Business listing per branch; the same text with a swapped city name is a doorway.

## Commercial factors

Commercial factors are signals Yandex uses for commercial queries: how much the site looks like a real, trustworthy
business that can fulfil the order. Show on service and product pages, as text:

- prices or price ranges, delivery and payment terms, guarantees and returns;
- contacts: a phone with city code, an email on the domain, an address, opening hours, messengers;
- legal details (company name, ИНН/ОГРН) in the footer or on a details page;
- a wide assortment or full service list, filters and search on large catalogues;
- reviews, cases, certificates, photos of real work and staff;
- clear navigation, a working cart or order form, an "about" page.

## Behavioural factors

Behavioural factors are how users act on results and on the site: clicks from the results page, returns to search,
time to the next action. Yandex weighs them more openly than Google. Improve them honestly: a title and snippet that
match the page, an answer on the first screen, fast mobile pages, clear next steps. Buying fake visits or clicks
("накрутка ПФ") is detected and leads to sanctions for the host.

## Yandex filters and sanctions

Yandex names its main filters, and each has a known cause and recovery path.

| Filter | Cause | Recovery |
|---|---|---|
| Баден-Баден (Baden-Baden) | over-optimised text written for the robot: repeated phrases, keyword lists, long SEO texts nobody reads | rewrite the affected pages for readers (`russian-language-seo`), then report in Webmaster's Security and violations |
| Минусинск (Minusinsk) | bought links that pass ranking weight | remove the paid links; wait for recrawl of the linking pages |
| АГС (AGS) | low-value sites made for selling links or with copied, auto-generated content | add real value, stop selling links |
| Behavioural manipulation | fake clicks and visits | stop the manipulation; sanctions lift after a period |
| Doorways, cloaking, hidden text | as in Google's spam policies | remove them |

Violations show in Webmaster › Diagnostics › Security and violations; after fixing, request a recheck there.

## Site quality index (ИКС)

ИКС (site quality index) is a Yandex score of a site's popularity and usefulness to users, shown in Webmaster and
for some sites in Yandex Business. It is a consequence of audience, traffic and trust, not a ranking factor and not a
target. Do not buy services promising to raise it.

## Yandex Business and local search

Yandex Business (business.yandex.ru, formerly Yandex Directory) holds the organisation cards shown in Yandex Search
and Maps. One card per branch with the real address, phone, hours, category, photos, prices and reviews; link it to
the site in Webmaster for regional assignment. Answer reviews; never post fake ones. 2GIS is a second major map
platform in the same markets (`local-seo`).

## Alice AI answers

Alice AI (formerly Neuro, «Нейро») generates answers in Yandex Search with links to sources. Since April 2026 Yandex
Webmaster shows a site's visibility in Alice AI answers: the queries where it is cited, and the competitors cited
instead. It uses the normal Yandex index, so the same rules apply: indexable pages, clear answers under matching
headings, specific facts (`ai-search-visibility`).

## Keyword demand for Yandex

Wordstat is the Yandex source of query frequency, and main phrases for Yandex are chosen on its exact frequency, not its
broad figure. Operators, sources, the APIs and a no-login script: the `yandex-wordstat` skill.

## Worked example: a Moscow renovation firm invisible in Yandex

Situation: a renovation company ranks in Google for «ремонт квартир под ключ» but not in Yandex.

Checks: Webmaster has no region set and no Yandex Business card; the service pages show no prices, only «по
запросу»; a 2,500-word text under the price block repeats the phrase 19 times in its forms. Fix: region Moscow in
Webmaster and a verified Yandex Business card linked to the site; price ranges per square metre, a sample estimate,
contract terms and company details as text; the long text cut to a 400-word answer to real questions (time, cost,
guarantee). Check: Search queries in Webmaster for the Moscow region over four to six weeks; Security and violations
stays empty.

## Verify Yandex fixes with commands

These commands prove what a fix changed on the server, before Yandex recrawls. The server's answer to the crawler's
user agent comes first, then the mirror, the robots.txt rules, and the commercial facts in the HTML.

```bash
YB='Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
PAGE=https://www.example.ru/uslugi/remont-kvartir/
curl -s -o /dev/null -w '%{http_code}\n' -A "$YB" "$PAGE"                            # expect 200
curl -sIL -o /dev/null -w '%{num_redirects} hops to %{url_effective}\n' http://example.ru/   # expect 1 hop to the main mirror
curl -s https://www.example.ru/robots.txt | grep -ciE '^(host|crawl-delay):'         # expect 0
curl -s -A "$YB" "$PAGE" | grep -ioE '<meta[^>]+name="(robots|yandex)"[^>]*>'        # expect no noindex
curl -s -A "$YB" "$PAGE" | grep -cE '[0-9] ?(₽|руб)'                                 # expect 1 or more: prices as text
```

A 200 here proves the server's answer, not a firewall rule that checks the crawler's IP, so confirm with a real visit:
log lines from `YandexBot`, verified by reverse and forward DNS, or the result of Indexing › Page recrawl. Then read
Webmaster: Diagnostics shows no critical problem, Security and violations stays empty, and Search queries for the
target region moves over four to six weeks.

## Checklist for Yandex SEO

The Yandex checklist covers setup, regions, trust and text.

1. Webmaster verified; main mirror set by 301; sitemaps submitted; no critical diagnostics.
2. Region assigned; a Yandex Business card per branch linked to the site.
3. Commercial pages show prices, terms, contacts and legal details as text.
4. robots.txt uses `Clean-param` for tracking parameters; no reliance on `Crawl-delay` or `Host`.
5. Main phrases chosen on exact Wordstat frequency for the target regions.
6. No over-optimised texts, bought links or behavioural manipulation; Security and violations empty.
7. Metrica linked; IndexNow sends changed URLs.

## Gotchas in Yandex SEO

The gotchas below are specific to Yandex.

1. **Long SEO texts under the catalogue.** Symptom: pages drop and Webmaster may list a violation. Cause: text stuffed
   with phrases is a classic Baden-Baden trigger. Fix: cut it to an answer to real questions.
2. **No region set.** Symptom: a local business ranks nowhere in particular. Cause: the site competes everywhere and
   wins nowhere. Fix: set the region and link a Yandex Business card.
3. **Scraping the Yandex results page.** Symptom: captchas and blocked IPs. Cause: automated requests to the results
   page are refused. Fix: use Webmaster for your own positions and paid SERP data for competitors.
4. **Latin spelling of a term in titles.** Symptom: a page misses demand that a rival takes. Cause: the Cyrillic form
   has the demand («AI агент» against «ИИ-агент»). Fix: compare exact frequency of both forms (`yandex-wordstat`).

## Anti-patterns in Yandex SEO

Anti-patterns for Yandex apply Google habits, or old Yandex tricks, to a search engine with its own rules.

| Do not | Do this instead |
|---|---|
| Buying clicks or visits | improve title, snippet and first screen; manipulation brings host sanctions |
| Using `Host` or `Crawl-delay` | use 301 redirects and the crawl rate setting in Webmaster |
| Treating ИКС as a goal | treat it as a consequence, and skip services that promise to raise it |
| Hiding prices behind «по запросу» | show ranges as text, because commercial factors read them |
| Swapping the city name across pages | give each city its own address, phone and specifics |

## See also for Yandex SEO

- `yandex-wordstat`: Wordstat operators, sources and the demand script
- `russian-language-seo`: writing and editing Russian text
- `keyword-research`: the general keyword workflow
- `local-seo`: 2GIS and other local platforms
- `xml-sitemaps`: IndexNow and sitemaps
- `ai-search-visibility`: Alice AI answers among other assistants
- `bing-seo`, `naver-search-advisor`: the other engines that take IndexNow
