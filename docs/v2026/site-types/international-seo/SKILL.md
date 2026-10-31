---
name: international-seo
description: 'Sets up and audits multilingual and multi-country sites for search: choosing ccTLDs, subdomains or subfolders, hreflang in HTML, HTTP headers or sitemaps with return links and x-default, valid language and region codes, canonicals per locale, translation versus localisation, no automatic IP redirects, and per-engine differences (Google, Bing, Yandex, Naver, Baidu, Seznam), with a China reference on Baidu, licensing and hosting. Use when launching a site in another language or country, when hreflang errors appear, when the wrong country version ranks, or when planning URL structure for international markets.'
metadata:
  tags:
  - seo
  - international-seo
  - hreflang
  - multilingual
  - localisation
  - geotargeting
---

# International and multilingual SEO

International SEO makes each language or country version of a site findable by the people it was made for, and
stops versions from competing with each other. The two tools are a clear URL structure per locale and hreflang
annotations that tell search engines which version is for whom.

## Step 0: read how the site handles locales today

Read the current setup first, because a change of URL structure is a migration, and redirects by language can hide
versions from crawlers.

```bash
curl -sL https://www.example.com/ | grep -ioE '<html[^>]*lang="[^"]*"|<link[^>]*hreflang[^>]*>'
curl -s https://www.example.com/sitemap.xml | grep -o '<xhtml:link' | wc -l
curl -sI -H 'Accept-Language: de' https://www.example.com/ | grep -iE '^(HTTP/|location:)'
```

The first two show where hreflang lives; the third shows whether the home page redirects by browser language. Then
list the locales that exist, how each is served (ccTLD, subdomain or folder), and clicks by country from Search Console.

## Language versus country targeting

A site targets languages, countries, or both, and the choice decides the URL structure and the hreflang codes.

| Case | Target | hreflang example |
|---|---|---|
| Same content for every German speaker | language | `de` |
| Different prices, stock or law per country, same language | language + region | `en-US`, `en-GB`, `en-AU` |
| One country, several languages | language + region | `fr-CH`, `de-CH`, `it-CH` |

Create a separate version only when it differs for the user: language, currency, prices, delivery, legal text, or
contact details. Near-identical pages for `en-US` and `en-CA` are fine with hreflang, but each version needs to work
for its market.

## URL structure for international sites

The URL structure options trade signal strength against cost.

| Structure | Example | Pros | Cons |
|---|---|---|---|
| Country domain (ccTLD) | `example.de` | strongest country signal; local trust | one site per country to build, link and maintain |
| Subfolder on a generic domain | `example.com/de/` | one domain's authority; cheapest | weaker country signal than a ccTLD |
| Subdomain | `de.example.com` | separate hosting possible | treated much like a separate site |
| URL parameter | `example.com/?lang=de` | — | not recommended: hard to target and to crawl |

Subfolders are the default for most sites. Google removed the country targeting setting from Search Console in
2022; a generic domain's country now comes from hreflang, local content and links.

## hreflang rules

hreflang tells search engines which URL serves which language and region, so the right one shows. Google ignores the
annotations of a pair that does not link both ways.

1. Every version lists every version, **including itself**.
2. Every link is **reciprocal**: if A names B, B names A. Missing return links are the most common error.
3. Codes: ISO 639-1 language (`en`, `de`, `ja`, `zh`), optionally a script (`zh-Hant`), optionally an ISO 3166-1
   alpha-2 region (`en-GB`). A region alone is invalid; `uk` is Ukrainian, not the United Kingdom (`en-GB`); `jp` and
   `cn` are not language codes. `kr` means Kanuri and `se` means Northern Sami: both are valid, but on most sites they
   are Korea (`ko`) or Sweden (`sv`) typed by mistake, so check what the page is for. Google does not support numeric
   regions such as `es-419`.
4. `x-default` names the fallback for users matching no version: a language selector or the main version.
5. URLs are absolute, answer 200, are indexable and **canonical**: each version's canonical is itself, never another
   language's URL.
6. Use one method per site: HTML `<link>` tags, HTTP `Link` headers (for PDFs) or the sitemap (`xml-sitemaps`).

```html
<link rel="alternate" hreflang="en-US" href="https://www.example.com/us/running-shoes/">
<link rel="alternate" hreflang="en-GB" href="https://www.example.com/uk/running-shoes/">
<link rel="alternate" hreflang="de" href="https://www.example.com/de/laufschuhe/">
<link rel="alternate" hreflang="x-default" href="https://www.example.com/running-shoes/">
```

HTTP header form:

```text
Link: <https://www.example.com/us/guide.pdf>; rel="alternate"; hreflang="en-US", <https://www.example.com/de/guide.pdf>; rel="alternate"; hreflang="de"
```

## Verify

The hreflang check script starts from one or more URLs, follows every alternate it finds, and reports missing self
references, missing return links, bad codes, non-200 alternates and canonical conflicts. A missing `x-default` is
optional, and `kr` or `se` may be intended, so these print as a `NOTE` and do not fail the run:

```bash
python3 scripts/hreflang_check.py https://www.example.com/us/running-shoes/
```

When the file is not on disk (a pack install), read this script from the library that served this page and save it first.

Then read the Search Console URL Inspection result for a few versions: "Google-selected canonical" must be the
version itself, not another language.

## Language detection and the lang attribute

Search engines detect a page's language from its visible content, so translate the whole main content, navigation
and metadata. Google says it uses neither hreflang nor the HTML `lang` attribute to detect language; set
`<html lang="de">` anyway for accessibility, Bing (which documents `lang` and the `content-language` meta tag as
signals) and browsers.

## Localisation, not only translation

Localisation adapts the page to the market, and it is what makes a version rank and convert there.

- Research keywords per market (`keyword-research`): the German query for a product is often not the translated
  English one.
- Local currency, units, date formats, phone numbers, addresses, payment and delivery options.
- Local proof: reviews, cases and certifications from that market.
- Localised slugs where the market expects them (`/de/laufschuhe/`), kept stable once published.
- Machine translation is acceptable when reviewed for quality; unreviewed, scaled machine translation can fall under
  scaled content abuse.

## Redirects and locale detection

Locale detection must never stop crawlers or people from reaching a version. Googlebot crawls mostly from US IP
addresses without an `Accept-Language` header, so automatic IP or browser-language redirects hide the other versions.
Show a banner suggesting the matching version instead, and remember the user's choice in a cookie. If the root URL
must choose a locale, serve the selector or the `x-default` version there.

## Differences between search engines

Search engines differ in how they read international signals.

| Engine | Notes |
|---|---|
| Google | hreflang in HTML, headers or sitemap; no country setting since 2022 |
| Bing | uses `content-language` meta and `lang`; ccTLDs and server location matter more; about 32% of Japan (`bing-seo`) |
| Yandex | supports hreflang; region assigned per site in Yandex Webmaster (`yandex-seo`) |
| Naver | Korean content and Naver's own services; read `naver-search-advisor` for Search Advisor and Yeti, and `naver-seo` for titles |
| Baidu | Simplified Chinese, Baidu's own tools, and a hosting and ICP question to settle first; hreflang appears in none of the official pages we read; [references/china-baidu.md](references/china-baidu.md) |
| Seznam | Czech Republic, about 15% (StatCounter, a third-party estimate, September 2026: 14.96%, Google 78.77%); takes IndexNow, so a key set up for Bing also reaches it |

Choosing engines starts from each market's share, so check current figures: StatCounter's search engine pages give a
third-party estimate per country, and a local source can differ widely (`naver-seo` shows two figures for Korea).

## Worked example: the US page ranks in the UK

Situation: a retailer has `/us/` and `/uk/` versions of each category; UK searchers see the US page with dollar
prices.

`hreflang_check.py` on the UK running shoes page: the UK page lists `en-GB` and `en-US`, but the US page lists only
itself and `x-default`, so the pair is not reciprocal; the UK pages also use `en-UK`. Fix: generate hreflang for all
locales from one table in the template, with `en-GB`; check that each version's canonical is itself. Check: the
script reports no errors; Search Console Performance filtered to the United Kingdom shows `/uk/` URLs taking the
impressions within a few weeks.

## Checklist for international SEO

The international checklist runs per template and per locale.

1. URL structure chosen and documented; each locale in its own folder, subdomain or domain.
2. hreflang on every indexable page: self reference, all versions, reciprocal, valid codes, x-default.
3. Each version's canonical is itself; sitemap lists canonical URLs only.
4. `hreflang_check.py` passes on one URL per template.
5. No automatic redirects by IP or browser language.
6. Content, metadata, structured data and navigation translated and localised; keywords researched per market.
7. Search Console Performance filtered by country shows the right version ranking in each market (the old
   International Targeting report was retired in 2022, so hreflang errors are found with a crawl or the script).

## Gotchas in international SEO

The gotchas below cause most wrong-country rankings.

1. **Canonical to the English version.** Symptom: translations drop out of the index. Cause: every translation
   canonicalises to the English page. Fix: give each version a canonical to itself.
2. **`en-UK`.** Symptom: UK pages get no benefit from hreflang. Cause: `en-UK` is not a valid code, so it is ignored.
   Fix: use `en-GB`.
3. **hreflang on non-canonical URLs.** Symptom: Search Console and the script show annotations that have no effect.
   Cause: annotations on URLs with tracking parameters or on redirecting URLs are ignored. Fix: use final canonical
   URLs only.
4. **Missing return links after adding a locale.** Symptom: a new country version never shows. Cause: the new version
   lists the others, the old ones do not list it. Fix: generate hreflang from one locale table.
5. **IP redirect to the local site.** Symptom: other country versions are not indexed. Cause: Googlebot sees only the
   US version. Fix: show a banner and let people choose.
6. **Half-translated pages.** Symptom: the German page ranks nowhere and the English one takes its traffic. Cause:
   translated navigation over an English body is detected as English and competes with the English page. Fix:
   translate the whole main content, navigation and metadata.
7. **Expecting hreflang to rank a weak page.** Symptom: annotations are valid and the page stays low. Cause: hreflang
   swaps which version shows; it does not make a page rank. Fix: improve the page for its market.

## Anti-patterns in international SEO

Anti-patterns in international work treat translation as the job and targeting as an afterthought.

| Do not | Do this instead |
|---|---|
| Creating a country version with nothing different for its users | create a version only when language, prices, delivery, law or contact details differ |
| Translating keywords instead of researching them | research demand per market |
| Using a URL parameter for locale | use a subfolder, subdomain or ccTLD |
| Mixing hreflang methods across a site | choose HTML tags, HTTP headers or the sitemap |
| Publishing unreviewed machine translation at scale | have it reviewed, since it can fall under scaled content abuse |

## References for international SEO

The reference files and scripts below hold the detail for this skill; open one only when the task needs it.

- [references/china-baidu.md](references/china-baidu.md): Baidu's official tools and their age, licensing, hosting and
  what the sources disagree on.
- `scripts/hreflang_check.py`: crawls a hreflang cluster and reports every error.
- The hreflang sitemap format: the `xml-sitemaps` skill, references/sitemap-formats.md.

## See also for international SEO

- `canonical-urls`: canonicals per locale
- `xml-sitemaps`: hreflang in sitemaps
- `keyword-research`: demand per market
- `yandex-seo`: regions and Yandex's own signals
- `bing-seo`: markets such as Japan where Bing is large
- `naver-seo`, `naver-search-advisor`: Naver's content rules, Search Advisor and Yeti for Korea
- `russian-language-seo`: localising English material for Russian search
